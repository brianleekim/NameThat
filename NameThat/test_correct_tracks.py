#!/usr/bin/env python3
"""
Test with correct track IDs for popular songs
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

def test_correct_track_ids():
    """Test with correct track IDs for popular songs"""
    print("🎵 Testing with Correct Track IDs")
    print("=" * 60)
    
    token = get_cached_token()
    if not token:
        print("❌ No cached token found")
        return
    
    headers = {
        'Authorization': f"Bearer {token}"
    }
    
    # These are the CORRECT track IDs for popular songs
    test_tracks = [
        # Blinding Lights - The Weeknd (correct ID)
        {'id': '0V3wPSX9ygBnCm8psKOegu', 'name': 'Blinding Lights', 'artist': 'The Weeknd'},
        
        # Shape of You - Ed Sheeran (correct ID)
        {'id': '7qiZfU4dY1lWnlzDn6eHrm', 'name': 'Shape of You', 'artist': 'Ed Sheeran'},
        
        # Uptown Funk - Mark Ronson ft. Bruno Mars (correct ID)
        {'id': '05bfbizlM5AX6Mf1UyM0PF', 'name': 'Uptown Funk', 'artist': 'Mark Ronson ft. Bruno Mars'},
        
        # Despacito - Luis Fonsi (correct ID)
        {'id': '6rPO02ozF3bM7NnOV4l6ja', 'name': 'Despacito', 'artist': 'Luis Fonsi'},
        
        # See You Again - Wiz Khalifa ft. Charlie Puth (correct ID)
        {'id': '5RIDHq1o3IEP00A8e1H35W', 'name': 'See You Again', 'artist': 'Wiz Khalifa ft. Charlie Puth'},
        
        # God's Plan - Drake (correct ID)
        {'id': '1zB4vmk8tFRmM9UULNzbLB', 'name': 'God\'s Plan', 'artist': 'Drake'},
        
        # Stressed Out - Twenty One Pilots (correct ID)
        {'id': '3CRDbSIZ4r5MsZ0YwxuEkn', 'name': 'Stressed Out', 'artist': 'Twenty One Pilots'},
        
        # Closer - The Chainsmokers ft. Halsey (correct ID)
        {'id': '7lEptt4wbM0yJTvSG5EBof', 'name': 'Closer', 'artist': 'The Chainsmokers ft. Halsey'},
        
        # Some additional popular tracks
        {'id': '4iV5W9uYEdYUVa79Axb7Rh', 'name': 'Numb', 'artist': 'Linkin Park'},
        {'id': '3HfB5hBU0dmBt8T0iCmH42', 'name': 'Talking to the Moon', 'artist': 'Bruno Mars'}
    ]
    
    tracks_with_previews = 0
    tracks_without_previews = 0
    
    for track in test_tracks:
        print(f"\n🎵 Testing: {track['name']} by {track['artist']}")
        print(f"   🆔 Track ID: {track['id']}")
        
        try:
            response = requests.get(
                f"https://api.spotify.com/v1/tracks/{track['id']}",
                headers=headers
            )
            
            if response.status_code == 200:
                track_data = response.json()
                
                print(f"   ✅ Track found: {track_data['name']}")
                print(f"   📅 Release Date: {track_data.get('album', {}).get('release_date', 'Unknown')}")
                print(f"   🌍 Available Markets: {len(track_data.get('available_markets', []))}")
                print(f"   📊 Popularity: {track_data.get('popularity', 'Unknown')}/100")
                print(f"   💿 Album: {track_data.get('album', {}).get('name', 'Unknown')}")
                
                preview_url = track_data.get('preview_url')
                if preview_url:
                    print(f"   🎵 Preview URL: {preview_url}")
                    
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
        time.sleep(0.2)
    
    print(f"\n" + "=" * 60)
    print("📊 RESULTS SUMMARY")
    print("=" * 60)
    print(f"✅ Tracks with previews: {tracks_with_previews}")
    print(f"❌ Tracks without previews: {tracks_without_previews}")
    print(f"📊 Success rate: {tracks_with_previews/(tracks_with_previews+tracks_without_previews)*100:.1f}%")
    
    if tracks_with_previews == 0:
        print(f"\n🚨 ALERT: No tracks have preview URLs!")
        print(f"This is very unusual for a Premium account.")
        print(f"Possible causes:")
        print(f"• Regional licensing restrictions")
        print(f"• Account needs time to update after Premium upgrade")
        print(f"• Technical issue with Spotify's preview service")
        print(f"• Need to contact Spotify support")

def test_user_playlist_tracks():
    """Test tracks from user's actual playlists"""
    print(f"\n🔍 Testing Your Playlist Tracks")
    print("=" * 60)
    
    token = get_cached_token()
    if not token:
        print("❌ No cached token found")
        return
    
    headers = {
        'Authorization': f"Bearer {token}"
    }
    
    try:
        # Get user's playlists
        response = requests.get(
            'https://api.spotify.com/v1/me/playlists?limit=5',
            headers=headers
        )
        
        if response.status_code == 200:
            playlists = response.json()['items']
            
            for playlist in playlists:
                print(f"\n📋 Playlist: {playlist['name']}")
                
                # Get tracks from this playlist
                tracks_response = requests.get(
                    f"https://api.spotify.com/v1/playlists/{playlist['id']}/tracks?limit=3",
                    headers=headers
                )
                
                if tracks_response.status_code == 200:
                    tracks = tracks_response.json()['items']
                    
                    for i, item in enumerate(tracks):
                        track = item['track']
                        if track:
                            print(f"   {i+1}. {track['name']} by {', '.join([a['name'] for a in track['artists']])}")
                            print(f"      🆔 ID: {track['id']}")
                            print(f"      🎵 Preview: {track.get('preview_url', 'None')}")
                            
                            if track.get('preview_url'):
                                print(f"      ✅ Has preview URL!")
                            else:
                                print(f"      ❌ No preview URL")
                else:
                    print(f"   ❌ Error getting tracks: {tracks_response.status_code}")
                
                time.sleep(0.5)  # Rate limiting
        else:
            print(f"❌ Error getting playlists: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🎵 Testing Preview URLs with Premium Account")
    print("=" * 60)
    
    test_correct_track_ids()
    test_user_playlist_tracks()
    
    print(f"\n" + "=" * 60)
    print("🎯 NEXT STEPS")
    print("=" * 60)
    print("If no preview URLs are available:")
    print("1. Wait a few hours for Premium to fully activate")
    print("2. Try logging out and back into Spotify")
    print("3. Contact Spotify support about preview URL access")
    print("4. Consider using the Web Playback SDK instead")

if __name__ == "__main__":
    main() 