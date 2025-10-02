# NameThat - Music Guessing Game

A social music guessing game built with Django and the Spotify Web API. Players can import playlists from Spotify and compete to guess song names from 1-second previews.

## Features

- **Spotify Integration**: Import and play from your Spotify playlists
- **Game Sessions**: Track multiple game sessions with scoring
- **1-Second Previews**: Quick song previews for challenging gameplay
- **Score Tracking**: Monitor performance with detailed statistics
- **RESTful API**: Clean API endpoints for frontend integration

## Project Structure

```
NameThat/
├── api/                    # Main Django app
│   ├── models.py          # Database models (GameSession, GameRound, UserStats)
│   ├── views.py           # API endpoints and game logic
│   ├── urls.py            # URL routing
│   └── utils.py           # Spotify API utilities
├── jukeguesser/           # Django project settings
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── test_game_api.py       # API testing script
└── README.md              # This file
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root:
```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/api/callback/
```

### 3. Set Up Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Start the Server
```bash
python manage.py runserver
```

### 5. Test the API
```bash
python test_game_api.py
```

## Game Flow

1. **Authentication**: Visit `/api/login/` to authenticate with Spotify
2. **Select Playlist**: Use `/api/playlists/` to get your playlists
3. **Start Game**: POST to `/api/start_game/` with a playlist ID
4. **Play Rounds**: 
   - GET random track from `/api/round/`
   - Play 1-second preview
   - Submit guess to `/api/submit_guess/`
5. **View Stats**: Check performance at `/api/game_stats/<session_id>/`

## API Endpoints

### Authentication
- `GET /api/login/` - Start Spotify OAuth flow
- `GET /api/callback/` - Handle OAuth callback
- `GET /api/playlists/` - Get user's Spotify playlists

### Game Management
- `POST /api/start_game/` - Start a new game session
- `POST /api/round/` - Get a random track for guessing
- `POST /api/submit_guess/` - Submit a song guess
- `GET /api/game_stats/<session_id>/` - Get game statistics

## Example Usage

### Start a Game
```python
import requests

# Start a game with a playlist
response = requests.post('http://127.0.0.1:8000/api/start_game/', 
    json={'playlist_id': 'your_playlist_id'})
game_session = response.json()
session_id = game_session['game_session_id']
```

### Get a Random Track
```python
# Get a track for the current round
response = requests.post('http://127.0.0.1:8000/api/round/',
    json={'playlist_id': 'your_playlist_id'})
track_data = response.json()
preview_url = track_data['preview_url']
```

### Submit a Guess
```python
# Submit your guess
response = requests.post('http://127.0.0.1:8000/api/submit_guess/',
    json={
        'game_session_id': session_id,
        'track_id': track_data['track_id'],
        'guess': 'Song Name',
        'time_taken': 5.2
    })
result = response.json()
is_correct = result['is_correct']
```

## Database Models

### GameSession
- Tracks overall game progress
- Stores playlist information
- Calculates score percentages

### GameRound
- Individual round data
- User guesses and timing
- Correct/incorrect status

### UserStats (Future)
- Aggregate user statistics
- Best scores and averages
- Game history

## Development

### Adding New Features
1. **Models**: Add to `api/models.py`
2. **Views**: Create endpoints in `api/views.py`
3. **URLs**: Add routes in `api/urls.py`
4. **Migrations**: Run `python manage.py makemigrations`

### Testing
- Use `test_game_api.py` for API testing
- Check `check_setup.py` for configuration issues
- Run `python test_oauth.py` for OAuth debugging

## 📖 Spotify API Integration

This project uses the [Spotify Web API](https://developer.spotify.com/documentation/web-api/) for:
- Playlist access and track retrieval
- OAuth authentication
- Preview URL generation

Key endpoints used:
- `GET /playlists/{playlist_id}` - Get playlist details
- `GET /playlists/{playlist_id}/tracks` - Get playlist tracks
- `GET /tracks/{id}` - Get track information

## Frontend Integration

The API is designed to work with any frontend framework:
- **React**: Use fetch or axios for API calls
- **Vue.js**: Integrate with the REST endpoints
- **Plain JavaScript**: Simple HTTP requests
- **Mobile Apps**: RESTful API compatible

## Security

- OAuth 2.0 authentication with Spotify
- Session-based token management
- Input validation and sanitization
- Secure environment variable handling

## Deployment

### Production Setup
1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up proper CORS settings
4. Use environment variables for secrets
5. Configure static file serving

### Environment Variables
```env
SPOTIFY_CLIENT_ID=your_production_client_id
SPOTIFY_CLIENT_SECRET=your_production_client_secret
SPOTIFY_REDIRECT_URI=https://yourdomain.com/api/callback/
SECRET_KEY=your_django_secret_key
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Acknowledgments

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) for music data
- [Django REST Framework](https://www.django-rest-framework.org/) for API development
- [Spotipy](https://spotipy.readthedocs.io/) for Spotify API integration
