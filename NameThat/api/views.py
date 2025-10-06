# api/views.py
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import get_spotify_oauth
import spotipy
import random
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@api_view(["GET"])
def debug_session(request):
    """Simple debug endpoint to test session functionality."""
    # Set a simple value in session
    request.session["debug_test"] = "session_working"
    request.session.save()
    
    # Get the value back
    debug_value = request.session.get("debug_test", "not_found")
    
    return Response({
        "session_id": request.session.session_key,
        "debug_value": debug_value,
        "all_session_data": dict(request.session),
        "message": "Debug session test"
    })

@api_view(["GET"])
def test_session(request):
    """Test endpoint to check if sessions are working."""
    # Debug logging
    print(f"Test session request - Session ID: {request.session.session_key}")
    print(f"Session data: {dict(request.session)}")
    
    # Set a test value
    request.session["test_value"] = "hello_world"
    request.session.save()
    
    return Response({
        "session_id": request.session.session_key,
        "session_data": dict(request.session),
        "message": "Session test successful"
    })

@api_view(["GET"])
def login(request):
    """Redirect user to Spotify OAuth consent page."""
    # Create or get existing session
    if not request.session.session_key:
        request.session.create()
    
    # Use the session key as state to preserve the session
    state = request.session.session_key
    auth_url = get_spotify_oauth().get_authorize_url(state=state)
    return redirect(auth_url)

@api_view(["GET"])
def callback(request):
    """Handle Spotify's redirect back with code, save token into session."""
    code = request.GET.get("code")
    state = request.GET.get("state")  # This should be our session key
    
    # Get the token info
    token_info = get_spotify_oauth().get_access_token(code)
    
    # Try to restore the original session using the state parameter
    if state:
        try:
            # Create a new session store with the original session key
            from django.contrib.sessions.backends.db import SessionStore
            original_session = SessionStore(session_key=state)
            
            # Save the token to the original session
            original_session["token_info"] = token_info
            original_session.save()
            
            # Set this session as the current one
            request.session = original_session
            
        except Exception as e:
            # Fallback: create new session
            if not request.session.session_key:
                request.session.create()
            request.session["token_info"] = token_info
            request.session.save()
    else:
        # No state parameter, create new session
        if not request.session.session_key:
            request.session.create()
        request.session["token_info"] = token_info
        request.session.save()
    
    # Redirect back to the frontend
    return redirect("http://localhost:3000/")

@api_view(["GET"])
def playlists(request):
    """Return simple list of current user's playlists, refreshing token if needed."""
    token_info = request.session.get("token_info")
    if not token_info:
        return Response({"error": "not authenticated"}, status=401)

    oauth = get_spotify_oauth()

    # If token expired, refresh it
    if oauth.is_token_expired(token_info):
        token_info = oauth.refresh_access_token(token_info["refresh_token"])
        request.session["token_info"] = token_info

    sp = spotipy.Spotify(auth=token_info["access_token"])
    items = sp.current_user_playlists(limit=50)["items"]
    data = [{"id": p["id"], "name": p["name"]} for p in items]
    return Response(data)

@api_view(["GET"])
def playlist_tracks(request, playlist_id):
    token = request.session.get("token_info", {}).get("access_token")
    if not token:
        return Response({"error": "not authenticated"}, status=401)
    
    try:
        sp = spotipy.Spotify(auth=token)
        
        # Get playlist details first
        playlist_info = sp.playlist(playlist_id, fields="name,description,images,owner(display_name)")
        
        # Get all tracks from the playlist
        # Using fields parameter to get detailed track information
        fields = "items(track(id,name,artists,album(name,images),preview_url,duration_ms,popularity,external_urls))"
        tracks_response = sp.playlist_tracks(playlist_id, fields=fields, limit=100)
        
        tracks = []
        for item in tracks_response["items"]:
            track = item["track"]
            if track:  # Skip null tracks
                # Extract artist names
                artists = [artist["name"] for artist in track.get("artists", [])]
                artist_names = ", ".join(artists)
                
                # Get album image (first image if available)
                album_images = track.get("album", {}).get("images", [])
                album_image = album_images[0]["url"] if album_images else None
                
                track_info = {
                    "id": track["id"],
                    "name": track["name"],
                    "artists": artist_names,
                    "album": track.get("album", {}).get("name", ""),
                    "album_image": album_image,
                    "preview_url": track.get("preview_url"),
                    "duration_ms": track.get("duration_ms"),
                    "popularity": track.get("popularity"),
                    "spotify_url": track.get("external_urls", {}).get("spotify"),
                    "has_preview": bool(track.get("preview_url"))
                }
                tracks.append(track_info)
        
        return Response({
            "playlist": {
                "id": playlist_id,
                "name": playlist_info["name"],
                "description": playlist_info.get("description", ""),
                "owner": playlist_info.get("owner", {}).get("display_name", ""),
                "image": playlist_info.get("images", [{}])[0].get("url") if playlist_info.get("images") else None
            },
            "tracks": tracks,
            "total_tracks": len(tracks),
            "tracks_with_preview": len([t for t in tracks if t["has_preview"]]),
            "tracks_without_preview": len([t for t in tracks if not t["has_preview"]])
        })
        
    except Exception as e:
        return Response({"error": f"Failed to get playlist tracks: {str(e)}"}, status=400)

