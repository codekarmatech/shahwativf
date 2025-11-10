from django.core.management.base import BaseCommand
from core.models import HomepageSlide
from django.core.files.base import ContentFile
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Create sample homepage slides for demonstration'

    def handle(self, *args, **options):
        # Sample slide data
        slides_data = [
            {
                'title': 'Welcome to Shashwat IVF and Women\'s Hospital',
                'subtitle': 'Experience the joy of parenthood with our NABH accredited IVF center in Ahmedabad. We provide comprehensive fertility solutions and exceptional care.',
                'button_text': 'Schedule Consultation',
                'button_link': '/contact',
                'order': 1
            },
            {
                'title': 'Advanced Fertility Treatments',
                'subtitle': 'State-of-the-art facilities and cutting-edge reproductive technology to give you the best chance of success in your journey towards parenthood.',
                'button_text': 'Learn More',
                'button_link': '/services',
                'order': 2
            },
            {
                'title': 'Expert Medical Team',
                'subtitle': 'Our team of highly skilled fertility specialists, gynecologists, and embryologists are dedicated to providing personalized care.',
                'button_text': 'Meet Our Doctors',
                'button_link': '/team',
                'order': 3
            }
        ]

        # Create slides if they don't exist
        for slide_data in slides_data:
            slide, created = HomepageSlide.objects.get_or_create(
                title=slide_data['title'],
                defaults={
                    'subtitle': slide_data['subtitle'],
                    'button_text': slide_data['button_text'],
                    'button_link': slide_data['button_link'],
                    'order': slide_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created slide: "{slide.title}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Slide already exists: "{slide.title}"')
                )

        self.stdout.write(
            self.style.SUCCESS('Sample slides creation completed!')
        )
        self.stdout.write(
            self.style.WARNING('Note: You can add images to these slides through the Django admin interface.')
        )