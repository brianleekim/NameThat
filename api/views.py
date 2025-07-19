# api/views.py
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import get_spotify_oauth
import spotipy
import random

@api_view(["GET"])
def login(request):
    """Redirect user to Spotify OAuth consent page."""
    auth_url = get_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@api_view(["GET"])
def callback(request):
    """Handle Spotify’s redirect back with code, save token into session."""
    code = request.GET.get("code")
    token_info = get_spotify_oauth().get_access_token(code)
    request.session["token_info"] = token_info
    # After login, send the user on to fetch playlists
    return redirect("/api/playlists/")

@api_view(["GET"])
def playlists(request):
    """Return simple list of current user’s playlists, refreshing token if needed."""
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

@api_view()
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
