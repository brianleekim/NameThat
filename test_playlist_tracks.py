#!/usr/bin/env python3
"""
Simple test for playlist_tracks function
"""

import requests
import json

def test_playlist_tracks():
    """Test getting tracks from a playlist"""
    print("🎵 Testing Playlist Tracks Function")
    print("=" * 50)
    
    # Step 1: Get your playlists
    print("1. First, get your playlists:")
    print("   Visit: http://127.0.0.1:8000/api/playlists/")
    print("   This will show you playlist IDs")
    
    # Step 2: Test with a specific playlist
    print("\n2. Then test with a playlist ID:")
    print("   Visit: http://127.0.0.1:8000/api/playlist/YOUR_PLAYLIST_ID/tracks/")
    print("   Replace YOUR_PLAYLIST_ID with an actual ID from step 1")
    
    print("\n3. Example:")
    print("   If your playlist ID is '37i9dQZF1DXcBWIGoYBM5M', visit:")
    print("   http://127.0.0.1:8000/api/playlist/37i9dQZF1DXcBWIGoYBM5M/tracks/")

def show_expected_response():
    """Show what the response should look like"""
    print("\n📋 Expected Response Format:")
    print("=" * 50)
    
    example_response = {
        "playlist": {
            "id": "37i9dQZF1DXcBWIGoYBM5M",
            "name": "Today's Top Hits",
            "description": "The hottest tracks right now.",
            "owner": "Spotify",
            "image": "https://i.scdn.co/image/..."
        },
        "tracks": [
            {
                "id": "4cOdK2wGLETKBW3PvgPWqT",
                "name": "Blinding Lights",
                "artists": "The Weeknd",
                "album": "After Hours",
                "album_image": "https://i.scdn.co/image/...",
                "preview_url": "https://p.scdn.co/mp3-preview/...",
                "duration_ms": 200040,
                "popularity": 95,
                "spotify_url": "https://open.spotify.com/track/...",
                "has_preview": True
            }
        ],
        "total_tracks": 50,
        "tracks_with_preview": 45,
        "tracks_without_preview": 5
    }
    
    print(json.dumps(example_response, indent=2))

def main():
    test_playlist_tracks()
    show_expected_response()
    
    print("\n" + "=" * 50)
    print("🎯 Steps to test:")
    print("1. Start your server: python manage.py runserver")
    print("2. Authenticate: Visit http://127.0.0.1:8000/api/login/")
    print("3. Get playlists: Visit http://127.0.0.1:8000/api/playlists/")
    print("4. Copy a playlist ID from the response")
    print("5. Test tracks: Visit http://127.0.0.1:8000/api/playlist/<ID>/tracks/")

if __name__ == "__main__":
    main() 