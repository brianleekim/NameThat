#!/usr/bin/env python3
"""
Check all your playlists for tracks with preview URLs
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

def check_all_playlists():
    """Check all user playlists for preview tracks"""
    print("🎵 Checking all your playlists for tracks with previews")
    print("=" * 60)
    
    token = get_cached_token()
    if not token:
        print("❌ No cached token found")
        return
    
    headers = {
        'Authorization': f"Bearer {token}"
    }
    
    # Get all user playlists
    try:
        response = requests.get(
            'https://api.spotify.com/v1/me/playlists?limit=50',
            headers=headers
        )
        
        if response.status_code == 200:
            playlists = response.json()['items']
            print(f"✅ Found {len(playlists)} playlists")
            
            playlists_with_previews = []
            
            for i, playlist in enumerate(playlists):
                print(f"\n🔍 Checking playlist {i+1}/{len(playlists)}: {playlist['name']}")
                
                try:
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
                                if len(example_tracks) < 2:
                                    example_tracks.append({
                                        'name': track['name'],
                                        'artists': ', '.join([a['name'] for a in track['artists']]),
                                        'preview_url': track['preview_url']
                                    })
                        
                        print(f"   📊 {tracks_with_preview}/{len(tracks)} tracks have previews")
                        
                        if tracks_with_preview > 0:
                            playlists_with_previews.append({
                                'id': playlist['id'],
                                'name': playlist['name'],
                                'tracks_with_preview': tracks_with_preview,
                                'total_tracks': len(tracks),
                                'examples': example_tracks
                            })
                            print(f"   ✅ This playlist has tracks with previews!")
                            
                            # Show example tracks
                            for j, track in enumerate(example_tracks):
                                print(f"      {j+1}. {track['name']} by {track['artists']}")
                        else:
                            print(f"   ❌ No tracks with previews in this playlist")
                    else:
                        print(f"   ❌ Error getting tracks: {tracks_response.status_code}")
                        
                except Exception as e:
                    print(f"   ❌ Error checking playlist: {e}")
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
            
            # Summary
            print("\n" + "=" * 60)
            print("📊 RESULTS SUMMARY")
            print("=" * 60)
            
            if playlists_with_previews:
                print(f"✅ Found {len(playlists_with_previews)} playlists with preview tracks:")
                
                for i, playlist in enumerate(playlists_with_previews):
                    print(f"\n{i+1}. {playlist['name']}")
                    print(f"   📊 {playlist['tracks_with_preview']}/{playlist['total_tracks']} tracks have previews")
                    print(f"   🆔 Playlist ID: {playlist['id']}")
                    print(f"   🎵 Example tracks:")
                    for track in playlist['examples']:
                        print(f"      • {track['name']} by {track['artists']}")
                
                # Test the first playlist with previews
                first_playlist = playlists_with_previews[0]
                print(f"\n🎵 Testing audio playback with '{first_playlist['name']}':")
                test_playlist_audio(first_playlist)
                
            else:
                print("❌ No playlists with preview tracks found!")
                print("\n💡 This means your playlists contain tracks that don't have preview URLs.")
                print("   This is common with:")
                print("   • Old songs (pre-2000s)")
                print("   • Obscure or indie tracks")
                print("   • Live recordings")
                print("   • Songs from certain regions")
                
                print(f"\n💡 Solutions:")
                print("1. Create a new playlist with popular songs")
                print("2. Add tracks from well-known artists")
                print("3. Use songs from the last 10-15 years")
                
        else:
            print(f"❌ Error getting playlists: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_playlist_audio(playlist):
    """Test audio playback for a specific playlist"""
    print(f"\n🔍 Testing audio for playlist: {playlist['name']}")
    
    if playlist['examples']:
        track = playlist['examples'][0]
        print(f"🎵 Testing track: {track['name']} by {track['artists']}")
        
        try:
            response = requests.head(track['preview_url'], timeout=10)
            if response.status_code == 200:
                print(f"✅ Preview URL is accessible!")
                
                # Create HTML audio player
                html_code = f"""
<div class="audio-player">
    <h3>{track['name']} by {track['artists']}</h3>
    <audio controls>
        <source src="{track['preview_url']}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    <p>From playlist: {playlist['name']}</p>
</div>
"""
                print(f"\n📝 HTML Audio Player Code:")
                print(html_code)
                
                print(f"\n🌐 To test in browser:")
                print(f"1. Create a new HTML file with the code above")
                print(f"2. Open it in your browser")
                print(f"3. Click play to hear the 30-second preview")
                
            else:
                print(f"❌ Preview URL returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing preview URL: {e}")

def main():
    check_all_playlists()

if __name__ == "__main__":
    main() 