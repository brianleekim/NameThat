from django.contrib import admin
from .models import GameSession, GameRound, UserStats

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'playlist_name', 'total_rounds', 'correct_guesses', 'get_score_percentage', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['playlist_name', 'playlist_id']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']

@admin.register(GameRound)
class GameRoundAdmin(admin.ModelAdmin):
    list_display = ['round_number', 'track_name', 'artist_name', 'is_correct', 'time_taken', 'created_at']
    list_filter = ['is_correct', 'created_at', 'game_session']
    search_fields = ['track_name', 'artist_name', 'user_guess']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_games_played', 'total_rounds_played', 'best_score_percentage', 'last_played']
    list_filter = ['last_played']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['last_played']
    ordering = ['-best_score_percentage']
