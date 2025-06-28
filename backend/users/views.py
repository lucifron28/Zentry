from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .models import User
from .serializers import UserSerializer, UserProfileSerializer, LeaderboardSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            serializer = UserProfileSerializer(user)
            return Response({
                'user': serializer.data,
                'message': 'Login successful'
            })
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class LeaderboardView(generics.ListAPIView):
    serializer_class = LeaderboardSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        leaderboard_type = self.request.query_params.get('type', 'experience_points')
        
        if leaderboard_type == 'tasks_completed':
            return User.objects.all().order_by('-tasks_completed')[:10]
        elif leaderboard_type == 'current_streak':
            return User.objects.all().order_by('-current_streak')[:10]
        elif leaderboard_type == 'longest_streak':
            return User.objects.all().order_by('-longest_streak')[:10]
        else:  # experience_points
            return User.objects.all().order_by('-experience_points')[:10]

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_stats(request):
    """Get dashboard statistics"""
    user_count = User.objects.count()
    total_experience = sum(user.experience_points for user in User.objects.all())
    active_users = User.objects.filter(current_streak__gt=0).count()
    
    return Response({
        'total_users': user_count,
        'total_experience': total_experience,
        'active_users': active_users,
    })
