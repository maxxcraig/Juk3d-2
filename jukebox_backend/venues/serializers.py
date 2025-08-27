from rest_framework import serializers
from .models import Venue, Song

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'description', 'is_active', 'created_at']

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'duration', 'external_id', 'album_art_url', 'created_at']