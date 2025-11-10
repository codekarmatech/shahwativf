from django.core.management.base import BaseCommand
from django.db.models import F, Value
from django.db.models.functions import Concat
from core.models import TeamMember, Doctor

class Command(BaseCommand):
    help = 'Populate and update team members and doctor credentials per requirements'

    def handle(self, *args, **options):
        # Update Doctor degrees for Dr. Shital Punjabi to include FICOG
        if Doctor.objects.filter(name__iexact='Dr. Shital Punjabi').exists():
            Doctor.objects.filter(name__iexact='Dr. Shital Punjabi', degrees__isnull=False).update(
                degrees=Concat(F('degrees'), Value(', FICOG'))
            )
            Doctor.objects.filter(name__iexact='Dr. Shital Punjabi', degrees='').update(
                degrees='FICOG'
            )
        else:
            # If no Doctor record, attempt to update TeamMember designation as fallback
            TeamMember.objects.filter(name__iexact='Dr. Shital Punjabi').update(
                qualifications=Concat(F('qualifications'), Value(', FICOG'))
            )

        # Remove specified team members
        TeamMember.objects.filter(name__iexact='Basanti Katara').update(is_active=False)
        TeamMember.objects.filter(name__iexact='Rohit Satani').update(is_active=False)

        # Add/Update Dr. Trishala Punjabi
        TeamMember.objects.update_or_create(
            name='Dr. Trishala Punjabi',
            defaults={
                'designation': 'MBBS',
                'qualifications': '',
                'category': 'support',
                'is_active': True,
            }
        )

        # Highlight achievements for Dr. Shital Punjabi
        Doctor.objects.filter(name__iexact='Dr. Shital Punjabi').update(
            achievements='Recipient of multiple gold medals and national awards in Gynecology and Obstetrics.'
        )

        # Add 10 new team members (placeholders for images/credentials)
        new_members = [
            ('Tapanbhai', 'Support Staff'),
            ('Nileshbhai', 'Support Staff'),
            ('Devbhai', 'Support Staff'),
            ('Bijal', 'Administrative Staff'),
            ('Priya', 'Administrative Staff'),
            ('Khushboo', 'Nursing Staff'),
            ('Dhavalbhai', 'Support Staff'),
            ('M.H. Shaikh', 'Technician'),
            ('Mansi', 'Administrative Staff'),
            ('Dr. Niyati', 'MBBS, Gynecologist'),
        ]

        for name, designation in new_members:
            TeamMember.objects.update_or_create(
                name=name,
                defaults={
                    'designation': designation,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS('Team members populated/updated successfully'))