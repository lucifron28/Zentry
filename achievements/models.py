from django.db import models
from django.conf import settings

class Badge(models.Model):
    BADGE_TYPES = [
        ('streak', 'Streak'),
        ('tasks', 'Tasks'),
        ('level', 'Level'),
        ('special', 'Special'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    emoji = models.CharField(max_length=10, default='🏆')
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES, default='tasks')
    requirement_value = models.IntegerField(help_text="Number needed to unlock (e.g., 5 for '5-day streak')")
    experience_reward = models.IntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emoji} {self.name}"

class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.username} earned {self.badge.name}"

class Leaderboard(models.Model):
    LEADERBOARD_TYPES = [
        ('tasks_completed', 'Tasks Completed'),
        ('experience_points', 'Experience Points'),
        ('current_streak', 'Current Streak'),
        ('longest_streak', 'Longest Streak'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leaderboard_type = models.CharField(max_length=30, choices=LEADERBOARD_TYPES)
    value = models.IntegerField()
    rank = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'leaderboard_type')
        ordering = ['rank']

    def __str__(self):
        return f"{self.user.username} - {self.leaderboard_type}: #{self.rank}"
