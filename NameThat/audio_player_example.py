#!/usr/bin/env python3
"""
Example script showing how to use the audio playback functionality
"""

import requests
import json
import time

# Base URL for your Django server
BASE_URL = "http://127.0.0.1:8000"

def get_playlists():
    """Get user's playlists"""
    try:
        response = requests.get(f"{BASE_URL}/api/playlists/")
        if response.status_code == 401:
            print("❌ Not authenticated. Please visit http://127.0.0.1:8000/api/login/ first")
            return None
        
        playlists = response.json()
        print(f"✅ Found {len(playlists)} playlists")
        return playlists
    except Exception as e:
        print(f"❌ Error getting playlists: {e}")
        return None

def get_playlist_tracks(playlist_id):
    """Get all tracks from a playlist"""
    try:
        response = requests.get(f"{BASE_URL}/api/playlist/{playlist_id}/tracks/")
        data = response.json()
        
        print(f"✅ Playlist: {data['playlist']['name']}")
        print(f"   Total tracks: {data['total_tracks']}")
        print(f"   Tracks with preview: {data['tracks_with_preview']}")
        print(f"   Tracks without preview: {data['tracks_without_preview']}")
        
        return data
    except Exception as e:
        print(f"❌ Error getting playlist tracks: {e}")
        return None

def get_random_track(playlist_id):
    """Get a random track from a playlist"""
    try:
        response = requests.get(f"{BASE_URL}/api/playlist/{playlist_id}/random/")
        track = response.json()
        
        print(f"🎵 Random track: {track['name']} by {track['artists']}")
        print(f"   Album: {track['album']}")
        print(f"   Duration: {format_duration(track['duration_ms'])}")
        print(f"   Preview URL: {track['preview_url']}")
        
        return track
    except Exception as e:
        print(f"❌ Error getting random track: {e}")
        return None

def get_track_details(track_id):
    """Get detailed information about a specific track"""
    try:
        response = requests.get(f"{BASE_URL}/api/track/{track_id}/")
        track = response.json()
        
        print(f"🎵 Track: {track['name']} by {track['artists']}")
        print(f"   Album: {track['album']}")
        print(f"   Duration: {format_duration(track['duration_ms'])}")
        print(f"   Popularity: {track['popularity']}/100")
        print(f"   Has preview: {track['has_preview']}")
        
        if track['has_preview']:
            print(f"   Preview URL: {track['preview_url']}")
        
        if track.get('audio_features'):
            features = track['audio_features']
            print(f"   Audio features:")
            print(f"     Tempo: {features.get('tempo', 'N/A')} BPM")
            print(f"     Energy: {features.get('energy', 'N/A')}")
            print(f"     Danceability: {features.get('danceability', 'N/A')}")
            print(f"     Valence: {features.get('valence', 'N/A')}")
        
        return track
    except Exception as e:
        print(f"❌ Error getting track details: {e}")
        return None

def format_duration(ms):
    """Format duration from milliseconds to MM:SS"""
    minutes = int(ms // 60000)
    seconds = int((ms % 60000) // 1000)
    return f"{minutes}:{seconds:02d}"

def create_html_audio_player(track):
    """Create HTML code for an audio player"""
    if not track['has_preview']:
        return None
    
    html = f"""
<div class="audio-player">
    <h3>{track['name']} by {track['artists']}</h3>
    <audio controls>
        <source src="{track['preview_url']}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    <p>Duration: {format_duration(track['duration_ms'])}</p>
    <p>Album: {track['album']}</p>
</div>
"""
    return html

def main():
    print("🎵 NameThat Audio Player Example")
    print("=" * 50)
    
    # Step 1: Get playlists
    print("\n1. Getting your playlists...")
    playlists = get_playlists()
    if not playlists:
        return
    
    # Show first few playlists
    print("\nYour playlists:")
    for i, playlist in enumerate(playlists[:5]):
        print(f"   {i+1}. {playlist['name']} (ID: {playlist['id']})")
    
    if len(playlists) > 5:
        print(f"   ... and {len(playlists) - 5} more")
    
    # Step 2: Get tracks from first playlist
    if playlists:
        first_playlist = playlists[0]
        print(f"\n2. Getting tracks from '{first_playlist['name']}'...")
        playlist_data = get_playlist_tracks(first_playlist['id'])
        
        if playlist_data and playlist_data['tracks']:
            # Show first few tracks
            print(f"\nFirst few tracks:")
            for i, track in enumerate(playlist_data['tracks'][:3]):
                preview_status = "✅" if track['has_preview'] else "❌"
                print(f"   {i+1}. {track['name']} by {track['artists']} {preview_status}")
    
    # Step 3: Get a random track
    if playlists:
        print(f"\n3. Getting a random track from '{first_playlist['name']}'...")
        random_track = get_random_track(first_playlist['id'])
        
        if random_track and random_track['has_preview']:
            # Create HTML audio player code
            html_code = create_html_audio_player(random_track)
            print(f"\n4. HTML Audio Player Code:")
            print(html_code)
            
            print(f"\n5. JavaScript Audio API Example:")
            js_code = f"""
const audio = new Audio('{random_track['preview_url']}');
audio.play();  // Start playback
audio.pause(); // Pause playback
audio.currentTime = 0; // Reset to beginning
"""
            print(js_code)
    
    # Step 4: Get detailed track info
    if playlists and playlist_data and playlist_data['tracks']:
        # Get first track with preview
        track_with_preview = next((t for t in playlist_data['tracks'] if t['has_preview']), None)
        if track_with_preview:
            print(f"\n6. Getting detailed info for '{track_with_preview['name']}'...")
            get_track_details(track_with_preview['id'])
    
    print("\n" + "=" * 50)
    print("🎯 How to use this in your application:")
    print("1. Use the HTML5 <audio> element for simple playback")
    print("2. Use JavaScript Audio API for programmatic control")
    print("3. The preview URLs are direct MP3 links from Spotify")
    print("4. Only 30-second previews are available (Spotify limitation)")
    print("5. Not all tracks have preview URLs available")
    
    print(f"\n🌐 Interactive Demo: http://127.0.0.1:8000/static/audio_player.html")

if __name__ == "__main__":
    main() 