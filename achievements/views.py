from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Badge, UserBadge, Leaderboard
from .serializers import BadgeSerializer, UserBadgeSerializer, LeaderboardSerializer

class BadgeListView(generics.ListAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated]

class UserBadgeListView(generics.ListAPIView):
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user).order_by('-earned_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_badge_eligibility(request):
    """Check if user is eligible for new badges"""
    user = request.user
    new_badges = []
    
    # Check streak badges
    streak_badges = Badge.objects.filter(badge_type='streak')
    for badge in streak_badges:
        if (user.current_streak >= badge.requirement_value and 
            not UserBadge.objects.filter(user=user, badge=badge).exists()):
            UserBadge.objects.create(user=user, badge=badge)
            user.add_experience(badge.experience_reward)
            new_badges.append(badge)
    
    # Check task completion badges
    task_badges = Badge.objects.filter(badge_type='tasks')
    for badge in task_badges:
        if (user.tasks_completed >= badge.requirement_value and 
            not UserBadge.objects.filter(user=user, badge=badge).exists()):
            UserBadge.objects.create(user=user, badge=badge)
            user.add_experience(badge.experience_reward)
            new_badges.append(badge)
    
    # Check level badges
    level_badges = Badge.objects.filter(badge_type='level')
    for badge in level_badges:
        if (user.level >= badge.requirement_value and 
            not UserBadge.objects.filter(user=user, badge=badge).exists()):
            UserBadge.objects.create(user=user, badge=badge)
            user.add_experience(badge.experience_reward)
            new_badges.append(badge)
    
    serializer = BadgeSerializer(new_badges, many=True)
    return Response({
        'new_badges': serializer.data,
        'count': len(new_badges)
    })
