from django.core.management.base import BaseCommand
from core.models import MediaCoverage
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Update MediaCoverage entries with placeholder images'

    def handle(self, *args, **options):
        # Update specific entries with images
        updates = [
            {
                'title_contains': 'Shashwat IVF Achieves 85% Success Rate',
                'image_path': 'media/news_article_1.svg'
            },
            {
                'title_contains': 'Dr. Shashwat Jani Receives Excellence Award',
                'image_path': 'media/award_recognition.svg'
            },
            {
                'title_contains': 'AI-Powered Embryo Selection',
                'image_path': 'media/technology_innovation.svg'
            },
            {
                'title_contains': 'Advanced Embryo Freezing Technology',
                'image_path': 'media/technology_innovation.svg'
            },
            {
                'title_contains': '2024 Success Statistics',
                'image_path': 'media/news_article_1.svg'
            }
        ]
        
        updated_count = 0
        for update in updates:
            try:
                media_item = MediaCoverage.objects.filter(
                    title__icontains=update['title_contains']
                ).first()
                
                if media_item:
                    # Update the image field with the file path
                    media_item.image = update['image_path']
                    media_item.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated image for: {media_item.title}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Media item not found for: {update["title_contains"]}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error updating {update["title_contains"]}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} media coverage entries with images')
        )