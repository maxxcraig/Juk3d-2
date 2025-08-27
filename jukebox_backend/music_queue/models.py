from django.db import models
from django.contrib.auth.models import User
from venues.models import Venue, Song

class QueueItem(models.Model):
    QUEUE_STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('playing', 'Playing'),
        ('played', 'Played'),
        ('skipped', 'Skipped'),
    ]
    
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=QUEUE_STATUS_CHOICES, default='queued')
    queued_at = models.DateTimeField(auto_now_add=True)
    played_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-is_paid', 'queued_at']  # Paid songs first, then by time
    
    def __str__(self):
        return f"{self.song.title} at {self.venue.name} ({'Paid' if self.is_paid else 'Free'})"

class CurrentlyPlaying(models.Model):
    venue = models.OneToOneField(Venue, on_delete=models.CASCADE)
    queue_item = models.ForeignKey(QueueItem, on_delete=models.CASCADE, null=True, blank=True)
    started_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.queue_item:
            return f"Playing {self.queue_item.song.title} at {self.venue.name}"
        return f"Nothing playing at {self.venue.name}"
