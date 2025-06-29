from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'webhook-integrations', views.WebhookIntegrationViewSet)
router.register(r'notification-logs', views.NotificationLogViewSet)

urlpatterns = [
    path('notifications/', include(router.urls)),
]
