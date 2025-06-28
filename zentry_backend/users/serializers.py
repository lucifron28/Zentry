from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'avatar', 'role', 'level', 'experience_points', 
            'current_streak', 'longest_streak', 'tasks_completed',
            'password', 'created_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile updates"""
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'avatar', 'role', 'level', 'experience_points', 
            'current_streak', 'longest_streak', 'tasks_completed'
        ]
        read_only_fields = ['level', 'experience_points', 'current_streak', 'longest_streak', 'tasks_completed']

class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for leaderboard display"""
    class Meta:
        model = User
        fields = [
            'id', 'username', 'avatar', 'role', 'level', 
            'experience_points', 'current_streak', 'tasks_completed'
        ]
