from django.urls import path
from . import views

urlpatterns = [
    path("login/",    views.login),      # GET  /api/login/
    path("callback/", views.callback),   # GET  /api/callback/
    path("playlists/",views.playlists),  # GET  /api/playlists/
    path("round/",    views.start_round),# POST /api/round/
]
