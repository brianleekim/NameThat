#!/usr/bin/env python3
"""
Re-authenticate with Spotify using proper settings
"""

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

def main():
    print("🎵 NameThat - Spotify Re-authentication")
    print("=" * 60)
    
    # Set environment variables
    os.environ['SPOTIFY_CLIENT_ID'] = '6a66b9a319ad4baba3bf7b2309af5739'
    os.environ['SPOTIFY_CLIENT_SECRET'] = '6259770824434e45b1ac6a47f879e654'
    os.environ['SPOTIFY_REDIRECT_URI'] = 'http://localhost:8000/api/callback/'
    
    print("🔧 Environment variables set:")
    print(f"   Client ID: {os.environ['SPOTIFY_CLIENT_ID']}")
    print(f"   Redirect URI: {os.environ['SPOTIFY_REDIRECT_URI']}")
    
    try:
        # Create OAuth manager with all necessary scopes
        scope = "user-read-private user-read-email playlist-read-private playlist-read-collaborative user-library-read"
        
        sp_oauth = SpotifyOAuth(
            client_id=os.environ['SPOTIFY_CLIENT_ID'],
            client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
            redirect_uri=os.environ['SPOTIFY_REDIRECT_URI'],
            scope=scope,
            cache_handler=spotipy.CacheFileHandler(cache_path='.cache_new')
        )
        
        print(f"✅ OAuth manager created with scopes: {scope}")
        
        # Check if we have a cached token
        token_info = sp_oauth.get_cached_token()
        
        if token_info:
            print(f"✅ Found cached token")
            
            # Check if token is expired
            if sp_oauth.is_token_expired(token_info):
                print(f"⚠️  Token is expired, refreshing...")
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                print(f"✅ Token refreshed")
            else:
                print(f"✅ Token is still valid")
                
            # Test the token
            sp = spotipy.Spotify(auth=token_info['access_token'])
            
            # Get user profile
            user = sp.current_user()
            print(f"👤 User: {user['display_name']}")
            print(f"🌍 Country: {user.get('country', 'Not provided')}")
            print(f"📅 Account type: {user.get('product', 'Unknown')}")
            
            # Test track access
            track = sp.track('4cOdK2wGLETKBW3PvgPWqT')  # Blinding Lights
            print(f"🎵 Test track: {track['name']}")
            print(f"🎵 Preview URL: {track.get('preview_url', 'None')}")
            
            # Test playlist access
            playlists = sp.current_user_playlists(limit=1)
            if playlists['items']:
                playlist = playlists['items'][0]
                print(f"📋 Test playlist: {playlist['name']}")
                
                # Get tracks from this playlist
                tracks = sp.playlist_tracks(playlist['id'], limit=1)
                if tracks['items']:
                    track_item = tracks['items'][0]['track']
                    print(f"🎵 First track: {track_item['name']}")
                    print(f"🎵 Preview URL: {track_item.get('preview_url', 'None')}")
            
            print(f"\n✅ Authentication successful!")
            print(f"💾 Token saved to .cache_new")
            
        else:
            print(f"❌ No cached token found")
            print(f"🔗 Please authenticate via the Django app:")
            print(f"   1. Start Django server: python manage.py runserver")
            print(f"   2. Visit: http://localhost:8000/api/login/")
            print(f"   3. Complete Spotify OAuth")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\n💡 Make sure to add SPOTIFY_REDIRECT_URI to your .env file:")
        print(f"   SPOTIFY_REDIRECT_URI=http://localhost:8000/api/callback/")

if __name__ == "__main__":
    main() 