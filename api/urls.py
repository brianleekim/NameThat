from django.urls import path
from . import views

urlpatterns = [
    path("login/",    views.login),      # GET  /api/login/
    path("callback/", views.callback),   # GET  /api/callback/
    path("playlists/",views.playlists),  # GET  /api/playlists/
    # New endpoints for playlist and track access
    path("playlist/<str:playlist_id>/tracks/", views.playlist_tracks), # GET /api/playlist/<id>/tracks/
]
