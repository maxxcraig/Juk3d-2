from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests
from .models import Venue, Song
from .serializers import VenueSerializer, SongSerializer

class VenueListView(generics.ListAPIView):
    queryset = Venue.objects.filter(is_active=True)
    serializer_class = VenueSerializer

class VenueDetailView(generics.RetrieveAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

@api_view(['GET'])
def search_songs(request):
    query = request.GET.get('q', '')
    if not query:
        return Response({'error': 'Query parameter "q" is required'}, status=400)
    
    # Import here to avoid circular imports
    from .freesound_service import FreesoundService
    
    # Get pagination parameters
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 15))
    
    # Search using Freesound API
    freesound = FreesoundService()
    results = freesound.search_sounds(query, page=page, page_size=page_size)
    
    return Response(results)
