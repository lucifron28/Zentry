from django.urls import path
from django.http import JsonResponse

def badges_list(request):
    return JsonResponse({'results': [], 'count': 0})

def user_badges_list(request):
    return JsonResponse({'results': [], 'count': 0})

urlpatterns = [
    path('achievements/badges/', badges_list, name='badges'),
    path('achievements/user-badges/', user_badges_list, name='user-badges'),
]
