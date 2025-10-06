#!/usr/bin/env python3
"""
Debug script to troubleshoot audio playback issues
"""

import requests
import json
import webbrowser
import time

BASE_URL = "http://127.0.0.1:8000"

def check_server():
    """Check if the server is running"""
    print("🔍 Step 1: Checking if server is running...")
    try:
        response = requests.get(f"{BASE_URL}/api/playlists/", timeout=5)
        if response.status_code == 401:
            print("✅ Server is running, but not authenticated")
            return True
        elif response.status_code == 200:
            print("✅ Server is running and authenticated!")
            return True
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start it with: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False

def check_authentication():
    """Check authentication status"""
    print("\n🔍 Step 2: Checking authentication...")
    try:
        response = requests.get(f"{BASE_URL}/api/playlists/")
        if response.status_code == 401:
            print("❌ Not authenticated")
            print("   You need to authenticate with Spotify first")
            return False
        elif response.status_code == 200:
            print("✅ Already authenticated!")
            return True
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking authentication: {e}")
        return False

def guide_authentication():
    """Guide user through authentication"""
    print("\n🔍 Step 3: Authentication Guide")
    print("=" * 50)
    print("To authenticate with Spotify:")
    print("1. Open your browser")
    print("2. Go to: http://127.0.0.1:8000/api/login/")
    print("3. You'll be redirected to Spotify")
    print("4. Click 'Agree' to authorize the app")
    print("5. You'll be redirected back to your app")
    print("6. Come back here and run this script again")
    
    try:
        response = input("\nWould you like to open the login page now? (y/n): ")
        if response.lower() in ['y', 'yes']:
            print("🌐 Opening login page...")
            webbrowser.open(f"{BASE_URL}/api/login/")
    except KeyboardInterrupt:
        print("\nLogin page not opened.")

def test_playlist_access():
    """Test accessing playlists after authentication"""
    print("\n🔍 Step 4: Testing playlist access...")
    try:
        response = requests.get(f"{BASE_URL}/api/playlists/")
        if response.status_code == 200:
            playlists = response.json()
            print(f"✅ Successfully accessed {len(playlists)} playlists")
            
            if playlists:
                print("\nYour playlists:")
                for i, playlist in enumerate(playlists[:5]):
                    print(f"   {i+1}. {playlist['name']} (ID: {playlist['id']})")
                
                if len(playlists) > 5:
                    print(f"   ... and {len(playlists) - 5} more")
                
                return playlists[0]['id']  # Return first playlist ID
            else:
                print("❌ No playlists found")
                return None
        else:
            print(f"❌ Failed to access playlists: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error accessing playlists: {e}")
        return None

def test_track_access(playlist_id):
    """Test accessing tracks from a playlist"""
    print(f"\n🔍 Step 5: Testing track access for playlist {playlist_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/playlist/{playlist_id}/tracks/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Successfully accessed {len(data['tracks'])} tracks")
            print(f"   Tracks with preview: {data['tracks_with_preview']}")
            print(f"   Tracks without preview: {data['tracks_without_preview']}")
            
            # Find a track with preview
            tracks_with_preview = [t for t in data['tracks'] if t['has_preview']]
            if tracks_with_preview:
                track = tracks_with_preview[0]
                print(f"\n✅ Found track with preview:")
                print(f"   Name: {track['name']}")
                print(f"   Artist: {track['artists']}")
                print(f"   Preview URL: {track['preview_url']}")
                return track
            else:
                print("❌ No tracks with preview found in this playlist")
                return None
        else:
            print(f"❌ Failed to access tracks: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error accessing tracks: {e}")
        return None

def test_audio_playback(track):
    """Test audio playback functionality"""
    print(f"\n🔍 Step 6: Testing audio playback...")
    if not track:
        print("❌ No track to test")
        return
    
    print(f"🎵 Testing playback for: {track['name']}")
    print(f"   Preview URL: {track['preview_url']}")
    
    # Test if the preview URL is accessible
    try:
        response = requests.head(track['preview_url'], timeout=10)
        if response.status_code == 200:
            print("✅ Preview URL is accessible")
            print("   You can play this track in your browser")
        else:
            print(f"❌ Preview URL returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing preview URL: {e}")
    
    print(f"\n🌐 To test audio playback:")
    print(f"1. Visit: {BASE_URL}/static/audio_player.html")
    print(f"2. Select a playlist")
    print(f"3. Click 'Load Tracks'")
    print(f"4. Click 'Play Current Track'")

def main():
    print("🎵 NameThat Audio Debug Script")
    print("=" * 50)
    
    # Step 1: Check server
    if not check_server():
        return
    
    # Step 2: Check authentication
    if not check_authentication():
        guide_authentication()
        return
    
    # Step 3: Test playlist access
    playlist_id = test_playlist_access()
    if not playlist_id:
        return
    
    # Step 4: Test track access
    track = test_track_access(playlist_id)
    
    # Step 5: Test audio playback
    test_audio_playback(track)
    
    print("\n" + "=" * 50)
    print("🎯 Summary:")
    print("✅ Server is running")
    print("✅ Authentication is working")
    print("✅ Playlist access is working")
    if track:
        print("✅ Track access is working")
        print("✅ Audio playback should work")
    else:
        print("❌ No tracks with preview found")
    
    print(f"\n🌐 Interactive Demo: {BASE_URL}/static/audio_player.html")

if __name__ == "__main__":
    main() 