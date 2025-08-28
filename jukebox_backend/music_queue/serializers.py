from rest_framework import serializers
from .models import QueueItem, CurrentlyPlaying
from venues.serializers import VenueSerializer, SongSerializer

class QueueItemSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    
    class Meta:
        model = QueueItem
        fields = ['id', 'venue', 'song', 'is_paid', 'amount_paid', 'status', 'queued_at', 'played_at']

class CurrentlyPlayingSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)
    queue_item = QueueItemSerializer(read_only=True)
    
    class Meta:
        model = CurrentlyPlaying
        fields = ['venue', 'queue_item', 'started_at']

class AddToQueueSerializer(serializers.Serializer):
    song_id = serializers.CharField(max_length=100)  # External music API ID
    title = serializers.CharField(max_length=200)
    artist = serializers.CharField(max_length=200)
    duration = serializers.IntegerField()
    album_art_url = serializers.URLField(required=False)
    is_paid = serializers.BooleanField(default=False)
    payment_method_id = serializers.CharField(max_length=255, required=False)  # Stripe payment method ID