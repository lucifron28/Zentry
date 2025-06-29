from django.urls import path
from django.http import JsonResponse

def users_list(request):
    return JsonResponse({'results': [], 'count': 0})

def profiles_list(request):
    return JsonResponse({'results': [], 'count': 0})

urlpatterns = [
    path('users/users/', users_list, name='users'),
    path('users/profiles/', profiles_list, name='profiles'),
]
