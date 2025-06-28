import requests
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from django.conf import settings
from django.utils import timezone
from .models import WebhookIntegration, NotificationLog

logger = logging.getLogger(__name__)


class WebhookService:
    """Service for sending webhook notifications to Discord and Microsoft Teams"""
    
    @staticmethod
    def send_notification(integration: WebhookIntegration, event_type: str, data: Dict[str, Any]) -> NotificationLog:
        """Send a webhook notification and log the result"""
        
        # Create notification log entry
        log = NotificationLog.objects.create(
            webhook_integration=integration,
            event_type=event_type,
            payload=data,
            status='pending'
        )
        
        try:
            # Format payload based on webhook type
            if integration.webhook_type == 'discord':
                payload = WebhookService._format_discord_payload(event_type, data)
            elif integration.webhook_type == 'teams':
                payload = WebhookService._format_teams_payload(event_type, data)
            else:
                raise ValueError(f"Unsupported webhook type: {integration.webhook_type}")
            
            # Send the webhook
            response = requests.post(
                integration.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            # Update log with response
            log.response_status_code = response.status_code
            log.response_body = response.text[:1000]  # Limit response body size
            log.sent_at = timezone.now()
            
            if response.status_code in [200, 204]:
                log.status = 'sent'
                logger.info(f"Webhook sent successfully: {integration.name} - {event_type}")
            else:
                log.status = 'failed'
                log.error_message = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"Webhook failed: {integration.name} - {event_type} - {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            log.status = 'failed'
            log.error_message = str(e)
            logger.error(f"Webhook request failed: {integration.name} - {event_type} - {e}")
            
        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
            logger.error(f"Webhook processing failed: {integration.name} - {event_type} - {e}")
            
        log.save()
        return log
    
    @staticmethod
    def _format_discord_payload(event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format payload for Discord webhooks"""
        
        # Color mapping for different event types
        colors = {
            'task_completed': 0x00ff00,  # Green
            'badge_earned': 0xffd700,    # Gold
            'project_created': 0x0099ff, # Blue
            'milestone_reached': 0xff6600, # Orange
            'daily_streak': 0x9966ff,    # Purple
        }
        
        color = colors.get(event_type, 0x808080)  # Default gray
        
        # Base embed structure
        embed = {
            "title": WebhookService._get_event_title(event_type),
            "color": color,
            "timestamp": timezone.now().isoformat(),
            "footer": {
                "text": "Zentry Project Management",
                "icon_url": "https://via.placeholder.com/32x32.png?text=Z"
            }
        }
        
        # Customize embed based on event type
        if event_type == 'task_completed':
            embed["description"] = f"🎉 **{data.get('user_name', 'Someone')}** completed the task **{data.get('task_title', 'Unknown Task')}**!"
            embed["fields"] = [
                {"name": "Project", "value": data.get('project_name', 'Unknown'), "inline": True},
                {"name": "Points Earned", "value": str(data.get('points', 0)), "inline": True}
            ]
            
        elif event_type == 'badge_earned':
            embed["description"] = f"🏆 **{data.get('user_name', 'Someone')}** earned a new badge: **{data.get('badge_name', 'Unknown Badge')}**!"
            embed["fields"] = [
                {"name": "Badge Description", "value": data.get('badge_description', 'No description'), "inline": False}
            ]
            
        elif event_type == 'project_created':
            embed["description"] = f"🚀 New project **{data.get('project_name', 'Unknown Project')}** has been created!"
            embed["fields"] = [
                {"name": "Created by", "value": data.get('user_name', 'Unknown'), "inline": True},
                {"name": "Description", "value": data.get('project_description', 'No description')[:100], "inline": False}
            ]
            
        elif event_type == 'milestone_reached':
            embed["description"] = f"🎯 Milestone reached: **{data.get('milestone_name', 'Unknown Milestone')}**!"
            embed["fields"] = [
                {"name": "Project", "value": data.get('project_name', 'Unknown'), "inline": True},
                {"name": "Progress", "value": f"{data.get('progress', 0)}%", "inline": True}
            ]
            
        elif event_type == 'daily_streak':
            embed["description"] = f"🔥 **{data.get('user_name', 'Someone')}** is on a {data.get('streak_days', 0)} day streak!"
            embed["fields"] = [
                {"name": "Streak Type", "value": data.get('streak_type', 'Daily tasks'), "inline": True}
            ]
        
        return {"embeds": [embed]}
    
    @staticmethod
    def _format_teams_payload(event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format payload for Microsoft Teams webhooks using simple text format"""
        
        # Create simple text message based on event type
        if event_type == 'task_completed':
            text = f"🎉 **Task Completed!**\n\n" \
                   f"**User:** {data.get('user_name', 'Someone')}\n" \
                   f"**Task:** {data.get('task_title', 'Unknown Task')}\n" \
                   f"**Project:** {data.get('project_name', 'Unknown')}\n" \
                   f"**Points Earned:** {data.get('points', 0)} XP\n\n" \
                   f"Great job! 🚀"
                   
        elif event_type == 'badge_earned':
            text = f"🏆 **New Badge Earned!**\n\n" \
                   f"**User:** {data.get('user_name', 'Someone')}\n" \
                   f"**Badge:** {data.get('badge_name', 'Unknown Badge')}\n" \
                   f"**Description:** {data.get('badge_description', 'No description')}\n\n" \
                   f"Congratulations! 🎉"
                   
        elif event_type == 'project_created':
            text = f"🚀 **New Project Created!**\n\n" \
                   f"**Project:** {data.get('project_name', 'Unknown Project')}\n" \
                   f"**Created by:** {data.get('user_name', 'Someone')}\n" \
                   f"**Description:** {data.get('project_description', 'No description')}\n\n" \
                   f"Let's build something amazing! 💪"
                   
        elif event_type == 'milestone_reached':
            text = f"🎯 **Milestone Reached!**\n\n" \
                   f"**Project:** {data.get('project_name', 'Unknown Project')}\n" \
                   f"**Milestone:** {data.get('milestone_name', 'Unknown Milestone')}\n" \
                   f"**Progress:** {data.get('progress', 0)}%\n\n" \
                   f"Keep up the great work! 📈"
                   
        elif event_type == 'daily_streak':
            text = f"🔥 **Daily Streak!**\n\n" \
                   f"**User:** {data.get('user_name', 'Someone')}\n" \
                   f"**Streak:** {data.get('streak_count', 0)} days\n" \
                   f"**Total Points:** {data.get('total_points', 0)} XP\n\n" \
                   f"You're on fire! Keep it up! 🎯"
                   
        else:
            text = f"📢 **Zentry Notification**\n\n" \
                   f"**Event:** {event_type.replace('_', ' ').title()}\n" \
                   f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" \
                   f"Something awesome happened in your project! 🎉"
        
        return {"text": text}
    
    @staticmethod
    def _get_event_title(event_type: str) -> str:
        """Get a human-readable title for the event type"""
        titles = {
            'task_completed': 'Task Completed',
            'badge_earned': 'Badge Earned',
            'project_created': 'Project Created', 
            'milestone_reached': 'Milestone Reached',
            'daily_streak': 'Daily Streak'
        }
        return titles.get(event_type, 'Zentry Notification')
    
    @staticmethod
    def send_test_notification(integration: WebhookIntegration, message: str = "Test message from Zentry!") -> NotificationLog:
        """Send a test notification to verify webhook configuration"""
        test_data = {
            'message': message,
            'timestamp': timezone.now().isoformat(),
            'test': True
        }
        
        return WebhookService.send_notification(integration, 'test', test_data)


def trigger_webhook_notifications(event_type: str, data: Dict[str, Any], project_id: Optional[int] = None):
    """
    Trigger webhook notifications for a specific event
    
    Args:
        event_type: The type of event (task_completed, badge_earned, etc.)
        data: Event data to include in the notification
        project_id: Optional project ID to filter integrations
    """
    
    # Get active webhook integrations for this event type
    integrations = WebhookIntegration.objects.filter(is_active=True)
    
    if project_id:
        integrations = integrations.filter(project_id=project_id)
    
    # Filter by event type (since JSONField contains lookup doesn't work in SQLite)
    filtered_integrations = []
    for integration in integrations:
        if event_type in integration.event_types:
            filtered_integrations.append(integration)
    
    # Send notifications
    for integration in filtered_integrations:
        try:
            WebhookService.send_notification(integration, event_type, data)
        except Exception as e:
            logger.error(f"Failed to send webhook notification: {integration.name} - {e}")
