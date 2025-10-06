# api/utils.py
import os
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-read-private user-read-email playlist-read-private playlist-read-collaborative user-library-read"
    )