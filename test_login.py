#!/usr/bin/env python3
"""
Test the login endpoint to ensure OAuth flow works
"""

import os
import django
from dotenv import load_dotenv

def test_login_endpoint():
    """Test if the login endpoint can generate a proper OAuth URL"""
    print("🔍 Testing Login Endpoint")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jukeguesser.settings')
    django.setup()
    
    try:
        from api.views import login
        from django.test import RequestFactory
        from django.http import HttpResponseRedirect
        
        # Create a mock request
        factory = RequestFactory()
        request = factory.get('/api/login/')
        
        # Call the login view
        response = login(request)
        
        # Check if it's a redirect (which it should be)
        if isinstance(response, HttpResponseRedirect):
            print(f"✅ Login endpoint working!")
            print(f"Redirect URL: {response.url}")
            
            # Check if it's a Spotify authorization URL
            if 'accounts.spotify.com' in response.url and 'authorize' in response.url:
                print("✅ Redirecting to Spotify authorization page")
                return True
            else:
                print("⚠️  Not redirecting to Spotify as expected")
                return False
        else:
            print(f"❌ Login endpoint not redirecting: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Login endpoint test failed: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\n🔍 Testing Environment Variables")
    print("=" * 50)
    
    load_dotenv()
    
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    
    print(f"Client ID: {'*' * len(client_id) if client_id else 'NOT SET'}")
    print(f"Client Secret: {'*' * len(client_secret) if client_secret else 'NOT SET'}")
    print(f"Redirect URI: {redirect_uri or 'NOT SET'}")
    
    if all([client_id, client_secret, redirect_uri]):
        print("✅ All environment variables are set")
        return True
    else:
        print("❌ Missing environment variables")
        return False

def main():
    print("🎵 Login Endpoint Test")
    print("=" * 50)
    
    env_ok = test_environment()
    login_ok = test_login_endpoint()
    
    print("\n" + "=" * 50)
    if env_ok and login_ok:
        print("🎉 Login endpoint should work!")
        print("\nNext steps:")
        print("1. Make sure server is running: python manage.py runserver 8080")
        print("2. Visit: http://127.0.0.1:8080/api/login/")
        print("3. You should be redirected to Spotify for authorization")
    else:
        print("❌ Issues found. Check the errors above.")
        
        if not env_ok:
            print("\n💡 Environment Issues:")
            print("- Check your .env file")
            print("- Make sure all variables are set correctly")
            
        if not login_ok:
            print("\n💡 Login Issues:")
            print("- Check Spotify app configuration")
            print("- Verify redirect URI matches exactly")
            print("- Make sure server is running on correct port")

if __name__ == "__main__":
    main() 