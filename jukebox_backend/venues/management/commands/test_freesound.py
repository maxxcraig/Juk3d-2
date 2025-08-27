from django.core.management.base import BaseCommand
from venues.freesound_service import FreesoundService

class Command(BaseCommand):
    help = 'Test Freesound API connection and search functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--query',
            type=str,
            default='ambient',
            help='Search query to test (default: ambient)'
        )

    def handle(self, *args, **options):
        query = options['query']
        
        self.stdout.write(f'Testing Freesound API with query: "{query}"')
        
        freesound = FreesoundService()
        
        # Test client ID configuration
        self.stdout.write('Checking API configuration...')
        
        if freesound.client_id:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Client ID configured: {freesound.client_id[:8]}...')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ No client ID configured')
            )
            return
        
        # Test search
        self.stdout.write(f'Searching for "{query}"...')
        results = freesound.search_sounds(query, page=1, page_size=5)
        
        if results.get('results'):
            self.stdout.write(
                self.style.SUCCESS(f'✅ Found {len(results["results"])} sounds')
            )
            
            for i, sound in enumerate(results['results'][:3], 1):
                self.stdout.write(f'  {i}. {sound["title"]} by {sound["artist"]} ({sound["duration"]}s)')
                if sound.get('preview_url'):
                    self.stdout.write(f'     Preview: {sound["preview_url"]}')
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ No results found or API error')
            )
        
        # Display total count
        total = results.get('total_count', 0)
        self.stdout.write(f'Total sounds available for "{query}": {total}')
        
        if results.get('message'):
            self.stdout.write(f'Message: {results["message"]}')