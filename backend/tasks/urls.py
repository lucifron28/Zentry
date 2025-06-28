from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectListCreateView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:task_id>/comments/', views.TaskCommentListCreateView.as_view(), name='task-comments'),
    path('task-stats/', views.task_stats, name='task-stats'),
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete-task'),
]
