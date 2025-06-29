from rest_framework import serializers
from .models import Badge, UserBadge, Leaderboard
from users.serializers import UserProfileSerializer

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = [
            'id', 'name', 'description', 'emoji', 'badge_type',
            'requirement_value', 'experience_reward', 'created_at'
        ]

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = UserBadge
        fields = ['id', 'badge', 'user', 'earned_at']

class LeaderboardSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'leaderboard_type', 'value', 'rank', 'updated_at']
