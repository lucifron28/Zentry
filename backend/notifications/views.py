from rest_framework import viewsets
from rest_framework.response import Response
from .models import WebhookIntegration, NotificationLog
from .serializers import WebhookIntegrationSerializer, NotificationLogSerializer

class WebhookIntegrationViewSet(viewsets.ModelViewSet):
    queryset = WebhookIntegration.objects.all()
    serializer_class = WebhookIntegrationSerializer

class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer
