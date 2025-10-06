#!/usr/bin/env python3
"""
Script to find playlists with tracks that have preview URLs available
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def check_authentication():
    """Check if user is authenticated"""
    try:
        response = requests.get(f"{BASE_URL}/api/playlists/")
        return response.status_code == 200
    except:
        return False

def get_user_playlists():
    """Get user's playlists and check for preview tracks"""
    print("🔍 Checking your playlists for tracks with previews...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/playlists/")
        if response.status_code != 200:
            print("❌ Not authenticated. Please authenticate first.")
            return []
        
        playlists = response.json()
        print(f"✅ Found {len(playlists)} playlists")
        
        playlists_with_previews = []
        
        for i, playlist in enumerate(playlists):
            print(f"\n🔍 Checking playlist {i+1}/{len(playlists)}: {playlist['name']}")
            
            try:
                # Get tracks from this playlist
                tracks_response = requests.get(f"{BASE_URL}/api/playlist/{playlist['id']}/tracks/")
                if tracks_response.status_code == 200:
                    tracks_data = tracks_response.json()
                    tracks_with_preview = tracks_data['tracks_with_preview']
                    total_tracks = tracks_data['total_tracks']
                    
                    print(f"   📊 {tracks_with_preview}/{total_tracks} tracks have previews")
                    
                    if tracks_with_preview > 0:
                        playlists_with_previews.append({
                            'id': playlist['id'],
                            'name': playlist['name'],
                            'tracks_with_preview': tracks_with_preview,
                            'total_tracks': total_tracks
                        })
                        print(f"   ✅ This playlist has tracks with previews!")
                    else:
                        print(f"   ❌ No tracks with previews in this playlist")
                else:
                    print(f"   ❌ Error accessing tracks: {tracks_response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error checking playlist: {e}")
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        return playlists_with_previews
        
    except Exception as e:
        print(f"❌ Error getting playlists: {e}")
        return []

def test_popular_playlists():
    """Test some popular Spotify playlists that are known to have preview tracks"""
    print("\n🔍 Testing popular Spotify playlists...")
    
    # Popular playlists that typically have preview tracks
    popular_playlists = [
        {
            'id': '37i9dQZF1DXcBWIGoYBM5M',
            'name': "Today's Top Hits"
        },
        {
            'id': '37i9dQZEVXbMDoHDwVN2tF',
            'name': 'Global Top 50'
        },
        {
            'id': '37i9dQZF1DX5Vy6DFOcx00',
            'name': 'All Out 2010s'
        },
        {
            'id': '37i9dQZF1DX4sWSpwq3LiO',
            'name': 'Peaceful Piano'
        },
        {
            'id': '37i9dQZF1DX7KNKjOK0o75',
            'name': 'Have a Great Day!'
        }
    ]
    
    playlists_with_previews = []
    
    for playlist in popular_playlists:
        print(f"\n🔍 Testing: {playlist['name']}")
        
        try:
            # Get tracks from this playlist
            tracks_response = requests.get(f"{BASE_URL}/api/playlist/{playlist['id']}/tracks/")
            if tracks_response.status_code == 200:
                tracks_data = tracks_response.json()
                tracks_with_preview = tracks_data['tracks_with_preview']
                total_tracks = tracks_data['total_tracks']
                
                print(f"   📊 {tracks_with_preview}/{total_tracks} tracks have previews")
                
                if tracks_with_preview > 0:
                    playlists_with_previews.append({
                        'id': playlist['id'],
                        'name': playlist['name'],
                        'tracks_with_preview': tracks_with_preview,
                        'total_tracks': total_tracks,
                        'is_public': True
                    })
                    print(f"   ✅ This playlist has tracks with previews!")
                else:
                    print(f"   ❌ No tracks with previews in this playlist")
            else:
                print(f"   ❌ Error accessing tracks: {tracks_response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error checking playlist: {e}")
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    return playlists_with_previews

def show_preview_track_example(playlist_id, playlist_name):
    """Show an example of a track with preview from the playlist"""
    print(f"\n🎵 Example track from '{playlist_name}':")
    
    try:
        # Get a random track from this playlist
        response = requests.get(f"{BASE_URL}/api/playlist/{playlist_id}/random/")
        if response.status_code == 200:
            track = response.json()
            
            print(f"   🎵 Track: {track['name']}")
            print(f"   👤 Artist: {track['artists']}")
            print(f"   💿 Album: {track['album']}")
            print(f"   ⏱️  Duration: {format_duration(track['duration_ms'])}")
            print(f"   🔗 Preview URL: {track['preview_url']}")
            
            # Test if the preview URL is accessible
            try:
                preview_response = requests.head(track['preview_url'], timeout=10)
                if preview_response.status_code == 200:
                    print(f"   ✅ Preview URL is accessible")
                else:
                    print(f"   ❌ Preview URL returned status: {preview_response.status_code}")
            except Exception as e:
                print(f"   ❌ Error testing preview URL: {e}")
            
            return track
        else:
            print(f"   ❌ Error getting random track: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def format_duration(ms):
    """Format duration from milliseconds to MM:SS"""
    minutes = int(ms // 60000)
    seconds = int((ms % 60000) // 1000)
    return f"{minutes}:{seconds:02d}"

def main():
    print("🎵 NameThat - Find Playlists with Preview Tracks")
    print("=" * 60)
    
    # Check authentication
    if not check_authentication():
        print("❌ You need to authenticate first!")
        print("1. Visit: http://127.0.0.1:8000/api/login/")
        print("2. Authorize with Spotify")
        print("3. Run this script again")
        return
    
    print("✅ Authenticated with Spotify!")
    
    # Check user's playlists
    user_playlists = get_user_playlists()
    
    # Check popular playlists
    popular_playlists = test_popular_playlists()
    
    # Combine results
    all_playlists = user_playlists + popular_playlists
    
    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY")
    print("=" * 60)
    
    if all_playlists:
        print(f"✅ Found {len(all_playlists)} playlists with preview tracks:")
        
        for i, playlist in enumerate(all_playlists):
            source = "Your Playlist" if not playlist.get('is_public') else "Public Playlist"
            print(f"\n{i+1}. {playlist['name']} ({source})")
            print(f"   📊 {playlist['tracks_with_preview']}/{playlist['total_tracks']} tracks have previews")
            print(f"   🆔 Playlist ID: {playlist['id']}")
        
        # Show example from first playlist
        first_playlist = all_playlists[0]
        show_preview_track_example(first_playlist['id'], first_playlist['name'])
        
        print(f"\n🌐 Test the audio player:")
        print(f"1. Visit: {BASE_URL}/static/audio_player.html")
        print(f"2. Select one of the playlists above")
        print(f"3. Click 'Load Tracks'")
        print(f"4. Click 'Play Current Track'")
        
    else:
        print("❌ No playlists with preview tracks found!")
        print("\nThis could be due to:")
        print("• Your playlists contain tracks that don't have preview URLs")
        print("• The tracks are from albums that don't allow previews")
        print("• You're in a region where previews aren't available")
        print("• The tracks are very old or obscure")
        
        print(f"\n💡 Try these solutions:")
        print("1. Create a new playlist with popular songs")
        print("2. Add tracks from well-known artists")
        print("3. Use one of the public playlists listed above")
        print("4. Check if you're using a VPN that might affect region")

if __name__ == "__main__":
    main() 