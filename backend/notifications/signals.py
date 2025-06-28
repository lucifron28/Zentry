from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tasks.models import Task, Project
from achievements.models import UserBadge
from .services import trigger_webhook_notifications
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Task)
def task_status_changed(sender, instance, created, **kwargs):
    """Trigger webhook when task status changes"""
    if not created and instance.status == 'completed':
        # Task was completed
        data = {
            'task_id': instance.id,
            'task_title': instance.title,
            'task_description': instance.description,
            'user_name': instance.assigned_to.username if instance.assigned_to else 'Unknown',
            'user_id': instance.assigned_to.id if instance.assigned_to else None,
            'project_name': instance.project.name,
            'project_id': instance.project.id,
            'points': getattr(instance, 'points', 10),  # Default points if not set
            'completed_at': instance.updated_at.isoformat() if instance.updated_at else None
        }
        
        trigger_webhook_notifications('task_completed', data, instance.project.id)
        logger.info(f"Task completed webhook triggered: {instance.title}")


@receiver(post_save, sender=Project)
def project_created(sender, instance, created, **kwargs):
    """Trigger webhook when new project is created"""
    if created:
        data = {
            'project_id': instance.id,
            'project_name': instance.name,
            'project_description': instance.description,
            'user_name': instance.created_by.username if instance.created_by else 'Unknown',
            'user_id': instance.created_by.id if instance.created_by else None,
            'created_at': instance.created_at.isoformat() if instance.created_at else None
        }
        
        trigger_webhook_notifications('project_created', data, instance.id)
        logger.info(f"Project created webhook triggered: {instance.name}")


@receiver(post_save, sender=UserBadge)
def badge_earned(sender, instance, created, **kwargs):
    """Trigger webhook when user earns a new badge"""
    if created:
        data = {
            'badge_id': instance.badge.id,
            'badge_name': instance.badge.name,
            'badge_description': instance.badge.description,
            'user_name': instance.user.username,
            'user_id': instance.user.id,
            'earned_at': instance.earned_at.isoformat() if instance.earned_at else None
        }
        
        # Try to get project context if available
        # This might need to be adjusted based on your badge logic
        project_id = None
        
        trigger_webhook_notifications('badge_earned', data, project_id)
        logger.info(f"Badge earned webhook triggered: {instance.user.username} - {instance.badge.name}")


# You can add more signal handlers for other events:
# - milestone_reached (when project reaches certain completion %)
# - daily_streak (when user maintains daily activity)
# etc.
