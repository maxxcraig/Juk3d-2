import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class FreesoundService:
    """
    Service class for interacting with Freesound API
    Uses client credentials for public sound search
    """
    
    def __init__(self):
        self.base_url = settings.FREESOUND_API_BASE_URL
        self.client_id = settings.FREESOUND_CLIENT_ID
        self.client_secret = settings.FREESOUND_CLIENT_SECRET
        self.access_token = None
    
    def get_access_token(self):
        """
        Get access token using client credentials flow for Freesound
        """
        if self.access_token:
            return self.access_token
            
        # Freesound uses a specific endpoint for client credentials
        token_url = f"{self.base_url}/oauth2/access_token/"
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(token_url, data=data, headers=headers)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                logger.info("Successfully obtained Freesound access token")
                return self.access_token
            else:
                logger.error(f"Freesound token request failed: {response.status_code} - {response.text}")
                return None
            
        except requests.RequestException as e:
            logger.error(f"Error getting Freesound access token: {e}")
            return None
    
    def search_sounds(self, query, page=1, page_size=15):
        """
        Search for sounds on Freesound
        For public search, we can try using the client_id as token parameter
        """
        if not self.client_id:
            return self._mock_response(query)
        
        search_url = f"{self.base_url}/search/text/"
        
        params = {
            'query': query,
            'page': page,
            'page_size': page_size,
            'fields': 'id,name,description,username,duration,previews,download,license',
            'filter': 'duration:[30 TO *]',  # At least 30 seconds long
            'token': self.client_id  # Try using client_id as token
        }
        
        try:
            response = requests.get(search_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_search_results(data)
            else:
                logger.error(f"Freesound search failed: {response.status_code} - {response.text}")
                return self._mock_response(query)
            
        except requests.RequestException as e:
            logger.error(f"Error searching Freesound: {e}")
            return self._mock_response(query)
    
    def get_sound_details(self, sound_id):
        """
        Get detailed information about a specific sound
        """
        token = self.get_access_token()
        if not token:
            return None
            
        sound_url = f"{self.base_url}/sounds/{sound_id}/"
        
        params = {
            'fields': 'id,name,description,username,duration,previews,download,license,tags',
        }
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        try:
            response = requests.get(sound_url, params=params, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Error getting sound details from Freesound: {e}")
            return None
    
    def _format_search_results(self, freesound_data):
        """
        Format Freesound API response for jukebox frontend
        """
        results = []
        
        for sound in freesound_data.get('results', []):
            # Use high-quality preview if available
            preview_url = None
            previews = sound.get('previews', {})
            
            if previews.get('preview-hq-mp3'):
                preview_url = previews['preview-hq-mp3']
            elif previews.get('preview-lq-mp3'):
                preview_url = previews['preview-lq-mp3']
            elif previews.get('preview-hq-ogg'):
                preview_url = previews['preview-hq-ogg']
            elif previews.get('preview-lq-ogg'):
                preview_url = previews['preview-lq-ogg']
            
            formatted_sound = {
                'id': f"freesound_{sound.get('id')}",
                'title': sound.get('name', 'Unknown Title'),
                'artist': sound.get('username', 'Unknown Artist'),
                'duration': int(float(sound.get('duration', 0))),
                'preview_url': preview_url,
                'download_url': sound.get('download'),
                'license': sound.get('license', 'Unknown License'),
                'description': sound.get('description', '')[:200] + '...' if sound.get('description', '') else '',
                'external_id': str(sound.get('id')),
                'source': 'freesound'
            }
            
            results.append(formatted_sound)
        
        return {
            'results': results,
            'total_count': freesound_data.get('count', 0),
            'next': freesound_data.get('next'),
            'previous': freesound_data.get('previous')
        }
    
    def _mock_response(self, query):
        """
        Fallback mock response when API is unavailable
        """
        return {
            'results': [
                {
                    'id': f'mock_sound_{i}',
                    'title': f'Sample Track {i} - {query}',
                    'artist': f'Artist {i}',
                    'duration': 180 + i * 15,
                    'preview_url': None,
                    'download_url': None,
                    'license': 'Creative Commons',
                    'description': f'Mock sound for testing - searched for "{query}"',
                    'external_id': f'mock_{i}',
                    'source': 'mock'
                }
                for i in range(1, 6)
            ],
            'total_count': 5,
            'next': None,
            'previous': None,
            'message': 'Using mock data - Freesound API unavailable'
        }