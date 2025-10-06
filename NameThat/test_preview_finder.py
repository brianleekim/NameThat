#!/usr/bin/env python3
"""
Test script for the Spotify Preview Finder
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.preview_finder import find_preview_urls_for_track

def test_preview_finder():
    """Test the preview finder with various tracks"""
    print("🎵 Testing Spotify Preview Finder")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Test tracks (popular songs that should have preview URLs)
    test_tracks = [
        ("Shape of You", "Ed Sheeran"),
        ("Blinding Lights", "The Weeknd"),
        ("Dance Monkey", "Tones and I"),
        ("Uptown Funk", "Mark Ronson ft. Bruno Mars"),
        ("Despacito", "Luis Fonsi"),
    ]
    
    for song_name, artist_name in test_tracks:
        print(f"\n🔍 Testing: {song_name} by {artist_name}")
        print("-" * 40)
        
        result = find_preview_urls_for_track(song_name, artist_name, limit=3)
        
        if result["success"]:
            print(f"✅ Search successful!")
            print(f"Query: {result['searchQuery']}")
            
            for i, track in enumerate(result["results"], 1):
                print(f"\n{i}. {track['name']}")
                print(f"   Album: {track['albumName']}")
                print(f"   Artists: {', '.join(track['artists'])}")
                print(f"   Popularity: {track['popularity']}")
                
                if track['previewUrls']:
                    print(f"   Preview URLs ({len(track['previewUrls'])} found):")
                    for j, preview in enumerate(track['previewUrls'], 1):
                        print(f"     {j}. {preview['url']}")
                        print(f"        Type: {preview['type']}")
                        print(f"        Source: {preview['source']}")
                else:
                    print("   ❌ No preview URLs found")
        else:
            print(f"❌ Error: {result['error']}")
    
    print("\n" + "=" * 50)
    print("🎯 Summary:")
    print("This test shows whether the enhanced preview finder can locate")
    print("preview URLs that might not be available through the standard API.")

if __name__ == "__main__":
    test_preview_finder() 