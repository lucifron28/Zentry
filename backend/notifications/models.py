from django.db import models
from django.contrib.auth import get_user_model
from tasks.models import Project

User = get_user_model()


class WebhookIntegration(models.Model):
    WEBHOOK_TYPES = [
        ('discord', 'Discord'),
        ('teams', 'Microsoft Teams'),
    ]
    
    EVENT_TYPES = [
        ('task_completed', 'Task Completed'),
        ('badge_earned', 'Badge Earned'),
        ('project_created', 'Project Created'),
        ('milestone_reached', 'Milestone Reached'),
        ('daily_streak', 'Daily Streak'),
    ]
    
    name = models.CharField(max_length=100)
    webhook_type = models.CharField(max_length=20, choices=WEBHOOK_TYPES)
    webhook_url = models.URLField(max_length=500)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='webhook_integrations')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    event_types = models.JSONField(default=list, help_text="List of event types to trigger this webhook")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Webhook Integration"
        verbose_name_plural = "Webhook Integrations"
        
    def __str__(self):
        return f"{self.name} ({self.webhook_type})"


class NotificationLog(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('retry', 'Retry'),
    ]
    
    webhook_integration = models.ForeignKey(WebhookIntegration, on_delete=models.CASCADE, related_name='logs')
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response_status_code = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Notification Log"
        verbose_name_plural = "Notification Logs"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.webhook_integration.name} - {self.event_type} ({self.status})"
