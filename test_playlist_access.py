#!/usr/bin/env python3
"""
Test script for playlist and track access endpoints
"""

import requests
import json

# Base URL for your Django server
BASE_URL = "http://127.0.0.1:8000"

def test_playlist_access():
    """Test the new playlist access endpoints"""
    print("🎵 Testing Playlist and Track Access")
    print("=" * 50)
    
    print("1. Get your playlists first:")
    print(f"   GET: {BASE_URL}/api/playlists/")
    print("   (This will return your playlist IDs)")
    
    print("\n2. Get all tracks from a specific playlist:")
    print(f"   GET: {BASE_URL}/api/playlist/YOUR_PLAYLIST_ID/tracks/")
    print("   (Replace YOUR_PLAYLIST_ID with an actual playlist ID)")
    
    print("\n3. Search for tracks:")
    print(f"   GET: {BASE_URL}/api/search/?q=your_search_query")
    print("   (Replace 'your_search_query' with what you want to search for)")
    
    print("\n4. Get your saved/liked tracks:")
    print(f"   GET: {BASE_URL}/api/saved_tracks/")
    print("   (This returns your liked songs)")

def show_example_responses():
    """Show example responses from the new endpoints"""
    print("\n📋 Example API Responses")
    print("=" * 50)
    
    print("\n1. Playlist Tracks Response:")
    playlist_example = {
        "playlist": {
            "id": "37i9dQZF1DXcBWIGoYBM5M",
            "name": "Today's Top Hits",
            "description": "The hottest tracks right now.",
            "owner": "Spotify",
            "image": "https://i.scdn.co/image/ab67706f00000002724554ed6bed6f051d9b0bfc"
        },
        "tracks": [
            {
                "id": "4cOdK2wGLETKBW3PvgPWqT",
                "name": "Blinding Lights",
                "artists": "The Weeknd",
                "album": "After Hours",
                "album_image": "https://i.scdn.co/image/ab67616d0000b2738863bc11d2aa12b54f5aeb36",
                "preview_url": "https://p.scdn.co/mp3-preview/...",
                "duration_ms": 200040,
                "popularity": 95,
                "spotify_url": "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT",
                "has_preview": True
            }
        ],
        "total_tracks": 50,
        "tracks_with_preview": 45,
        "tracks_without_preview": 5
    }
    print(json.dumps(playlist_example, indent=2))
    
    print("\n2. Search Response:")
    search_example = {
        "query": "Blinding Lights",
        "tracks": [
            {
                "id": "4cOdK2wGLETKBW3PvgPWqT",
                "name": "Blinding Lights",
                "artists": "The Weeknd",
                "album": "After Hours",
                "album_image": "https://i.scdn.co/image/ab67616d0000b2738863bc11d2aa12b54f5aeb36",
                "preview_url": "https://p.scdn.co/mp3-preview/...",
                "duration_ms": 200040,
                "popularity": 95,
                "spotify_url": "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT",
                "has_preview": True
            }
        ],
        "total_found": 1000,
        "tracks_with_preview": 15
    }
    print(json.dumps(search_example, indent=2))

def show_usage_examples():
    """Show how to use the endpoints in code"""
    print("\n💻 Usage Examples")
    print("=" * 50)
    
    print("\n1. Get all tracks from a playlist:")
    print("""
import requests

# Get playlist tracks
playlist_id = "37i9dQZF1DXcBWIGoYBM5M"
response = requests.get(f"{BASE_URL}/api/playlist/{playlist_id}/tracks/")
playlist_data = response.json()

print(f"Playlist: {playlist_data['playlist']['name']}")
print(f"Total tracks: {playlist_data['total_tracks']}")
print(f"Tracks with preview: {playlist_data['tracks_with_preview']}")

for track in playlist_data['tracks']:
    print(f"- {track['name']} by {track['artists']}")
    if track['has_preview']:
        print(f"  Preview: {track['preview_url']}")
""")
    
    print("\n2. Search for tracks:")
    print("""
# Search for tracks
query = "Blinding Lights"
response = requests.get(f"{BASE_URL}/api/search/?q={query}")
search_data = response.json()

print(f"Found {search_data['total_found']} tracks for '{query}'")
for track in search_data['tracks']:
    print(f"- {track['name']} by {track['artists']}")
""")
    
    print("\n3. Get saved tracks:")
    print("""
# Get saved tracks
response = requests.get(f"{BASE_URL}/api/saved_tracks/")
saved_data = response.json()

print(f"You have {saved_data['total_saved']} saved tracks")
for track in saved_data['tracks']:
    print(f"- {track['name']} by {track['artists']}")
""")

def main():
    test_playlist_access()
    show_example_responses()
    show_usage_examples()
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Start your server: python manage.py runserver")
    print("2. Authenticate: Visit http://127.0.0.1:8000/api/login/")
    print("3. Get your playlists: GET /api/playlists/")
    print("4. Get playlist tracks: GET /api/playlist/<id>/tracks/")
    print("5. Search tracks: GET /api/search/?q=your_query")
    print("6. Get saved tracks: GET /api/saved_tracks/")

if __name__ == "__main__":
    main() 