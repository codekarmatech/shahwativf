from django.core.management.base import BaseCommand
from core.models import Doctor

class Command(BaseCommand):
    help = 'Clear image fields for doctors with missing images'

    def handle(self, *args, **options):
        doctors = Doctor.objects.filter(image__in=['media/doctors/shital.jpg', 'media/doctors/rajesh.jpg'])
        for doctor in doctors:
            doctor.image = None
            doctor.save()
        self.stdout.write(self.style.SUCCESS('Successfully cleared doctor images'))