from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.CharField(max_length=50, default='🧑‍💻')
    role = models.CharField(max_length=100, default='Developer')
    level = models.IntegerField(default=1)
    experience_points = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    tasks_completed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - Level {self.level}"

    def add_experience(self, points):
        """Add experience points and level up if needed"""
        self.experience_points += points
        # Level up every 100 XP
        new_level = (self.experience_points // 100) + 1
        if new_level > self.level:
            self.level = new_level
        self.save()

    def update_streak(self):
        """Update user's streak based on activity"""
        from django.utils import timezone
        from datetime import timedelta
        
        today = timezone.now().date()
        if self.last_activity:
            last_activity_date = self.last_activity.date()
            if last_activity_date == today:
                # Already updated today
                return
            elif last_activity_date == today - timedelta(days=1):
                # Continue streak
                self.current_streak += 1
            else:
                # Streak broken
                self.current_streak = 1
        else:
            self.current_streak = 1
        
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        
        self.last_activity = timezone.now()
        self.save()
