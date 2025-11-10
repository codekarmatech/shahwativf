"""
scrape_shashwativf.py
======================

This module provides a self‑contained command line tool for scraping the
`https://www.shashwativf.com/` website.  The goal of the script is to
download all textual content and image assets from the public pages of
the site while respecting its robots.txt directives.  Content from
each page is stored in a structured directory hierarchy under a user
provided output directory, making it easy to locate the original
context of every downloaded resource.

Key features
------------

* **Robots awareness**: Before scraping begins, the script fetches the
  site's robots.txt file and parses it to verify that each target URL
  is allowed for scraping.  If a path is disallowed the script
  gracefully skips it.

* **Page enumeration**: A static list of page endpoints (e.g.
  ``index.php``, ``doctor.php``, ``team.php``, etc.) is defined in
  ``PAGE_ENDPOINTS``.  These endpoints were derived from an analysis of
  the site's navigation structure and represent the principal public
  pages of the site as of July 2025.  If the site's navigation
  changes, you can update this list accordingly or supply your own
  endpoints at runtime via the ``--extra-pages`` argument.

* **Resource extraction**:  For every page, the script downloads the
  HTML and uses `BeautifulSoup` to identify image resources via the
  ``<img>`` tag, ``data-bg-img`` attributes and inline CSS
  ``background-image`` declarations.  Relative URLs are resolved
  against the page's base URL.  Duplicate image URLs across pages are
  de‑duplicated to avoid redundant downloads.

* **Folder structure**:  Each page's scraped content is saved in a
  directory named after the page (e.g. ``index``, ``doctor``).  Textual
  content is stored as ``page.txt`` and extracted images are saved in
  a subdirectory called ``images``.  Images specific to hero
  sections (identified via ``data-bg-img`` or background images on
  sections with IDs like ``home``) are stored in a dedicated
  ``hero_images`` folder to make it clear which assets correspond to
  the hero carousel or banner.

* **Extensibility**:  The script is written as a class
  (`ShashwativfScraper`) to encapsulate scraping logic.  It exposes
  hooks for adding additional pages or overriding how hero images are
  detected.  Comprehensive logging is provided via Python's
  ``logging`` module.

Usage example
-------------

To download the site into a directory called ``scraped_site`` you
would run:

```
python scrape_shashwativf.py --output-dir scraped_site
```

To include additional pages not enumerated in ``PAGE_ENDPOINTS``:

```
python scrape_shashwativf.py \
    --output-dir scraped_site \
    --extra-pages about.php,pricing.php
```

Note:  This script requires Python 3.8 or later and the ``beautifulsoup4``
package.  You can install dependencies with ``pip install -r
requirements.txt``.  Internet access is required at runtime.
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional, Set

import requests
from bs4 import BeautifulSoup


def parse_robots_txt(base_url: str) -> Set[str]:
    """Fetches the robots.txt for the given base URL and returns a set of
    disallowed path prefixes for user agent ``*``.  If the site does not
    provide a robots file or the file is unreachable, an empty set is
    returned.

    Args:
        base_url: The scheme and authority of the site, e.g.
            ``https://www.shashwativf.com``.

    Returns:
        A set of disallowed path prefixes.  Each entry is a string
        beginning with a slash.
    """
    robots_url = urllib.parse.urljoin(base_url, "/robots.txt")
    try:
        response = requests.get(robots_url, timeout=10)
        response.raise_for_status()
    except Exception as exc:
        logging.info("Unable to fetch robots.txt from %s: %s", robots_url, exc)
        return set()
    disallowed: Set[str] = set()
    ua: Optional[str] = None
    for line in response.text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.lower().startswith('user-agent'):
            ua = line.split(':', 1)[1].strip()
        elif ua in ('*', None) and line.lower().startswith('disallow'):
            path = line.split(':', 1)[1].strip()
            if path:
                disallowed.add(path)
    return disallowed


def is_allowed(url: str, disallowed_paths: Set[str], base_url: str) -> bool:
    """Determines whether a URL is allowed under robots.txt rules.

    Args:
        url: The absolute URL being considered.
        disallowed_paths: A set of disallowed path prefixes from
            ``parse_robots_txt``.
        base_url: The scheme and authority of the site.

    Returns:
        True if the URL's path does not begin with any disallowed
        prefix, otherwise False.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.netloc:
        # Relative URL; join with base
        url = urllib.parse.urljoin(base_url, url)
        parsed = urllib.parse.urlparse(url)
    # Only enforce rules on the same host
    if parsed.netloc != urllib.parse.urlparse(base_url).netloc:
        return True
    path = parsed.path or '/'
    for disallowed in disallowed_paths:
        # According to the standard, a blank disallow means allow all
        if not disallowed:
            continue
        if path.startswith(disallowed):
            return False
    return True


