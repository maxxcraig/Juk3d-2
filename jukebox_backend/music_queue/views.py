from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
from decimal import Decimal
from .models import QueueItem, CurrentlyPlaying
from venues.models import Venue, Song
from .serializers import QueueItemSerializer, CurrentlyPlayingSerializer, AddToQueueSerializer

@api_view(['GET'])
def venue_queue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    
    # Get currently playing
    try:
        currently_playing = CurrentlyPlaying.objects.get(venue=venue)
        current_song = CurrentlyPlayingSerializer(currently_playing).data
    except CurrentlyPlaying.DoesNotExist:
        current_song = None
    
    # Get next 10 songs in queue
    queue_items = QueueItem.objects.filter(
        venue=venue,
        status='queued'
    ).order_by('-is_paid', 'queued_at')[:10]
    
    queue_data = QueueItemSerializer(queue_items, many=True).data
    
    return Response({
        'venue_id': venue_id,
        'venue_name': venue.name,
        'currently_playing': current_song,
        'queue': queue_data
    })

@api_view(['POST'])
def add_to_queue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    serializer = AddToQueueSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # Handle payment if paid song
    if data.get('is_paid', False):
        payment_token = data.get('payment_token')
        if not payment_token:
            return Response({
                'error': 'Payment token required for paid songs'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Placeholder for Stripe payment processing
        payment_success = process_payment(payment_token, Decimal('1.00'))
        if not payment_success:
            return Response({
                'error': 'Payment failed - Stripe integration pending'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create song
    song, created = Song.objects.get_or_create(
        external_id=data['song_id'],
        defaults={
            'title': data['title'],
            'artist': data['artist'],
            'duration': data['duration'],
            'album_art_url': data.get('album_art_url', '')
        }
    )
    
    # Create queue item
    queue_item = QueueItem.objects.create(
        venue=venue,
        song=song,
        is_paid=data.get('is_paid', False),
        amount_paid=Decimal('1.00') if data.get('is_paid', False) else Decimal('0.00'),
        user=request.user if request.user.is_authenticated else None
    )
    
    return Response({
        'message': 'Song added to queue successfully',
        'queue_item': QueueItemSerializer(queue_item).data
    }, status=status.HTTP_201_CREATED)

def process_payment(payment_token, amount):
    """
    Placeholder function for Stripe payment processing
    Will be implemented when Stripe credentials are provided
    """
    # Mock payment success for development
    return True

@api_view(['POST'])
def next_song(request, venue_id):
    """
    Move to the next song in queue (for venue staff/admin use)
    """
    venue = get_object_or_404(Venue, id=venue_id)
    
    # Mark current song as played
    try:
        currently_playing = CurrentlyPlaying.objects.get(venue=venue)
        if currently_playing.queue_item:
            currently_playing.queue_item.status = 'played'
            currently_playing.queue_item.save()
    except CurrentlyPlaying.DoesNotExist:
        currently_playing = CurrentlyPlaying.objects.create(venue=venue)
    
    # Get next song from queue
    next_queue_item = QueueItem.objects.filter(
        venue=venue,
        status='queued'
    ).order_by('-is_paid', 'queued_at').first()
    
    if next_queue_item:
        next_queue_item.status = 'playing'
        next_queue_item.save()
        currently_playing.queue_item = next_queue_item
        currently_playing.save()
    else:
        currently_playing.queue_item = None
        currently_playing.save()
    
    return Response({
        'message': 'Moved to next song',
        'currently_playing': CurrentlyPlayingSerializer(currently_playing).data if next_queue_item else None
    })
