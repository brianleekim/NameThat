#!/usr/bin/env python3
"""
Test preview URLs using Spotify's official documentation examples
Based on Spotify Web API documentation
"""

import requests
import json
import os

def get_cached_token():
    """Get the cached Spotify token"""
    try:
        with open('.cache', 'r') as f:
            cache_data = json.load(f)
        return cache_data.get('access_token')
    except:
        return None

def test_spotify_documentation_examples():
    """Test tracks that should definitely have preview URLs according to Spotify docs"""
    print("🎵 Testing Spotify Documentation Examples")
    print("=" * 60)
    
    token = get_cached_token()
    if not token:
        print("❌ No cached token found")
        return
    
    headers = {
        'Authorization': f"Bearer {token}"
    }
    
    # These are examples from Spotify's documentation and known working tracks
    test_tracks = [
        # From Spotify's official documentation examples
        {'id': '4iV5W9uYEdYUVa79Axb7Rh', 'name': 'Numb', 'artist': 'Linkin Park'},
        {'id': '3HfB5hBU0dmBt8T0iCmH42', 'name': 'Talking to the Moon', 'artist': 'Bruno Mars'},
        {'id': '0V3wPSX9ygBnCm8psKOegu', 'name': 'Blinding Lights', 'artist': 'The Weeknd'},
        {'id': '7qiZfU4dY1lWnlzDn6eHrm', 'name': 'Shape of You', 'artist': 'Ed Sheeran'},
        
        # Additional popular tracks that should have previews
        {'id': '05bfbizlM5AX6Mf1UyM0PF', 'name': 'Uptown Funk', 'artist': 'Mark Ronson ft. Bruno Mars'},
        {'id': '6rPO02ozF3bM7NnOV4l6ja', 'name': 'Despacito', 'artist': 'Luis Fonsi'},
        {'id': '5RIDHq1o3IEP00A8e1H35W', 'name': 'See You Again', 'artist': 'Wiz Khalifa ft. Charlie Puth'},
        
        # Some tracks from different genres/eras
        {'id': '1zB4vmk8tFRmM9UULNzbLB', 'name': 'God\'s Plan', 'artist': 'Drake'},
        {'id': '3CRDbSIZ4r5MsZ0YwxuEkn', 'name': 'Stressed Out', 'artist': 'Twenty One Pilots'},
        {'id': '7lEptt4wbM0yJTvSG5EBof', 'name': 'Closer', 'artist': 'The Chainsmokers ft. Halsey'}
    ]
    
    tracks_with_previews = 0
    tracks_without_previews = 0
    
    for track in test_tracks:
        print(f"\n🎵 Testing: {track['name']} by {track['artist']}")
        
        try:
            response = requests.get(
                f"https://api.spotify.com/v1/tracks/{track['id']}",
                headers=headers
            )
            
            if response.status_code == 200:
                track_data = response.json()
                
                print(f"   📅 Release Date: {track_data.get('album', {}).get('release_date', 'Unknown')}")
                print(f"   🌍 Available Markets: {len(track_data.get('available_markets', []))}")
                print(f"   📊 Popularity: {track_data.get('popularity', 'Unknown')}/100")
                print(f"   💿 Album: {track_data.get('album', {}).get('name', 'Unknown')}")
                
                preview_url = track_data.get('preview_url')
                if preview_url:
                    print(f"   ✅ Preview URL: {preview_url}")
                    
                    # Test if preview URL is accessible
                    try:
                        preview_response = requests.head(preview_url, timeout=10)
                        if preview_response.status_code == 200:
                            print(f"   ✅ Preview URL is accessible")
                            tracks_with_previews += 1
                        else:
                            print(f"   ❌ Preview URL returned status: {preview_response.status_code}")
                            tracks_without_previews += 1
                    except Exception as e:
                        print(f"   ❌ Error testing preview URL: {e}")
                        tracks_without_previews += 1
                else:
                    print(f"   ❌ No preview URL available")
                    tracks_without_previews += 1
                    
            else:
                print(f"   ❌ Error getting track: {response.status_code}")
                tracks_without_previews += 1
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            tracks_without_previews += 1
        
        # Small delay to avoid rate limiting
        import time
        time.sleep(0.2)
    
    print(f"\n" + "=" * 60)
    print("📊 RESULTS SUMMARY")
    print("=" * 60)
    print(f"✅ Tracks with previews: {tracks_with_previews}")
    print(f"❌ Tracks without previews: {tracks_without_previews}")
    print(f"📊 Success rate: {tracks_with_previews/(tracks_with_previews+tracks_without_previews)*100:.1f}%")
    
    if tracks_with_previews == 0:
        print(f"\n🚨 ALERT: No tracks have preview URLs!")
        print(f"This suggests a regional or account issue.")
        print(f"Possible causes:")
        print(f"• Your Spotify account region doesn't support preview URLs")
        print(f"• You're using a free account with restrictions")
        print(f"• There's a licensing issue in your region")
        print(f"• Your account needs to be updated with country information")