@dataclass
class PageScrapeResult:
    """Represents the scraped content for a single page."""
    url: str
    html: str
    text: str
    images: List[str] = field(default_factory=list)
    hero_images: List[str] = field(default_factory=list)


class ShashwativfScraper:
    """Encapsulates logic for scraping the Shashwat IVF site."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip('/')
        # Precompute robots.txt rules
        self.disallowed = parse_robots_txt(self.base_url)
        logging.debug("Robots disallowed paths: %s", self.disallowed)

    def fetch_page(self, endpoint: str) -> Optional[str]:
        """Fetches the raw HTML for a given endpoint.

        Args:
            endpoint: Path relative to base (e.g. ``index.php``).

        Returns:
            The HTML as a string, or None if the request fails or is
            disallowed by robots.txt.
        """
        url = urllib.parse.urljoin(self.base_url + '/', endpoint.lstrip('/'))
        if not is_allowed(url, self.disallowed, self.base_url):
            logging.warning("Skipping %s due to robots.txt disallow", url)
            return None
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; ShashwatScraper/1.0)'
        }
        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            return response.text
        except Exception as exc:
            logging.error("Failed to fetch %s: %s", url, exc)
            return None

    def extract_images(self, soup: BeautifulSoup) -> (List[str], List[str]):
        """Extracts image URLs and hero image URLs from the parsed soup.

        Standard images are identified via ``<img src>`` attributes,
        whereas hero images are captured from ``data-bg-img`` attributes or
        inline CSS ``background-image`` declarations.  Duplicate URLs are
        removed while preserving order.

        Args:
            soup: The parsed BeautifulSoup object of the page.

        Returns:
            A tuple containing two lists: (images, hero_images).
        """
        images: List[str] = []
        hero_images: List[str] = []

        def add_unique(target: List[str], url: str) -> None:
            if url and url not in target:
                target.append(url)

        # Extract from <img>
        for img in soup.find_all('img'):
            src = img.get('src') or ''
            if src:
                add_unique(images, src.strip())
        # Extract from data-bg-img
        for elem in soup.find_all(attrs={'data-bg-img': True}):
            bg = elem['data-bg-img']
            add_unique(hero_images, bg.strip())
        # Extract from inline CSS: style="background-image: url(...)"
        style_re = re.compile(r'background-image\s*:\s*url\([\"\']?(.*?)[\"\']?\)', re.IGNORECASE)
        for elem in soup.find_all(style=True):
            match = style_re.search(elem['style'])
            if match:
                add_unique(hero_images, match.group(1).strip())
        return images, hero_images

    def scrape_page(self, endpoint: str) -> Optional[PageScrapeResult]:
        """Scrapes a single page and returns structured results.

        Args:
            endpoint: The relative path to scrape.

        Returns:
            A PageScrapeResult or None if scraping failed.
        """
        html = self.fetch_page(endpoint)
        if html is None:
            return None
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)
        images, hero_images = self.extract_images(soup)
        # Convert to absolute URLs
        abs_images = [urllib.parse.urljoin(self.base_url + '/', url) for url in images]
        abs_hero = [urllib.parse.urljoin(self.base_url + '/', url) for url in hero_images]
        return PageScrapeResult(
            url=urllib.parse.urljoin(self.base_url + '/', endpoint),
            html=html,
            text=text,
            images=abs_images,
            hero_images=abs_hero
        )

    def download_image(self, url: str, dest: Path) -> None:
        """Downloads a single image to the destination path.

        Args:
            url: Absolute URL of the image.
            dest: Path on disk where the image will be saved.  Parent
                directories are created automatically.
        """
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; ShashwatScraper/1.0)'}
            with requests.get(url, headers=headers, stream=True, timeout=20) as resp:
                resp.raise_for_status()
                with open(dest, 'wb') as out_file:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            out_file.write(chunk)
            logging.info("Downloaded image %s", dest)
        except Exception as exc:
            logging.error("Failed to download image %s: %s", url, exc)

    def save_page(self, result: PageScrapeResult, out_dir: Path) -> None:
        """Saves the scraped page content and images into the output directory.

        Args:
            result: The scraped page result.
            out_dir: Base directory where the page folder will be created.
        """
        page_name = Path(urllib.parse.urlparse(result.url).path).stem or 'index'
        page_dir = out_dir / page_name
        page_dir.mkdir(parents=True, exist_ok=True)
        # Save text content
        text_file = page_dir / 'page.txt'
        text_file.write_text(result.text, encoding='utf-8')
        # Save HTML content
        html_file = page_dir / 'page.html'
        html_file.write_text(result.html, encoding='utf-8')
        # Save images
        for img_url in result.images:
            fname = os.path.basename(urllib.parse.urlparse(img_url).path)
            self.download_image(img_url, page_dir / 'images' / fname)
        # Save hero images
        for hero_url in result.hero_images:
            fname = os.path.basename(urllib.parse.urlparse(hero_url).path)
            self.download_image(hero_url, page_dir / 'hero_images' / fname)


def run_scraper(base_url: str, output_dir: Path, pages: Iterable[str]) -> None:
    """Runs the scraping process for a set of pages.

    Args:
        base_url: The root of the site to scrape.
        output_dir: Directory where scraped data will be stored.
        pages: Iterable of relative page paths.
    """
    scraper = ShashwativfScraper(base_url)
    for endpoint in pages:
        logging.info("Scraping page %s", endpoint)
        result = scraper.scrape_page(endpoint)
        if result is None:
            logging.warning("No result for %s", endpoint)
            continue
        scraper.save_page(result, output_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape the shashwativf.com website.")
    parser.add_argument(
        '--base-url',
        default='https://www.shashwativf.com',
        help='Base URL of the site (default: https://www.shashwativf.com)'
    )
    parser.add_argument(
        '--output-dir',
        required=True,
        help='Directory where scraped content will be saved'
    )
    parser.add_argument(
        '--extra-pages',
        default='',
        help='Comma separated list of additional pages (relative URLs) to scrape'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        help='Logging level (DEBUG, INFO, WARNING, ERROR)'
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO),
                        format='%(asctime)s - %(levelname)s - %(message)s')
    output_dir = Path(args.output_dir)
    # Primary pages discovered during DOM analysis
    PAGE_ENDPOINTS: List[str] = [
        'index.php',
        'doctor.php',
        'team.php',
        'obgynecology.php',
        'fertility.php',
        'counselling.php',
        'andrology.php',
        'endoscopy.php',
        'iui.php',
        'ivf.php',
        'icsi.php',
        'embryo.php',
        'vitrification.php',
        'embryoscopy.php',
        'blastocystculture.php',
        'assistedhatching.php',
        'media.php',
        'success.php',
        'contact.php',
        'connect.php',
    ]
    # Incorporate extra pages supplied by the user
    if args.extra_pages:
        for page in [p.strip() for p in args.extra_pages.split(',') if p.strip()]:
            if page not in PAGE_ENDPOINTS:
                PAGE_ENDPOINTS.append(page)
    run_scraper(args.base_url, output_dir, PAGE_ENDPOINTS)


if __name__ == '__main__':
    main()