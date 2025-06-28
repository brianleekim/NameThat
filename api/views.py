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
    """Return simple list of current user’s playlists."""
    token = request.session.get("token_info", {}).get("access_token")
    if not token:
        return Response({"error": "not authenticated"}, status=401)

    sp = spotipy.Spotify(auth=token)
    items = sp.current_user_playlists(limit=50)["items"]
    data = [{"id": p["id"], "name": p["name"]} for p in items]
    return Response(data)

@api_view(["POST"])
def start_round(request):
    """
    Given JSON { "playlist_id": "<id>" },
    pick one random track with a preview_url and return it.
    """
    token = request.session.get("token_info", {}).get("access_token")
    if not token:
        return Response({"error": "not authenticated"}, status=401)

    playlist_id = request.data.get("playlist_id")
    if not playlist_id:
        return Response({"error": "playlist_id required"}, status=400)

    sp = spotipy.Spotify(auth=token)
    resp = sp.playlist_tracks(playlist_id, fields="items(track(id,name,preview_url))", limit=100)
    tracks = [t["track"] for t in resp["items"] if t["track"]["preview_url"]]
    if not tracks:
        return Response({"error": "no previewable tracks in this playlist"}, status=400)

    choice = random.choice(tracks)
    return Response({
        "track_id": choice["id"],
        "preview_url": choice["preview_url"],
        "answer": choice["name"]  # omit or hash on the frontend if you want
    })
