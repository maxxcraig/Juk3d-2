# Digital Jukebox Platform

A digital music queue platform built with React Native (Expo) and Django REST Framework. Users can select venues, view current playing music, and add songs to the queue either for free or by paying $1 (paid songs get priority).

## Features

- **Venue Selection**: Choose from L&L Hawaiian BBQ, Chipotle, or Trujillos
- **Queue Management**: View current song and next 10 songs in queue
- **Priority System**: Paid songs ($1) jump ahead of free songs
- **Authentication**: Firebase Auth integration (ready for credentials)
- **Payments**: Stripe integration (ready for credentials)
- **Music API**: Ready for integration with music streaming service

## Project Structure

```
Juk3d/
├── JukeboxApp/          # React Native (Expo) frontend
├── jukebox_backend/     # Django REST API
├── venv/               # Python virtual environment
└── README.md
```

## Setup Instructions

### Backend (Django)

1. **Activate virtual environment:**
   ```bash
   cd Juk3d
   source venv/bin/activate
   ```

2. **Navigate to backend and run migrations:**
   ```bash
   cd jukebox_backend
   python manage.py migrate
   python manage.py seed_venues
   ```

3. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

   Backend will be available at `http://localhost:8000`

### Frontend (React Native)

1. **Navigate to app directory:**
   ```bash
   cd JukeboxApp
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start Expo:**
   ```bash
   npm start
   ```

   Then:
   - Press `i` for iOS simulator
   - Press `a` for Android emulator  
   - Scan QR code with Expo Go app on your phone

## API Endpoints

### Venues
- `GET /api/venues/` - List all venues
- `GET /api/venues/{id}/` - Get venue details

### Music Queue
- `GET /api/venues/{venue_id}/queue/` - Get current song and queue for venue
- `POST /api/venues/{venue_id}/queue/add/` - Add song to queue
- `POST /api/venues/{venue_id}/next/` - Move to next song (admin)

### Search
- `GET /api/songs/search/?q={query}` - Search for songs (currently returns mock data)

## Integration Placeholders

The following integrations are ready and waiting for credentials:

### Firebase Authentication
- Login/signup screens built
- Replace placeholder in `LoginScreen.tsx` when Firebase config is available

### Stripe Payments
- Payment flow implemented
- Add Stripe keys to Django `settings.py`:
  - `STRIPE_PUBLISHABLE_KEY`
  - `STRIPE_SECRET_KEY`

### Music API
- Song search endpoint ready
- Replace mock data in `venues/views.py` when music API is available
- Update `MUSIC_API_BASE_URL` and `MUSIC_API_KEY` in `settings.py`

## Development Notes

- Backend uses SQLite for development (easily switchable to PostgreSQL)
- CORS is configured for React Native development
- All API endpoints return JSON
- Queue automatically sorts paid songs before free songs
- Mock data is used until real integrations are added

## Next Steps

1. Add Firebase configuration
2. Add Stripe API keys
3. Integrate with music streaming API (Spotify, Apple Music, etc.)
4. Add user authentication to React Native app
5. Connect frontend to Django backend
6. Test payment flow
7. Deploy to production

## Testing

The app can be tested without any external API keys:
- Use "Continue as Demo User" to bypass auth
- Mock songs are available for testing queue functionality
- Payment flow shows placeholder messages