def check_user_account_details():
    """Check detailed user account information"""
    print(f"\n🔍 Checking User Account Details")
    print("=" * 60)
    
    token = get_cached_token()
    if not token:
        print("❌ No cached token found")
        return
    
    headers = {
        'Authorization': f"Bearer {token}"
    }
    
    try:
        # Get detailed user profile
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            
            print(f"👤 Display Name: {user_data.get('display_name', 'Not provided')}")
            print(f"📧 Email: {user_data.get('email', 'Not provided')}")
            print(f"🌍 Country: {user_data.get('country', 'Not provided')}")
            print(f"📅 Account Type: {user_data.get('product', 'Unknown')}")
            print(f"🆔 User ID: {user_data.get('id', 'Not provided')}")
            print(f"🔗 Spotify URI: {user_data.get('uri', 'Not provided')}")
            print(f"🔗 External URL: {user_data.get('external_urls', {}).get('spotify', 'Not provided')}")
            
            # Check if account has country info
            country = user_data.get('country')
            if not country:
                print(f"\n⚠️  WARNING: No country information in account!")
                print(f"This is likely why preview URLs are not available.")
                print(f"To fix this:")
                print(f"1. Go to your Spotify account settings")
                print(f"2. Update your profile with your country")
                print(f"3. Re-authenticate with the app")
            
            # Check account type
            product = user_data.get('product')
            if product == 'free':
                print(f"\n⚠️  WARNING: You're using a free Spotify account!")
                print(f"Free accounts may have limited access to preview URLs.")
                print(f"Consider upgrading to Spotify Premium for full access.")
            elif product == 'premium':
                print(f"\n✅ You have a Premium account - should have full access")
            else:
                print(f"\n❓ Unknown account type: {product}")
                
        else:
            print(f"❌ Error getting user profile: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_region_specific_tracks():
    """Test tracks that are known to work in different regions"""
    print(f"\n🌍 Testing Region-Specific Preview Availability")
    print("=" * 60)
    
    token = get_cached_token()
    if not token:
        print("❌ No cached token found")
        return
    
    headers = {
        'Authorization': f"Bearer {token}"
    }
    
    # Test with market parameter to see if it affects preview URLs
    markets = ['US', 'GB', 'CA', 'AU', 'DE', 'FR', 'JP']
    
    for market in markets:
        print(f"\n🌍 Testing market: {market}")
        
        try:
            # Test a popular track with market parameter
            response = requests.get(
                f"https://api.spotify.com/v1/tracks/4cOdK2wGLETKBW3PvgPWqT?market={market}",
                headers=headers
            )
            
            if response.status_code == 200:
                track_data = response.json()
                preview_url = track_data.get('preview_url')
                
                if preview_url:
                    print(f"   ✅ Preview URL available for {market}")
                else:
                    print(f"   ❌ No preview URL for {market}")
            else:
                print(f"   ❌ Error for {market}: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error testing {market}: {e}")
        
        # Small delay
        import time
        time.sleep(0.5)

def main():
    print("🎵 Spotify Preview URL Investigation")
    print("Based on Spotify Web API Documentation")
    print("=" * 60)
    
    check_user_account_details()
    test_spotify_documentation_examples()
    test_region_specific_tracks()
    
    print(f"\n" + "=" * 60)
    print("🎯 RECOMMENDATIONS")
    print("=" * 60)
    print("If no preview URLs are available:")
    print("1. Update your Spotify account with your country")
    print("2. Consider upgrading to Spotify Premium")
    print("3. Try using a different Spotify account")
    print("4. Check if preview URLs are available in your region")
    print("5. Contact Spotify support about preview URL availability")

if __name__ == "__main__":
    main() 