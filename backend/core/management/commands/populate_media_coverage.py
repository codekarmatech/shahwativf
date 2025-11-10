from django.core.management.base import BaseCommand
from core.models import MediaCoverage
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Populate MediaCoverage model with placeholder data'

    def handle(self, *args, **options):
        # Clear existing data
        MediaCoverage.objects.all().delete()
        
        media_data = [
            {
                'title': 'Shashwat IVF Achieves 85% Success Rate in Advanced IVF Treatments',
                'description': 'Leading fertility clinic in Ahmedabad reports breakthrough success rates using latest embryo selection technology and personalized treatment protocols.',
                'media_type': 'news',
                'source': 'Times of India',
                'display_size': 'large',
                'display_priority': 100,
                'is_featured': True,
                'external_url': 'https://timesofindia.indiatimes.com/city/ahmedabad/fertility-clinic-success',
                'date': date.today() - timedelta(days=15)
            },
            {
                'title': 'Dr. Shashwat Jani Receives Excellence Award for Reproductive Medicine',
                'description': 'Recognized by Gujarat Medical Association for outstanding contributions to fertility treatments and patient care excellence.',
                'media_type': 'award',
                'source': 'Gujarat Medical Journal',
                'display_size': 'medium',
                'display_priority': 95,
                'is_featured': True,
                'external_url': 'https://gujaratmedical.org/awards-2024',
                'date': date.today() - timedelta(days=30)
            },
            {
                'title': 'Revolutionary ICSI Technique Helps 500+ Couples Achieve Parenthood',
                'description': 'Shashwat IVF introduces advanced micromanipulation technology resulting in higher fertilization rates and successful pregnancies.',
                'media_type': 'achievement',
                'source': 'Indian Express',
                'display_size': 'medium',
                'display_priority': 90,
                'is_featured': True,
                'external_url': 'https://indianexpress.com/article/cities/ahmedabad/ivf-breakthrough',
                'date': date.today() - timedelta(days=45)
            },
            {
                'title': 'Patient Success Story: From Despair to Joy in 18 Months',
                'description': 'Couple shares emotional journey of overcoming 8 years of infertility through personalized IVF treatment at Shashwat IVF.',
                'media_type': 'testimonial',
                'source': 'Ahmedabad Mirror',
                'display_size': 'small',
                'display_priority': 85,
                'is_featured': False,
                'external_url': 'https://ahmedabadmirror.com/patient-success-story',
                'date': date.today() - timedelta(days=60)
            },
            {
                'title': 'Shashwat IVF Launches Free Fertility Awareness Campaign',
                'description': 'Community outreach program educates 10,000+ couples about fertility health and treatment options across Gujarat.',
                'media_type': 'social_impact',
                'source': 'DNA India',
                'display_size': 'small',
                'display_priority': 80,
                'is_featured': False,
                'external_url': 'https://dnaindia.com/ahmedabad/fertility-awareness',
                'date': date.today() - timedelta(days=75)
            },
            {
                'title': 'Advanced Embryo Freezing Technology Increases Success Rates by 25%',
                'description': 'State-of-the-art vitrification technique preserves embryo quality and improves pregnancy outcomes for patients.',
                'media_type': 'technology',
                'source': 'Business Standard',
                'display_size': 'medium',
                'display_priority': 75,
                'is_featured': True,
                'external_url': 'https://business-standard.com/healthcare/fertility-tech',
                'date': date.today() - timedelta(days=90)
            },
            {
                'title': 'Dr. Jani Speaks at International Fertility Conference in Mumbai',
                'description': 'Presents research on personalized ovarian stimulation protocols and their impact on IVF success rates.',
                'media_type': 'conference',
                'source': 'Medical News Today',
                'display_size': 'small',
                'display_priority': 70,
                'is_featured': False,
                'external_url': 'https://medicalnewstoday.com/fertility-conference-2024',
                'date': date.today() - timedelta(days=105)
            },
            {
                'title': 'Research Publication: Novel Approach to Male Infertility Treatment',
                'description': 'Groundbreaking study published in International Journal of Reproductive Medicine shows 40% improvement in sperm quality.',
                'media_type': 'research',
                'source': 'Journal of Reproductive Medicine',
                'display_size': 'small',
                'display_priority': 65,
                'is_featured': False,
                'external_url': 'https://reproductivemedicine.org/male-infertility-study',
                'date': date.today() - timedelta(days=120)
            },
            {
                'title': 'Exclusive Interview: Future of Fertility Treatments in India',
                'description': 'Dr. Shashwat Jani discusses emerging technologies, accessibility challenges, and the future landscape of reproductive medicine.',
                'media_type': 'interview',
                'source': 'NDTV Health',
                'display_size': 'wide',
                'display_priority': 60,
                'is_featured': True,
                'external_url': 'https://ndtv.com/health/fertility-future-interview',
                'date': date.today() - timedelta(days=135)
            },
            {
                'title': '2024 Success Statistics: 1,200+ Healthy Babies Born',
                'description': 'Annual report showcases exceptional outcomes with 82% clinical pregnancy rate and 78% live birth rate across all age groups.',
                'media_type': 'statistics',
                'source': 'Healthcare Today',
                'display_size': 'large',
                'display_priority': 55,
                'is_featured': True,
                'external_url': 'https://healthcaretoday.in/ivf-success-statistics',
                'date': date.today() - timedelta(days=150)
            },
            {
                'title': 'Shashwat IVF Receives ISO 9001:2015 Certification',
                'description': 'Quality management system certification ensures highest standards in patient care and laboratory procedures.',
                'media_type': 'award',
                'source': 'Quality Assurance India',
                'display_size': 'small',
                'display_priority': 50,
                'is_featured': False,
                'external_url': 'https://qualityassurance.in/iso-certification-healthcare',
                'date': date.today() - timedelta(days=165)
            },
            {
                'title': 'Miracle Twins Born After 12 Years of Infertility Struggle',
                'description': 'Emotional testimonial from couple who welcomed healthy twins through advanced IVF treatment and unwavering medical support.',
                'media_type': 'testimonial',
                'source': 'Divya Bhaskar',
                'display_size': 'medium',
                'display_priority': 45,
                'is_featured': False,
                'external_url': 'https://divyabhaskar.co.in/miracle-twins-story',
                'date': date.today() - timedelta(days=180)
            },
            {
                'title': 'AI-Powered Embryo Selection Improves IVF Outcomes',
                'description': 'Implementation of artificial intelligence in embryo assessment leads to 30% increase in implantation success rates.',
                'media_type': 'technology',
                'source': 'Tech Health News',
                'display_size': 'small',
                'display_priority': 40,
                'is_featured': False,
                'external_url': 'https://techhealthnews.com/ai-embryo-selection',
                'date': date.today() - timedelta(days=195)
            },
            {
                'title': 'Free Fertility Check-up Camp Benefits 2,000+ Women',
                'description': 'Community health initiative provides comprehensive fertility assessments and counseling to underprivileged women across Gujarat.',
                'media_type': 'social_impact',
                'source': 'Gujarat Samachar',
                'display_size': 'small',
                'display_priority': 35,
                'is_featured': False,
                'external_url': 'https://gujaratsamachar.com/fertility-camp-2024',
                'date': date.today() - timedelta(days=210)
            },
            {
                'title': 'Breakthrough in Endometriosis Treatment Increases Pregnancy Rates',
                'description': 'Novel surgical approach combined with hormonal therapy shows remarkable results in treating endometriosis-related infertility.',
                'media_type': 'research',
                'source': 'Obstetrics & Gynecology Today',
                'display_size': 'medium',
                'display_priority': 30,
                'is_featured': False,
                'external_url': 'https://obgyntoday.com/endometriosis-breakthrough',
                'date': date.today() - timedelta(days=225)
            },
            {
                'title': 'Patient Testimonial: Hope Restored After Multiple Failed Attempts',
                'description': 'Inspiring story of perseverance and medical excellence leading to successful pregnancy after 5 previous IVF failures.',
                'media_type': 'testimonial',
                'source': 'Sandesh News',
                'display_size': 'small',
                'display_priority': 25,
                'is_featured': False,
                'external_url': 'https://sandeshnews.in/hope-restored-ivf-success',
                'date': date.today() - timedelta(days=240)
            }
        ]
        
        created_count = 0
        for data in media_data:
            media_coverage = MediaCoverage.objects.create(**data)
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Created: {media_coverage.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} media coverage entries')
        )