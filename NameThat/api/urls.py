from django.urls import path
from .views import get_preview_url_view, login, callback, playlists, test_session, debug_session, random_track_from_playlist

urlpatterns = [
    path('get_preview/', get_preview_url_view, name='get_preview_url'),
    path('login/', login, name='login'),
    path('callback/', callback, name='callback'),
    path('playlists/', playlists, name='playlists'),
    path('test_session/', test_session, name='test_session'),
    path('debug_session/', debug_session, name='debug_session'),
    path('random_track_from_playlist/<str:playlist_id>/', random_track_from_playlist, name='random_track_from_playlist'),
]
