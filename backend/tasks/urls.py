from django.urls import path
from django.http import JsonResponse

def projects_list(request):
    return JsonResponse({'results': [], 'count': 0})

def tasks_list(request):
    return JsonResponse({'results': [], 'count': 0})

urlpatterns = [
    path('tasks/projects/', projects_list, name='projects'),
    path('tasks/tasks/', tasks_list, name='tasks'),
]
