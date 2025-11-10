from django.core.management.base import BaseCommand
from core.models import SocialMediaLink, ContactInfo

class Command(BaseCommand):
    help = 'Populate footer data with sample social media links and contact information'

    def handle(self, *args, **options):
        # Create contact info
        contact_info, created = ContactInfo.objects.get_or_create(
            defaults={
                'address': 'Shashwat IVF and Women\'s Hospital, Ahmedabad, Gujarat, India',
                'phone': ': (+91)75676-72781',
                'email': 'info@shashwativf.com'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created contact info')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Contact info already exists')
            )

        # Create social media links
        social_links_data = [
            {
                'platform': 'Facebook',
                'url': 'https://www.facebook.com/shashwativf',
                'is_active': True,
                'order': 1
            },
            {
                'platform': 'YouTube',
                'url': 'https://www.youtube.com/channel/shashwativf',
                'is_active': True,
                'order': 2
            },
            {
                'platform': 'Instagram',
                'url': 'https://www.instagram.com/shashwativf',
                'is_active': True,
                'order': 3
            },
        ]

        for link_data in social_links_data:
            social_link, created = SocialMediaLink.objects.get_or_create(
                platform=link_data['platform'],
                defaults=link_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created {link_data["platform"]} social link')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'{link_data["platform"]} social link already exists')
                )

        self.stdout.write(
            self.style.SUCCESS('Footer data population completed!')
        )