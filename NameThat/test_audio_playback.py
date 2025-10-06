#!/usr/bin/env python3
"""
Test script for audio playback functionality
"""

import requests
import json
import webbrowser
import time

# Base URL for your Django server
BASE_URL = "http://127.0.0.1:8000"

def test_audio_playback():
    """Test the new audio playback endpoints"""
    print("🎵 Testing Audio Playback Functionality")
    print("=" * 60)
    
    print("1. New API Endpoints Available:")
    print(f"   GET: {BASE_URL}/api/track/<track_id>/")
    print("   - Get a single track with preview URL")
    print(f"   GET: {BASE_URL}/api/playlist/<playlist_id>/random/")
    print("   - Get a random track from a playlist")
    print(f"   GET: {BASE_URL}/api/playlist/<playlist_id>/tracks/")
    print("   - Get all tracks from a playlist (enhanced)")
    
    print("\n2. Audio Player Demo:")
    print(f"   Visit: {BASE_URL}/static/audio_player.html")
    print("   - Interactive demo of audio playback")
    print("   - Select playlists and play tracks")
    print("   - Uses HTML5 audio element for playback")
    
    print("\n3. How Audio Playback Works:")
    print("   - Spotify provides 30-second preview URLs")
    print("   - These are direct MP3 links that can be played in browsers")
    print("   - Use HTML5 <audio> element or JavaScript Audio API")
    print("   - No need to redirect to Spotify app")
    
    print("\n4. Limitations:")
    print("   - Only 30-second previews available")
    print("   - Not all tracks have preview URLs")
    print("   - Cannot play full tracks (Spotify API limitation)")
    print("   - Cannot control playback beyond basic audio controls")

def show_code_examples():
    """Show code examples for audio playback"""
    print("\n💻 Code Examples")
    print("=" * 60)
    
    print("\n1. Get a track with preview URL:")
    print("""
import requests

# Get track details
track_id = "4cOdK2wGLETKBW3PvgPWqT"  # Example track ID
response = requests.get(f"{BASE_URL}/api/track/{track_id}/")
track = response.json()

if track['has_preview']:
    preview_url = track['preview_url']
    print(f"Track: {track['name']} by {track['artists']}")
    print(f"Preview URL: {preview_url}")
    print("You can play this URL in an HTML5 audio element")
else:
    print("No preview available for this track")
""")
    
    print("\n2. Get a random track from a playlist:")
    print("""
# Get random track from playlist
playlist_id = "37i9dQZF1DXcBWIGoYBM5M"
response = requests.get(f"{BASE_URL}/api/playlist/{playlist_id}/random/")
track = response.json()

print(f"Random track: {track['name']} by {track['artists']}")
print(f"Preview URL: {track['preview_url']}")
""")
    
    print("\n3. HTML5 Audio Element:")
    print("""
<audio controls>
    <source src="PREVIEW_URL_HERE" type="audio/mpeg">
    Your browser does not support the audio element.
</audio>
""")
    
    print("\n4. JavaScript Audio API:")
    print("""
const audio = new Audio('PREVIEW_URL_HERE');
audio.play();  // Start playback
audio.pause(); // Pause playback
audio.currentTime = 0; // Reset to beginning
""")

def show_spotify_api_info():
    """Show information about Spotify API limitations"""
    print("\n📚 Spotify API Information")
    print("=" * 60)
    
    print("\nWhat Spotify Web API provides:")
    print("✅ Track metadata (name, artist, album, etc.)")
    print("✅ 30-second preview URLs (MP3 format)")
    print("✅ Playlist access and management")
    print("✅ Audio features (tempo, key, energy, etc.)")
    print("✅ OAuth authentication")
    
    print("\nWhat Spotify Web API does NOT provide:")
    print("❌ Full track streaming")
    print("❌ Server-side audio control")
    print("❌ Direct audio manipulation")
    print("❌ Custom playback controls")
    print("❌ Audio file downloads")
    
    print("\nWhy these limitations exist:")
    print("• Spotify's terms of service protect their content")
    print("• Full streaming requires Spotify Premium and official clients")
    print("• Preview URLs are meant for discovery, not full playback")
    print("• This ensures artists get proper compensation")
    
    print("\nAlternative approaches:")
    print("• Use Spotify's embedded player (redirects to Spotify)")
    print("• Use Spotify Connect API (requires Premium)")
    print("• Use Spotify Web Playback SDK (limited control)")
    print("• Work with 30-second previews (current approach)")

def open_demo():
    """Open the audio player demo in browser"""
    demo_url = f"{BASE_URL}/static/audio_player.html"
    print(f"\n🌐 Opening demo in browser: {demo_url}")
    try:
        webbrowser.open(demo_url)
    except:
        print("Could not open browser automatically. Please visit the URL manually.")

def main():
    test_audio_playback()
    show_code_examples()
    show_spotify_api_info()
    
    print("\n" + "=" * 60)
    print("🎯 Next Steps:")
    print("1. Start your server: python manage.py runserver")
    print("2. Authenticate: Visit http://127.0.0.1:8000/api/login/")
    print("3. Test the demo: Visit http://127.0.0.1:8000/static/audio_player.html")
    print("4. Use the new endpoints in your application")
    
    # Ask if user wants to open the demo
    try:
        response = input("\nWould you like to open the audio player demo? (y/n): ")
        if response.lower() in ['y', 'yes']:
            open_demo()
    except KeyboardInterrupt:
        print("\nDemo not opened.")

if __name__ == "__main__":
    main() 