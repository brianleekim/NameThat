#!/usr/bin/env python3
"""
Simple OAuth test script to debug Spotify login issues
"""

import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

def test_oauth_setup():
    """Test the OAuth configuration"""
    print("🔍 Testing Spotify OAuth Configuration")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check environment variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    
    print(f"Client ID: {'*' * len(client_id) if client_id else 'NOT SET'}")
    print(f"Client Secret: {'*' * len(client_secret) if client_secret else 'NOT SET'}")
    print(f"Redirect URI: {redirect_uri or 'NOT SET'}")
    
    if not all([client_id, client_secret, redirect_uri]):
        print("❌ Missing environment variables!")
        return False
    
    try:
        # Create OAuth object
        oauth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-read-private"
        )
        
        # Generate authorization URL
        auth_url = oauth.get_authorize_url()
        print(f"\n✅ OAuth setup successful!")
        print(f"Authorization URL: {auth_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ OAuth setup failed: {e}")
        return False

def test_django_imports():
    """Test if Django can import the OAuth utilities"""
    print("\n🔍 Testing Django OAuth imports")
    print("=" * 50)
    
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jukeguesser.settings')
        django.setup()
        
        from api.utils import get_spotify_oauth
        oauth = get_spotify_oauth()
        
        auth_url = oauth.get_authorize_url()
        print(f"✅ Django OAuth import successful!")
        print(f"Authorization URL: {auth_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django OAuth import failed: {e}")
        return False

def main():
    print("🎵 Spotify OAuth Debug Tool")
    print("=" * 50)
    
    # Test basic OAuth
    oauth_ok = test_oauth_setup()
    
    # Test Django integration
    django_ok = test_django_imports()
    
    print("\n" + "=" * 50)
    if oauth_ok and django_ok:
        print("🎉 All tests passed! OAuth should work.")
        print("\nNext steps:")
        print("1. Make sure server is running on correct port")
        print("2. Visit the login URL in your browser")
        print("3. Check browser console for any errors")
    else:
        print("❌ Some tests failed. Check the errors above.")
        
        if not oauth_ok:
            print("\n💡 OAuth Issues:")
            print("- Check your .env file")
            print("- Verify Spotify app settings")
            print("- Make sure redirect URI matches exactly")
            
        if not django_ok:
            print("\n💡 Django Issues:")
            print("- Run: pip install -r requirements.txt")
            print("- Check Django settings")
            print("- Make sure all dependencies are installed")

if __name__ == "__main__":
    main() 