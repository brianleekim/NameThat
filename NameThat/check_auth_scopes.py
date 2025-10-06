#!/usr/bin/env python3
"""
Check OAuth scopes and permissions for Spotify API access
"""

import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def check_token_scopes():
    """Check what scopes the current token has"""
    print("🔍 Checking OAuth token scopes")
    print("=" * 60)
    
    try:
        with open('.cache', 'r') as f:
            cache_data = json.load(f)
        
        token = cache_data.get('access_token')
        if not token:
            print("❌ No access token found")
            return
        
        # Decode the JWT token to see scopes
        import base64
        
        # Split the token (JWT format: header.payload.signature)
        parts = token.split('.')
        if len(parts) == 3:
            # Decode the payload part
            payload = parts[1]
            # Add padding if needed
            payload += '=' * (4 - len(payload) % 4)
            
            try:
                decoded = base64.b64decode(payload).decode('utf-8')
                token_data = json.loads(decoded)
                
                print(f"✅ Token decoded successfully")
                print(f"📅 Expires at: {token_data.get('exp', 'Unknown')}")
                print(f"👤 User ID: {token_data.get('sub', 'Unknown')}")
                
                # Check for scopes
                if 'scope' in token_data:
                    scopes = token_data['scope'].split(' ')
                    print(f"🔑 Scopes: {scopes}")
                    
                    # Check for important scopes
                    important_scopes = [
                        'user-read-private',
                        'user-read-email',
                        'playlist-read-private',
                        'playlist-read-collaborative',
                        'user-library-read'
                    ]
                    
                    print(f"\n🔍 Checking important scopes:")
                    for scope in important_scopes:
                        if scope in scopes:
                            print(f"   ✅ {scope}")
                        else:
                            print(f"   ❌ {scope} (missing)")
                            
                else:
                    print(f"❌ No scopes found in token")
                    
            except Exception as e:
                print(f"❌ Error decoding token: {e}")
        else:
            print(f"❌ Token doesn't appear to be in JWT format")
            
    except Exception as e:
        print(f"❌ Error reading cache: {e}")

def test_api_access():
    """Test various API endpoints to see what we can access"""
    print(f"\n🔍 Testing API access")
    print("=" * 60)
    
    try:
        with open('.cache', 'r') as f:
            cache_data = json.load(f)
        
        token = cache_data.get('access_token')
        if not token:
            print("❌ No access token found")
            return
        
        headers = {
            'Authorization': f"Bearer {token}"
        }
        
        # Test user profile
        print("👤 Testing user profile access...")
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✅ User profile accessible")
            print(f"   📧 Email: {user_data.get('email', 'Not provided')}")
            print(f"   🌍 Country: {user_data.get('country', 'Not provided')}")
            print(f"   📅 Account type: {user_data.get('product', 'Unknown')}")
        else:
            print(f"   ❌ User profile error: {response.status_code}")
        
        # Test playlists access
        print(f"\n📋 Testing playlists access...")
        response = requests.get('https://api.spotify.com/v1/me/playlists?limit=1', headers=headers)
        if response.status_code == 200:
            print(f"   ✅ Playlists accessible")
        else:
            print(f"   ❌ Playlists error: {response.status_code}")
        
        # Test specific track access
        print(f"\n🎵 Testing track access...")
        track_id = '4cOdK2wGLETKBW3PvgPWqT'  # Blinding Lights
        response = requests.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=headers)
        if response.status_code == 200:
            track_data = response.json()
            print(f"   ✅ Track accessible: {track_data['name']}")
            print(f"   🎵 Preview URL: {track_data.get('preview_url', 'None')}")
        else:
            print(f"   ❌ Track error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")

def check_spotipy_auth():
    """Check if we can create a new Spotipy client with proper scopes"""
    print(f"\n🔍 Testing Spotipy authentication")
    print("=" * 60)
    
    try:
        # Try to create a new auth manager with all necessary scopes
        scope = "user-read-private user-read-email playlist-read-private playlist-read-collaborative user-library-read"
        
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=scope,
            cache_handler=spotipy.CacheFileHandler(cache_path='.cache_new')
        ))
        
        print(f"✅ Spotipy client created successfully")
        
        # Test user profile
        user = sp.current_user()
        print(f"👤 User: {user['display_name']}")
        print(f"🌍 Country: {user.get('country', 'Not provided')}")
        print(f"📅 Account type: {user.get('product', 'Unknown')}")
        
        # Test track access
        track = sp.track('4cOdK2wGLETKBW3PvgPWqT')  # Blinding Lights
        print(f"🎵 Track: {track['name']}")
        print(f"🎵 Preview URL: {track.get('preview_url', 'None')}")
        
        # Test playlist access
        playlists = sp.current_user_playlists(limit=1)
        if playlists['items']:
            playlist = playlists['items'][0]
            print(f"📋 Playlist: {playlist['name']}")
            
            # Get tracks from this playlist
            tracks = sp.playlist_tracks(playlist['id'], limit=1)
            if tracks['items']:
                track_item = tracks['items'][0]['track']
                print(f"🎵 First track: {track_item['name']}")
                print(f"🎵 Preview URL: {track_item.get('preview_url', 'None')}")
        
    except Exception as e:
        print(f"❌ Error with Spotipy: {e}")

def main():
    print("🎵 NameThat - OAuth Scope Check")
    print("=" * 60)
    
    check_token_scopes()
    test_api_access()
    check_spotipy_auth()
    
    print(f"\n" + "=" * 60)
    print("🎯 RECOMMENDATIONS")
    print("=" * 60)
    print("If preview URLs are still not available:")
    print("1. Try re-authenticating with all scopes")
    print("2. Check if your Spotify account has country info")
    print("3. Try using a different Spotify account")
    print("4. Check if you're using a free vs premium account")

if __name__ == "__main__":
    main() 