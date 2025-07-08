from django.db import models
from django.contrib.auth.models import User
import uuid

class GameSession(models.Model):
    """Represents a single game session with a playlist"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    playlist_id = models.CharField(max_length=100)
    playlist_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    total_rounds = models.IntegerField(default=0)
    correct_guesses = models.IntegerField(default=0)
    
    def get_score_percentage(self):
        if self.total_rounds == 0:
            return 0
        return (self.correct_guesses / self.total_rounds) * 100
    
    def __str__(self):
        return f"Game {self.id} - {self.playlist_name}"

class GameRound(models.Model):
    """Represents a single round in a game session"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='rounds')
    track_id = models.CharField(max_length=100)
    track_name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200, blank=True)
    preview_url = models.URLField()
    user_guess = models.CharField(max_length=200, blank=True)
    is_correct = models.BooleanField(null=True)  # null = not answered yet
    time_taken = models.FloatField(null=True)  # seconds taken to answer
    round_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Round {self.round_number} - {self.track_name}"

class UserStats(models.Model):
    """Track user statistics across all games"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_games_played = models.IntegerField(default=0)
    total_rounds_played = models.IntegerField(default=0)
    total_correct_guesses = models.IntegerField(default=0)
    best_score_percentage = models.FloatField(default=0.0)
    average_time_per_guess = models.FloatField(default=0.0)
    last_played = models.DateTimeField(null=True, blank=True)
    
    def update_stats(self, game_session):
        """Update stats after a game session"""
        self.total_games_played += 1
        self.total_rounds_played += game_session.total_rounds
        self.total_correct_guesses += game_session.correct_guesses
        
        if game_session.total_rounds > 0:
            score_percentage = game_session.get_score_percentage()
            if score_percentage > self.best_score_percentage:
                self.best_score_percentage = score_percentage
        
        # Calculate average time (simplified - you can enhance this)
        rounds = game_session.rounds.filter(time_taken__isnull=False)
        if rounds.exists():
            avg_time = sum(r.time_taken for r in rounds) / rounds.count()
            if self.average_time_per_guess == 0:
                self.average_time_per_guess = avg_time
            else:
                # Weighted average
                total_rounds = self.total_rounds_played
                self.average_time_per_guess = (
                    (self.average_time_per_guess * (total_rounds - game_session.total_rounds) + 
                     avg_time * game_session.total_rounds) / total_rounds
                )
        
        self.save()
    
    def __str__(self):
        return f"Stats for {self.user.username}"
