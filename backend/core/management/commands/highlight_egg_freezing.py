from django.core.management.base import BaseCommand
from core.models import Service, HomepageSlide

class Command(BaseCommand):
    help = 'Highlight Egg Freezing service and feature it on homepage'

    def handle(self, *args, **options):
        # Ensure Egg Freezing service exists and is featured
        service, _ = Service.objects.update_or_create(
            slug='egg-freezing',
            defaults={
                'title': 'Egg Freezing',
                'description': 'Preserve your fertility with modern egg freezing techniques and personalized care.',
                'content': 'Egg freezing (oocyte cryopreservation) allows women to preserve their reproductive potential. Our center offers internationally benchmarked protocols, advanced vitrification technology, and compassionate counselling to help you make informed choices.',
                'is_featured': True,
            }
        )

        # Create/Update a prominent homepage slide for Egg Freezing
        slide, _ = HomepageSlide.objects.update_or_create(
            title='Egg Freezing: Preserve Your Fertility',
            defaults={
                'subtitle': 'Advanced vitrification technology with compassionate counselling to support your future family plans.',
                'button_text': 'Explore Egg Freezing',
                'button_link': '/services',
                'order': 1,
                'is_active': True,
            }
        )

        self.stdout.write(self.style.SUCCESS('Egg Freezing service highlighted and homepage slide updated'))