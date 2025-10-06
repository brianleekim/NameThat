"""
Spotify Preview Finder - Python Implementation
Based on the spotify-preview-finder npm package approach
"""

import spotipy
import os
from typing import List, Dict, Optional, Tuple
import re

class SpotifyPreviewFinder:
    def __init__(self, client_id: str, client_secret: str):
        """Initialize with Spotify credentials"""
        self.client_id = client_id
        self.client_secret = client_secret
        self.sp = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Spotify API"""
        try:
            from spotipy.oauth2 import SpotifyClientCredentials
            auth_manager = SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
        except Exception as e:
            print(f"Authentication failed: {e}")
            self.sp = None
    
    def find_preview_urls(self, song_name: str, artist_name: Optional[str] = None, limit: int = 5) -> Dict:
        """
        Find preview URLs for a song using enhanced search
        
        Args:
            song_name: Name of the song
            artist_name: Name of the artist (optional, but recommended)
            limit: Maximum number of results to return
            
        Returns:
            Dict with success status and results
        """
        if not self.sp:
            return {
                "success": False,
                "error": "Not authenticated with Spotify API"
            }
        
        try:
            # Build search query
            if artist_name:
                search_query = f'track:"{song_name}" artist:"{artist_name}"'
            else:
                search_query = song_name
            
            # Search for tracks
            results = self.sp.search(
                q=search_query,
                type='track',
                limit=limit,
                market='US'  # Use US market for better preview availability
            )
            
            tracks = []
            for item in results['tracks']['items']:
                track_info = self._extract_track_info(item)
                if track_info:
                    tracks.append(track_info)
            
            return {
                "success": True,
                "searchQuery": search_query,
                "results": tracks
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Search failed: {str(e)}"
            }
    
    def _extract_track_info(self, track_item: Dict) -> Optional[Dict]:
        """Extract track information and find preview URLs"""
        try:
            # Basic track info
            track_info = {
                "name": track_item['name'],
                "trackId": track_item['id'],
                "spotifyUrl": track_item['external_urls']['spotify'],
                "albumName": track_item['album']['name'],
                "releaseDate": track_item['album']['release_date'],
                "popularity": track_item['popularity'],
                "durationMs": track_item['duration_ms'],
                "artists": [artist['name'] for artist in track_item['artists']],
                "previewUrls": []
            }
            
            # Check for official preview URL
            if track_item.get('preview_url'):
                track_info["previewUrls"].append({
                    "url": track_item['preview_url'],
                    "type": "official",
                    "source": "spotify_api"
                })
            
            # Try to find alternative preview URLs
            alternative_urls = self._find_alternative_preview_urls(track_info)
            track_info["previewUrls"].extend(alternative_urls)
            
            return track_info
            
        except Exception as e:
            print(f"Error extracting track info: {e}")
            return None
    
    def _find_alternative_preview_urls(self, track_info: Dict) -> List[Dict]:
        """Find alternative preview URLs using various methods"""
        alternative_urls = []
        
        try:
            # Method 1: Try different markets
            markets = ['US', 'GB', 'CA', 'AU', 'DE', 'FR', 'JP']
            for market in markets:
                try:
                    track = self.sp.track(track_info['trackId'], market=market)
                    if track.get('preview_url'):
                        alternative_urls.append({
                            "url": track['preview_url'],
                            "type": "market_alternative",
                            "source": f"spotify_{market.lower()}"
                        })
                        break  # Found one, no need to check more markets
                except:
                    continue
            
            # Method 2: Try searching for similar tracks
            if not alternative_urls:
                similar_tracks = self._find_similar_tracks(track_info)
                for similar in similar_tracks:
                    if similar.get('preview_url'):
                        alternative_urls.append({
                            "url": similar['preview_url'],
                            "type": "similar_track",
                            "source": "spotify_similar"
                        })
                        break
            
            # Method 3: Try album tracks
            if not alternative_urls:
                album_tracks = self._find_album_tracks(track_info)
                for album_track in album_tracks:
                    if album_track.get('preview_url'):
                        alternative_urls.append({
                            "url": album_track['preview_url'],
                            "type": "album_track",
                            "source": "spotify_album"
                        })
                        break
            
        except Exception as e:
            print(f"Error finding alternative URLs: {e}")
        
        return alternative_urls
    
    def _find_similar_tracks(self, track_info: Dict) -> List[Dict]:
        """Find similar tracks that might have preview URLs"""
        try:
            # Get audio features for the track
            features = self.sp.audio_features([track_info['trackId']])
            if not features or not features[0]:
                return []
            
            # Search for tracks with similar characteristics
            search_query = f'artist:"{track_info["artists"][0]}"'
            results = self.sp.search(
                q=search_query,
                type='track',
                limit=10,
                market='US'
            )
            
            return results['tracks']['items']
            
        except Exception as e:
            print(f"Error finding similar tracks: {e}")
            return []
    
    def _find_album_tracks(self, track_info: Dict) -> List[Dict]:
        """Find other tracks from the same album that might have preview URLs"""
        try:
            # Get album tracks
            album_tracks = self.sp.album_tracks(track_info['albumName'], market='US')
            return album_tracks['items']
            
        except Exception as e:
            print(f"Error finding album tracks: {e}")
            return []

def find_preview_urls_for_track(track_name: str, artist_name: str = None, limit: int = 3) -> Dict:
    """
    Convenience function to find preview URLs for a track
    
    Args:
        track_name: Name of the track
        artist_name: Name of the artist (optional)
        limit: Maximum number of results
        
    Returns:
        Dict with preview URL results
    """
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        return {
            "success": False,
            "error": "Spotify credentials not found in environment variables"
        }
    
    finder = SpotifyPreviewFinder(client_id, client_secret)
    return finder.find_preview_urls(track_name, artist_name, limit)

# Example usage
if __name__ == "__main__":
    # Test the preview finder
    result = find_preview_urls_for_track("Shape of You", "Ed Sheeran", 2)
    
    if result["success"]:
        print(f"Search Query: {result['searchQuery']}")
        for track in result["results"]:
            print(f"\nTrack: {track['name']}")
            print(f"Album: {track['albumName']}")
            print(f"Popularity: {track['popularity']}")
            print("Preview URLs:")
            for preview in track['previewUrls']:
                print(f"  - {preview['url']} ({preview['type']})")
    else:
        print(f"Error: {result['error']}") 