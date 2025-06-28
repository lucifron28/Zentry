from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from .models import Project, Task, TaskComment
from .serializers import ProjectSerializer, TaskSerializer, TaskDetailSerializer, TaskCommentSerializer

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(
            Q(created_by=self.request.user) | Q(members=self.request.user)
        ).distinct()
    
    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        project.members.add(self.request.user)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(
            Q(created_by=self.request.user) | Q(members=self.request.user)
        ).distinct()

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Task.objects.filter(
            Q(created_by=self.request.user) | 
            Q(assigned_to=self.request.user) |
            Q(project__members=self.request.user)
        ).distinct().order_by('-created_at')
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by project
        project_id = self.request.query_params.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(
            Q(created_by=self.request.user) | 
            Q(assigned_to=self.request.user) |
            Q(project__members=self.request.user)
        ).distinct()

class TaskCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return TaskComment.objects.filter(task_id=task_id).order_by('-created_at')
    
    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        serializer.save(user=self.request.user, task_id=task_id)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_stats(request):
    """Get task statistics for dashboard"""
    user_tasks = Task.objects.filter(
        Q(assigned_to=request.user) | Q(project__members=request.user)
    ).distinct()
    
    stats = {
        'total_tasks': user_tasks.count(),
        'todo_count': user_tasks.filter(status='todo').count(),
        'in_progress_count': user_tasks.filter(status='in_progress').count(),
        'completed_count': user_tasks.filter(status='completed').count(),
        'my_tasks': user_tasks.filter(assigned_to=request.user).count(),
    }
    
    return Response(stats)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_task(request, task_id):
    """Mark a task as completed"""
    try:
        task = Task.objects.get(
            id=task_id,
            assigned_to=request.user
        )
        task.complete_task()
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