@api_view(["GET"])
def track_preview(request, track_id):
    """Get a single track with its preview URL for audio playback."""
    token = request.session.get("token_info", {}).get("access_token")
    if not token:
        return Response({"error": "not authenticated"}, status=401)
    
    try:
        sp = spotipy.Spotify(auth=token)
        
        # Get track details
        track = sp.track(track_id)
        
        # Extract artist names
        artists = [artist["name"] for artist in track.get("artists", [])]
        artist_names = ", ".join(artists)
        
        # Get album image
        album_images = track.get("album", {}).get("images", [])
        album_image = album_images[0]["url"] if album_images else None
        
        track_info = {
            "id": track["id"],
            "name": track["name"],
            "artists": artist_names,
            "album": track.get("album", {}).get("name", ""),
            "album_image": album_image,
            "preview_url": track.get("preview_url"),
            "duration_ms": track.get("duration_ms"),
            "popularity": track.get("popularity"),
            "spotify_url": track.get("external_urls", {}).get("spotify"),
            "has_preview": bool(track.get("preview_url")),
            "audio_features": None
        }
        
        # Get audio features if available
        try:
            features = sp.audio_features([track_id])[0]
            if features:
                track_info["audio_features"] = {
                    "tempo": features.get("tempo"),
                    "key": features.get("key"),
                    "mode": features.get("mode"),
                    "danceability": features.get("danceability"),
                    "energy": features.get("energy"),
                    "valence": features.get("valence")
                }
        except:
            pass  # Audio features not available
        
        return Response(track_info)
        
    except Exception as e:
        return Response({"error": f"Failed to get track: {str(e)}"}, status=400)

@api_view(["GET"])
def random_track_from_playlist(request, playlist_id):
    """Get a random track from a playlist for guessing games, using Node.js preview service if needed."""
    token = request.session.get("token_info", {}).get("access_token")
    if not token:
        return Response({"error": "not authenticated"}, status=401)
    
    try:
        sp = spotipy.Spotify(auth=token)
        # Get all tracks from the playlist
        fields = "items(track(id,name,artists,album(name,images),preview_url,duration_ms,popularity,external_urls))"
        tracks_response = sp.playlist_tracks(playlist_id, fields=fields, limit=100)
        
        # Filter out null tracks
        valid_tracks = [item["track"] for item in tracks_response["items"] if item["track"]]
        if not valid_tracks:
            return Response({"error": "No tracks found in this playlist"}, status=404)
        
        # Shuffle tracks to randomize selection
        random.shuffle(valid_tracks)
        
        # Try to find a track with a preview (Spotify or Node)
        for track in valid_tracks:
            preview_url = track.get("preview_url")
            # If no Spotify preview, try Node.js service
            if not preview_url:
                track_name = track.get("name", "")
                artists = track.get("artists", [])
                artist_name = artists[0]["name"] if artists else ""
                try:
                    resp = requests.get(
                        "http://localhost:3001/preview",
                        params={"track": track_name, "artist": artist_name},
                        timeout=5
                    )
                    data = resp.json()
                    preview_url = data.get("preview")
                except Exception:
                    preview_url = None
            if preview_url:
                # Extract artist names
                artists = [artist["name"] for artist in track.get("artists", [])]
                artist_names = ", ".join(artists)
                # Get album image
                album_images = track.get("album", {}).get("images", [])
                album_image = album_images[0]["url"] if album_images else None
                track_info = {
                    "id": track["id"],
                    "name": track["name"],
                    "artists": artist_names,
                    "album": track.get("album", {}).get("name", ""),
                    "album_image": album_image,
                    "preview_url": preview_url,
                    "duration_ms": track.get("duration_ms"),
                    "popularity": track.get("popularity"),
                    "spotify_url": track.get("external_urls", {}).get("spotify"),
                    "has_preview": True
                }
                return Response(track_info)
        # If no track with any preview found
        return Response({"error": "No tracks with preview available in this playlist (Spotify or Node)"}, status=404)
    except Exception as e:
        return Response({"error": f"Failed to get random track: {str(e)}"}, status=400)

@csrf_exempt
def get_preview_url_view(request):
    track = request.GET.get('track')
    artist = request.GET.get('artist')
    if not track or not artist:
        return JsonResponse({'error': 'Missing track or artist'}, status=400)
    try:
        resp = requests.get('http://localhost:3001/preview', params={'track': track, 'artist': artist}, timeout=5)
        data = resp.json()
        if 'preview' in data and data['preview']:
            return JsonResponse({'preview': data['preview']})
        else:
            return JsonResponse({'error': 'No preview found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
