from rest_framework import serializers
from .models import WebhookIntegration, NotificationLog


class WebhookIntegrationSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = WebhookIntegration
        fields = [
            'id', 'name', 'webhook_type', 'webhook_url', 'project', 'project_name',
            'created_by', 'created_by_username', 'event_types', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        
    def validate_event_types(self, value):
        """Validate that event_types contains valid choices"""
        valid_events = [choice[0] for choice in WebhookIntegration.EVENT_TYPES]
        for event in value:
            if event not in valid_events:
                raise serializers.ValidationError(f"'{event}' is not a valid event type.")
        return value


class NotificationLogSerializer(serializers.ModelSerializer):
    webhook_integration_name = serializers.CharField(source='webhook_integration.name', read_only=True)
    webhook_type = serializers.CharField(source='webhook_integration.webhook_type', read_only=True)
    
    class Meta:
        model = NotificationLog
        fields = [
            'id', 'webhook_integration', 'webhook_integration_name', 'webhook_type',
            'event_type', 'payload', 'status', 'response_status_code',
            'response_body', 'error_message', 'retry_count',
            'created_at', 'sent_at'
        ]
        read_only_fields = ['created_at', 'sent_at']


class WebhookTestSerializer(serializers.Serializer):
    """Serializer for testing webhook endpoints"""
    test_message = serializers.CharField(max_length=500, default="Test message from Zentry!", required=False)
