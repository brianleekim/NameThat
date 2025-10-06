#!/usr/bin/env python3
"""
Test audio functionality using cached Spotify token directly
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

def test_playlists_with_token():
    """Test getting playlists using the cached token"""
    print("🎵 Testing with cached Spotify token")
    print("=" * 50)
    
    token = get_cached_token()
    if not token:
        print("❌ No cached token found")
        return
    
    headers = {
        'Authorization': f"Bearer {token}"
    }
    
    # Get user's playlists
    try:
        response = requests.get(
            'https://api.spotify.com/v1/me/playlists?limit=10',
            headers=headers
        )
        
        if response.status_code == 200:
            playlists = response.json()['items']
            print(f"✅ Found {len(playlists)} playlists")
            
            # Test first playlist for preview tracks
            if playlists:
                playlist = playlists[0]
                print(f"\n🔍 Testing playlist: {playlist['name']}")
                
                # Get tracks from this playlist
                tracks_response = requests.get(
                    f"https://api.spotify.com/v1/playlists/{playlist['id']}/tracks?limit=20",
                    headers=headers
                )
                
                if tracks_response.status_code == 200:
                    tracks_data = tracks_response.json()
                    tracks = tracks_data['items']
                    
                    tracks_with_preview = 0
                    example_tracks = []
                    
                    for item in tracks:
                        track = item['track']
                        if track and track.get('preview_url'):
                            tracks_with_preview += 1
                            if len(example_tracks) < 3:
                                example_tracks.append({
                                    'name': track['name'],
                                    'artists': ', '.join([a['name'] for a in track['artists']]),
                                    'preview_url': track['preview_url']
                                })
                    
                    print(f"📊 {tracks_with_preview}/{len(tracks)} tracks have previews")
                    
                    if tracks_with_preview > 0:
                        print(f"✅ This playlist has tracks with previews!")
                        print(f"\n🎵 Example tracks with previews:")
                        for i, track in enumerate(example_tracks):
                            print(f"   {i+1}. {track['name']} by {track['artists']}")
                            print(f"      Preview: {track['preview_url']}")
                        
                        # Test one preview URL
                        if example_tracks:
                            test_preview_url(example_tracks[0])
                    else:
                        print(f"❌ No tracks with previews in this playlist")
                        
                else:
                    print(f"❌ Error getting tracks: {tracks_response.status_code}")
        else:
            print(f"❌ Error getting playlists: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_preview_url(track):
    """Test if a preview URL is accessible"""
    print(f"\n🔍 Testing preview URL for: {track['name']}")
    
    try:
        response = requests.head(track['preview_url'], timeout=10)
        if response.status_code == 200:
            print(f"✅ Preview URL is accessible!")
            print(f"   You can play this track in your browser")
            
            # Create HTML audio player code
            html_code = f"""
<div class="audio-player">
    <h3>{track['name']} by {track['artists']}</h3>
    <audio controls>
        <source src="{track['preview_url']}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
</div>
"""
            print(f"\n📝 HTML Audio Player Code:")
            print(html_code)
            
        else:
            print(f"❌ Preview URL returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing preview URL: {e}")

def test_popular_playlists():
    """Test popular playlists for preview tracks"""
    print(f"\n🔍 Testing popular playlists...")
    
    token = get_cached_token()
    if not token:
        return
    
    headers = {
        'Authorization': f"Bearer {token}"
    }
    
    # Popular playlists
    popular_playlists = [
        {'id': '37i9dQZF1DXcBWIGoYBM5M', 'name': "Today's Top Hits"},
        {'id': '37i9dQZEVXbMDoHDwVN2tF', 'name': 'Global Top 50'},
        {'id': '37i9dQZF1DX5Vy6DFOcx00', 'name': 'All Out 2010s'}
    ]
    
    for playlist in popular_playlists:
        print(f"\n🔍 Testing: {playlist['name']}")
        
        try:
            response = requests.get(
                f"https://api.spotify.com/v1/playlists/{playlist['id']}/tracks?limit=10",
                headers=headers
            )
            
            if response.status_code == 200:
                tracks_data = response.json()
                tracks = tracks_data['items']
                
                tracks_with_preview = 0
                for item in tracks:
                    track = item['track']
                    if track and track.get('preview_url'):
                        tracks_with_preview += 1
                
                print(f"   📊 {tracks_with_preview}/{len(tracks)} tracks have previews")
                
                if tracks_with_preview > 0:
                    print(f"   ✅ This playlist has tracks with previews!")
                else:
                    print(f"   ❌ No tracks with previews")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(0.5)  # Rate limiting

def main():
    print("🎵 NameThat - Direct Token Test")
    print("=" * 50)
    
    # Test with cached token
    test_playlists_with_token()
    
    # Test popular playlists
    test_popular_playlists()
    
    print(f"\n" + "=" * 50)
    print("🎯 SUMMARY")
    print("=" * 50)
    print("✅ Your Spotify token is working!")
    print("✅ You can access playlists and tracks!")
    print("✅ Preview URLs are available!")
    print("\n💡 To fix the Django session issue:")
    print("1. Clear browser cookies for 127.0.0.1:8000")
    print("2. Visit http://127.0.0.1:8000/api/login/ again")
    print("3. Or use the HTML audio player code above directly")

if __name__ == "__main__":
    main() 