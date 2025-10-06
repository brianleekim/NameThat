#!/usr/bin/env python3
"""
Test authentication status and debug session issues
"""

import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000"

def test_with_session():
    """Test API calls with session cookies"""
    print("🔍 Testing authentication with session...")
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # First, try to get playlists
    try:
        response = session.get(f"{BASE_URL}/api/playlists/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        if response.status_code == 200:
            print("✅ Successfully authenticated!")
            return True
        else:
            print("❌ Not authenticated")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_direct_login():
    """Test the login endpoint directly"""
    print("\n🔍 Testing login endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/login/", allow_redirects=False)
        print(f"Login Status Code: {response.status_code}")
        
        if response.status_code == 302:  # Redirect
            print("✅ Login endpoint is working (redirecting to Spotify)")
            print(f"Redirect URL: {response.headers.get('Location', 'Unknown')}")
        else:
            print(f"❌ Unexpected response from login endpoint")
            
    except Exception as e:
        print(f"❌ Error testing login: {e}")

def check_cache_file():
    """Check if the cache file exists and is valid"""
    print("\n🔍 Checking cache file...")
    
    cache_file = ".cache"
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            print("✅ Cache file exists")
            print(f"   Token type: {cache_data.get('token_type', 'Unknown')}")
            print(f"   Expires at: {cache_data.get('expires_at', 'Unknown')}")
            print(f"   Has refresh token: {'Yes' if cache_data.get('refresh_token') else 'No'}")
            
            # Check if token is expired
            import time
            current_time = int(time.time())
            expires_at = cache_data.get('expires_at', 0)
            
            if expires_at > current_time:
                print(f"   ✅ Token is still valid (expires in {expires_at - current_time} seconds)")
            else:
                print(f"   ❌ Token has expired")
                
        except Exception as e:
            print(f"❌ Error reading cache file: {e}")
    else:
        print("❌ Cache file does not exist")

def test_spotify_api_directly():
    """Test Spotify API directly using the cached token"""
    print("\n🔍 Testing Spotify API directly...")
    
    try:
        with open('.cache', 'r') as f:
            cache_data = json.load(f)
        
        access_token = cache_data.get('access_token')
        if not access_token:
            print("❌ No access token in cache")
            return False
        
        # Test Spotify API directly
        headers = {
            'Authorization': f"Bearer {access_token}"
        }
        
        response = requests.get(
            'https://api.spotify.com/v1/me/playlists',
            headers=headers
        )
        
        print(f"Spotify API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Spotify API working! Found {len(data.get('items', []))} playlists")
            return True
        elif response.status_code == 401:
            print("❌ Spotify token is invalid or expired")
            return False
        else:
            print(f"❌ Spotify API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Spotify API: {e}")
        return False

def main():
    print("🎵 NameThat - Authentication Debug")
    print("=" * 50)
    
    # Check cache file
    check_cache_file()
    
    # Test Spotify API directly
    spotify_working = test_spotify_api_directly()
    
    # Test Django session
    django_working = test_with_session()
    
    # Test login endpoint
    test_direct_login()
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSIS")
    print("=" * 50)
    
    if spotify_working and not django_working:
        print("🔍 ISSUE: Spotify token is valid, but Django session is not working")
        print("\n💡 SOLUTIONS:")
        print("1. Clear your browser cookies for 127.0.0.1:8000")
        print("2. Try visiting http://127.0.0.1:8000/api/login/ again")
        print("3. Make sure you're using the same browser session")
        print("4. Check if your browser blocks cookies")
        
    elif not spotify_working:
        print("🔍 ISSUE: Spotify token is invalid or expired")
        print("\n💡 SOLUTIONS:")
        print("1. Delete the .cache file")
        print("2. Visit http://127.0.0.1:8000/api/login/ to re-authenticate")
        
    elif django_working:
        print("✅ Everything is working! You should be able to use the audio player.")
        
    else:
        print("🔍 ISSUE: Multiple problems detected")
        print("\n💡 SOLUTIONS:")
        print("1. Restart the Django server")
        print("2. Clear browser cookies")
        print("3. Re-authenticate with Spotify")

if __name__ == "__main__":
    main() 