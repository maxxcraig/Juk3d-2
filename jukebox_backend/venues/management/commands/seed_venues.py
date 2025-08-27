from django.core.management.base import BaseCommand
from venues.models import Venue

class Command(BaseCommand):
    help = 'Create initial venue data'

    def handle(self, *args, **options):
        venues_data = [
            {
                'name': "L&L Hawaiian BBQ",
                'description': "Authentic Hawaiian BBQ with island vibes"
            },
            {
                'name': "Chipotle",
                'description': "Fresh Mexican grill with customizable bowls"
            },
            {
                'name': "Trujillos",
                'description': "Traditional Mexican cuisine and atmosphere"
            }
        ]

        for venue_data in venues_data:
            venue, created = Venue.objects.get_or_create(
                name=venue_data['name'],
                defaults=venue_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created venue: {venue.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Venue already exists: {venue.name}')
                )