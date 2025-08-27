from django.urls import path
from .views import venue_queue, add_to_queue, next_song

urlpatterns = [
    path('venues/<int:venue_id>/queue/', venue_queue, name='venue-queue'),
    path('venues/<int:venue_id>/queue/add/', add_to_queue, name='add-to-queue'),
    path('venues/<int:venue_id>/next/', next_song, name='next-song'),
]