from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import WebhookIntegration, NotificationLog
from .serializers import (
    WebhookIntegrationSerializer, 
    NotificationLogSerializer,
    WebhookTestSerializer
)
from .services import WebhookService


class WebhookIntegrationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing webhook integrations"""
    
    queryset = WebhookIntegration.objects.all()
    serializer_class = WebhookIntegrationSerializer
    permission_classes = [AllowAny]  # Temporarily allow any for testing
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['webhook_type', 'project', 'is_active']
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        if self.request.user.is_authenticated:
            serializer.save(created_by=self.request.user)
        else:
            # For testing without authentication, use a default user
            from django.contrib.auth import get_user_model
            User = get_user_model()
            default_user = User.objects.first()  # Use first user as default
            serializer.save(created_by=default_user)
    
    def get_queryset(self):
        """Filter integrations based on user permissions"""
        queryset = super().get_queryset()
        
        # Users can only see integrations for projects they have access to
        # For now, we'll show all (you might want to add project-based permissions)
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """Test a webhook integration by sending a test message"""
        integration = get_object_or_404(WebhookIntegration, pk=pk)
        
        # Check if user has permission to test this integration
        if request.user.is_authenticated:
            if integration.created_by != request.user and not request.user.is_staff:
                return Response(
                    {'error': 'You do not have permission to test this integration'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        serializer = WebhookTestSerializer(data=request.data)
        if serializer.is_valid():
            test_message = serializer.validated_data.get('test_message', 'Test message from Zentry!')
            
            try:
                log = WebhookService.send_test_notification(integration, test_message)
                
                return Response({
                    'message': 'Test notification sent',
                    'log_id': log.id,
                    'status': log.status,
                    'response_status_code': log.response_status_code
                })
            except Exception as e:
                return Response(
                    {'error': f'Failed to send test notification: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """Get notification logs for a specific webhook integration"""
        integration = get_object_or_404(WebhookIntegration, pk=pk)
        
        logs = NotificationLog.objects.filter(webhook_integration=integration).order_by('-created_at')
        
        # Pagination
        page = self.paginate_queryset(logs)
        if page is not None:
            serializer = NotificationLogSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = NotificationLogSerializer(logs, many=True)
        return Response(serializer.data)


class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing notification logs"""
    
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer
    permission_classes = [AllowAny]  # Temporarily allow any for testing
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'event_type', 'webhook_integration__webhook_type']
    
    def get_queryset(self):
        """Filter logs based on user permissions"""
        queryset = super().get_queryset()
        
        # Users can only see logs for integrations they created
        # Staff can see all logs
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            queryset = queryset.filter(webhook_integration__created_by=self.request.user)
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        """Retry a failed notification"""
        log = get_object_or_404(NotificationLog, pk=pk)
        
        # Check permissions
        if log.webhook_integration.created_by != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to retry this notification'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if retry is allowed
        if log.status not in ['failed', 'retry'] or log.retry_count >= 3:
            return Response(
                {'error': 'This notification cannot be retried'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create a new log entry for the retry
            new_log = WebhookService.send_notification(
                log.webhook_integration,
                log.event_type,
                log.payload
            )
            new_log.retry_count = log.retry_count + 1
            new_log.save()
            
            return Response({
                'message': 'Notification retry initiated',
                'new_log_id': new_log.id,
                'status': new_log.status
            })
        except Exception as e:
            return Response(
                {'error': f'Failed to retry notification: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
