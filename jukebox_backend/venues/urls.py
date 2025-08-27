from django.urls import path
from .views import VenueListView, VenueDetailView, search_songs

urlpatterns = [
    path('venues/', VenueListView.as_view(), name='venue-list'),
    path('venues/<int:pk>/', VenueDetailView.as_view(), name='venue-detail'),
    path('songs/search/', search_songs, name='search-songs'),
]