from django.contrib import admin
from .models import WebhookIntegration, NotificationLog


@admin.register(WebhookIntegration)
class WebhookIntegrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'webhook_type', 'project', 'created_by', 'is_active', 'created_at']
    list_filter = ['webhook_type', 'is_active', 'created_at']
    search_fields = ['name', 'project__name', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'webhook_type', 'webhook_url', 'project', 'created_by')
        }),
        ('Configuration', {
            'fields': ('event_types', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['webhook_integration', 'event_type', 'status', 'response_status_code', 'retry_count', 'created_at']
    list_filter = ['status', 'event_type', 'webhook_integration__webhook_type', 'created_at']
    search_fields = ['webhook_integration__name', 'event_type', 'error_message']
    readonly_fields = ['created_at', 'sent_at']
    
    fieldsets = (
        (None, {
            'fields': ('webhook_integration', 'event_type', 'status')
        }),
        ('Request/Response', {
            'fields': ('payload', 'response_status_code', 'response_body', 'error_message', 'retry_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'sent_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent manual creation of logs
        return False
