#!/usr/bin/env python3
"""
Debug script to examine individual tracks and understand why they don't have preview URLs
"""

import requests
import json
import time

def get_cached_token():
    """Get the cached Spotify token"""
    try:
        with open('.cache', 'r') as f:
            cache_data = json.load(f)
        return cache_data.get('access_token')
    except:
        return None

def examine_playlist_tracks(playlist_name, playlist_id):
    """Examine individual tracks in a playlist to understand why they don't have previews"""
    print(f"\n🔍 Examining tracks in playlist: {playlist_name}")
    print("=" * 60)
    
    token = get_cached_token()
    if not token:
        print("❌ No cached token found")
        return
    
    headers = {
        'Authorization': f"Bearer {token}"
    }
    
    try:
        # Get tracks from this playlist
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=10",
            headers=headers
        )
        
        if response.status_code == 200:
            tracks_data = response.json()
            tracks = tracks_data['items']
            
            print(f"📊 Found {len(tracks)} tracks to examine")
            
            for i, item in enumerate(tracks):
                track = item['track']
                if not track:
                    print(f"\n{i+1}. ❌ Null track (removed from Spotify)")
                    continue
                
                print(f"\n{i+1}. 🎵 {track['name']} by {', '.join([a['name'] for a in track['artists']])}")
                print(f"   📅 Release Date: {track.get('album', {}).get('release_date', 'Unknown')}")
                print(f"   🌍 Available Markets: {len(track.get('available_markets', []))}")
                print(f"   📊 Popularity: {track.get('popularity', 'Unknown')}/100")
                print(f"   💿 Album: {track.get('album', {}).get('name', 'Unknown')}")
                print(f"   🏷️  Label: {track.get('album', {}).get('label', 'Unknown')}")
                
                # Check for preview URL
                preview_url = track.get('preview_url')
                if preview_url:
                    print(f"   ✅ Preview URL: {preview_url}")
                    
                    # Test if preview URL is accessible
                    try:
                        preview_response = requests.head(preview_url, timeout=10)
                        if preview_response.status_code == 200:
                            print(f"   ✅ Preview URL is accessible")
                        else:
                            print(f"   ❌ Preview URL returned status: {preview_response.status_code}")
                    except Exception as e:
                        print(f"   ❌ Error testing preview URL: {e}")
                else:
                    print(f"   ❌ No preview URL available")
                    
                    # Check possible reasons
                    reasons = []
                    
                    # Check if track is from a very old album
                    release_date = track.get('album', {}).get('release_date', '')
                    if release_date and release_date < '2000':
                        reasons.append("Very old track (pre-2000)")
                    
                    # Check if track has low popularity
                    popularity = track.get('popularity', 0)
                    if popularity < 30:
                        reasons.append("Low popularity")
                    
                    # Check if track is from a small label
                    label = track.get('album', {}).get('label', '').lower()
                    if label and any(small_label in label for small_label in ['indie', 'independent', 'local']):
                        reasons.append("Independent/small label")
                    
                    # Check if track is explicit
                    if track.get('explicit', False):
                        reasons.append("Explicit content")
                    
                    # Check if track is from a compilation
                    album_type = track.get('album', {}).get('album_type', '')
                    if album_type == 'compilation':
                        reasons.append("Compilation album")
                    
                    if reasons:
                        print(f"   💡 Possible reasons: {', '.join(reasons)}")
                    else:
                        print(f"   💡 No obvious reason - this might be a regional/licensing issue")
                
                # Small delay to avoid rate limiting
                time.sleep(0.2)
                
        else:
            print(f"❌ Error getting tracks: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_specific_tracks():
    """Test specific popular tracks to see if they have preview URLs"""
    print(f"\n🔍 Testing specific popular tracks")
    print("=" * 60)
    
    token = get_cached_token()
    if not token:
        print("❌ No cached token found")
        return
    
    headers = {
        'Authorization': f"Bearer {token}"
    }
    
    # Test specific track IDs for popular songs
    test_tracks = [
        {'id': '4cOdK2wGLETKBW3PvgPWqT', 'name': 'Blinding Lights', 'artist': 'The Weeknd'},
        {'id': '7qiZfU4dY1lWnlzDn6eHrm', 'name': 'Shape of You', 'artist': 'Ed Sheeran'},
        {'id': '05bfbizlM5AX6Mf1UyM0PF', 'name': 'Uptown Funk', 'artist': 'Mark Ronson ft. Bruno Mars'},
        {'id': '6rPO02ozF3bM7NnOV4l6ja', 'name': 'Despacito', 'artist': 'Luis Fonsi'},
        {'id': '5RIDHq1o3IEP00A8e1H35W', 'name': 'See You Again', 'artist': 'Wiz Khalifa ft. Charlie Puth'}
    ]
    
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
                
                preview_url = track_data.get('preview_url')
                if preview_url:
                    print(f"   ✅ Preview URL: {preview_url}")
                    
                    # Test if preview URL is accessible
                    try:
                        preview_response = requests.head(preview_url, timeout=10)
                        if preview_response.status_code == 200:
                            print(f"   ✅ Preview URL is accessible")
                        else:
                            print(f"   ❌ Preview URL returned status: {preview_response.status_code}")
                    except Exception as e:
                        print(f"   ❌ Error testing preview URL: {e}")
                else:
                    print(f"   ❌ No preview URL available")
                    
            else:
                print(f"   ❌ Error getting track: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(0.5)  # Rate limiting

def check_user_market():
    """Check what market the user is in and if that affects preview availability"""
    print(f"\n🔍 Checking user market and region")
    print("=" * 60)
    
    token = get_cached_token()
    if not token:
        print("❌ No cached token found")
        return
    
    headers = {
        'Authorization': f"Bearer {token}"
    }
    
    try:
        # Get user profile to see their country
        response = requests.get(
            'https://api.spotify.com/v1/me',
            headers=headers
        )
        
        if response.status_code == 200:
            user_data = response.json()
            country = user_data.get('country', 'Unknown')
            print(f"🌍 Your country: {country}")
            
            if country:
                print(f"💡 Preview availability can vary by region")
                print(f"   Some tracks may not have previews in {country}")
                print(f"   This is often due to licensing restrictions")
            else:
                print(f"💡 No country information available")
                
        else:
            print(f"❌ Error getting user profile: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🎵 NameThat - Track Preview Debug")
    print("=" * 60)
    
    # Check user market first
    check_user_market()
    
    # Test specific popular tracks
    test_specific_tracks()
    
    # Examine tracks from first playlist
    token = get_cached_token()
    if token:
        headers = {'Authorization': f"Bearer {token}"}
        
        try:
            response = requests.get(
                'https://api.spotify.com/v1/me/playlists?limit=1',
                headers=headers
            )
            
            if response.status_code == 200:
                playlists = response.json()['items']
                if playlists:
                    playlist = playlists[0]
                    examine_playlist_tracks(playlist['name'], playlist['id'])
                    
        except Exception as e:
            print(f"❌ Error getting playlists: {e}")
    
    print(f"\n" + "=" * 60)
    print("🎯 SUMMARY")
    print("=" * 60)
    print("This script helps identify why tracks don't have preview URLs.")
    print("Common reasons include:")
    print("• Regional licensing restrictions")
    print("• Old tracks (pre-2000)")
    print("• Independent/small label releases")
    print("• Explicit content")
    print("• Compilation albums")

if __name__ == "__main__":
    main() 