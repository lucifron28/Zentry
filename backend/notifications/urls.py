from django.urls import path
from django.http import JsonResponse

def webhook_integrations_list(request):
    return JsonResponse({'results': [], 'count': 0})

def notification_logs_list(request):
    return JsonResponse({'results': [], 'count': 0})

urlpatterns = [
    path('notifications/webhook-integrations/', webhook_integrations_list, name='webhook-integrations'),
    path('notifications/notification-logs/', notification_logs_list, name='notification-logs'),
]
