#!/usr/bin/env python3
"""
Setup checker for NameThat music guessing game
Run this script to verify your configuration is correct
"""

import os
import sys
from dotenv import load_dotenv

def check_env_variables():
    """Check if all required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    load_dotenv()
    
    required_vars = [
        'SPOTIFY_CLIENT_ID',
        'SPOTIFY_CLIENT_SECRET', 
        'SPOTIFY_REDIRECT_URI'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * len(value)} (length: {len(value)})")
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with these variables")
        return False
    
    print("✅ All environment variables are set")
    return True

def check_redirect_uri():
    """Check if redirect URI is properly formatted"""
    print("\n🔍 Checking redirect URI format...")
    
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    if not redirect_uri:
        print("❌ SPOTIFY_REDIRECT_URI not set")
        return False
    
    # Check if it's a valid localhost URI
    if not (redirect_uri.startswith('http://127.0.0.1:') or 
            redirect_uri.startswith('http://localhost:')):
        print(f"⚠️  Redirect URI should be localhost: {redirect_uri}")
        print("For local development, use: http://127.0.0.1:8000/api/callback/")
    
    if not redirect_uri.endswith('/api/callback/'):
        print(f"⚠️  Redirect URI should end with /api/callback/: {redirect_uri}")
    
    print(f"✅ Redirect URI: {redirect_uri}")
    return True

def check_django_setup():
    """Check if Django is properly configured"""
    print("\n🔍 Checking Django setup...")
    
    try:
        import django
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jukeguesser.settings')
        django.setup()
        
        print("✅ Django is properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Django setup error: {e}")
        return False

def check_spotify_imports():
    """Check if Spotify-related packages are installed"""
    print("\n🔍 Checking Spotify packages...")
    
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyOAuth
        print("✅ spotipy is installed")
        return True
    except ImportError as e:
        print(f"❌ Missing spotipy: {e}")
        print("Run: pip install spotipy")
        return False

def main():
    print("🎵 NameThat Setup Checker")
    print("=" * 40)
    
    checks = [
        check_env_variables,
        check_redirect_uri,
        check_spotify_imports,
        check_django_setup
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All checks passed! Your setup should work.")
        print("\nNext steps:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate") 
        print("3. Run: python manage.py runserver")
        print("4. Visit: http://127.0.0.1:8000/api/login/")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 