# Zentry Webhook Integration Guide

This guide explains how to set up and use webhook integrations in Zentry for Discord and Microsoft Teams notifications.

## Overview

Zentry supports webhook integrations that automatically send notifications to Discord and Microsoft Teams when specific events occur in your projects:

- ✅ **Task Completed** - When a team member completes a task
- 🏆 **Badge Earned** - When a user earns a new achievement badge
- 🚀 **Project Created** - When a new project is created
- 🎯 **Milestone Reached** - When project milestones are achieved
- 🔥 **Daily Streak** - When users maintain daily activity streaks

## Setup Instructions

### 1. Discord Webhook Setup

1. **Create Discord Webhook:**
   - Go to your Discord server
   - Right-click on the channel where you want notifications
   - Select "Edit Channel" → "Integrations" → "Webhooks"
   - Click "Create Webhook"
   - Give it a name (e.g., "Zentry Bot")
   - Copy the webhook URL

2. **Configure in Zentry:**
   - Go to Django Admin: `/admin/notifications/webhookintegration/`
   - Find your Discord integration or create a new one
   - Paste the webhook URL
   - Select event types you want to receive
   - Set `is_active` to True

### 2. Microsoft Teams Webhook Setup

1. **Create Teams Webhook:**
   - Go to your Teams channel
   - Click the three dots (...) next to the channel name
   - Select "Connectors"
   - Find "Incoming Webhook" and click "Configure"
   - Give it a name (e.g., "Zentry Notifications")
   - Optionally upload an image
   - Click "Create" and copy the webhook URL

2. **Configure in Zentry:**
   - Go to Django Admin: `/admin/notifications/webhookintegration/`
   - Find your Teams integration or create a new one
   - Paste the webhook URL
   - Select event types you want to receive
   - Set `is_active` to True

## API Endpoints

### Webhook Integrations

#### List all webhook integrations
```
GET /api/notifications/api/webhook-integrations/
```

#### Create new webhook integration
```
POST /api/notifications/api/webhook-integrations/
Content-Type: application/json

{
    "name": "My Discord Notifications",
    "webhook_type": "discord",
    "webhook_url": "https://discord.com/api/webhooks/CHANNEL_ID/TOKEN",
    "project": 1,
    "event_types": ["task_completed", "badge_earned"],
    "is_active": true
}
```

#### Update webhook integration
```
PUT /api/notifications/api/webhook-integrations/{id}/
Content-Type: application/json

{
    "name": "Updated Name",
    "event_types": ["task_completed", "badge_earned", "milestone_reached"],
    "is_active": true
}
```

#### Test webhook integration
```
POST /api/notifications/api/webhook-integrations/{id}/test/
Content-Type: application/json

{
    "test_message": "Hello from Zentry! This is a test notification."
}
```

#### Get webhook logs
```
GET /api/notifications/api/webhook-integrations/{id}/logs/
```

### Notification Logs

#### List all notification logs
```
GET /api/notifications/api/notification-logs/
```

#### Filter logs by status
```
GET /api/notifications/api/notification-logs/?status=failed
GET /api/notifications/api/notification-logs/?event_type=task_completed
```

#### Retry failed notification
```
POST /api/notifications/api/notification-logs/{id}/retry/
```

## Event Types and Data

### Task Completed
Triggered when a task status changes to "completed"

**Data included:**
```json
{
    "task_id": 123,
    "task_title": "Implement user authentication",
    "task_description": "Add login and signup functionality",
    "user_name": "john_doe",
    "user_id": 1,
    "project_name": "Web App Project",
    "project_id": 1,
    "points": 25,
    "completed_at": "2024-01-15T10:30:00Z"
}
```

### Badge Earned
Triggered when a user earns a new badge

**Data included:**
```json
{
    "badge_id": 5,
    "badge_name": "Task Master",
    "badge_description": "Complete 10 tasks in a single day",
    "user_name": "john_doe",
    "user_id": 1,
    "earned_at": "2024-01-15T10:30:00Z"
}
```

### Project Created
Triggered when a new project is created

**Data included:**
```json
{
    "project_id": 2,
    "project_name": "Mobile App Development",
    "project_description": "Build a cross-platform mobile application",
    "user_name": "jane_smith",
    "user_id": 2,
    "created_at": "2024-01-15T10:30:00Z"
}
```

### Milestone Reached
Triggered when project reaches certain completion percentages

**Data included:**
```json
{
    "milestone_name": "50% Project Completion",
    "project_name": "Web App Project",
    "project_id": 1,
    "progress": 50,
    "user_name": "project_manager",
    "user_id": 3
}
```

### Daily Streak
Triggered when users maintain daily activity

**Data included:**
```json
{
    "user_name": "john_doe",
    "user_id": 1,
    "streak_days": 7,
    "streak_type": "Daily task completion"
}
```

## Testing Webhooks

### Via Management Command
```bash
# Test task completion notification
python manage.py test_webhook --event-type task_completed --project-id 1

# Test badge earned notification
python manage.py test_webhook --event-type badge_earned

# Test project creation notification
python manage.py test_webhook --event-type project_created
```

### Via API
```bash
# Test a specific webhook integration
curl -X POST http://localhost:8000/api/notifications/api/webhook-integrations/1/test/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"test_message": "Test from API!"}'
```

### Via Admin Interface
1. Go to `/admin/notifications/webhookintegration/`
2. Click on a webhook integration
3. Look for test functionality (if added to admin)

## Monitoring and Troubleshooting

### Check Notification Logs
- **Admin Interface:** `/admin/notifications/notificationlog/`
- **API:** `GET /api/notifications/api/notification-logs/`

### Common Issues

1. **Webhook URL Invalid:**
   - Verify the webhook URL is correct
   - Check if the webhook was deleted in Discord/Teams

2. **Authentication Errors:**
   - Ensure the webhook URL includes the correct token
   - Check if the bot/connector is still active

3. **Rate Limiting:**
   - Discord/Teams may rate limit requests
   - Check response codes in notification logs

4. **Network Issues:**
   - Check server connectivity
   - Review error messages in logs

### Status Codes
- `200/204` - Success
- `400` - Bad request (check payload format)
- `401` - Unauthorized (check webhook URL/token)
- `404` - Webhook not found (URL may be invalid)
- `429` - Rate limited (reduce notification frequency)

## Message Formats

### Discord Messages
Discord webhooks receive rich embeds with:
- Colored borders based on event type
- Event title and description
- Relevant fields (project, points, etc.)
- Timestamp and footer with Zentry branding

### Teams Messages
Teams webhooks receive MessageCard format with:
- Themed colors based on event type
- Activity title and subtitle
- Facts sections with key information
- Professional formatting for business environments

## Advanced Configuration

### Custom Event Types
You can extend the system by:
1. Adding new event types to `WebhookIntegration.EVENT_TYPES`
2. Creating signal handlers for new events
3. Implementing custom payload formatting

### Filtering Events
Webhook integrations can be configured to only receive specific event types:
```json
{
    "event_types": ["task_completed", "badge_earned"]
}
```

### Project-Specific Webhooks
Each webhook integration is associated with a specific project, allowing for:
- Project-specific Discord channels
- Team-specific notifications
- Departmental separation

## Security Considerations

1. **Webhook URL Security:**
   - Keep webhook URLs confidential
   - Regenerate URLs if compromised
   - Use HTTPS endpoints only

2. **Rate Limiting:**
   - Implement delays between notifications if needed
   - Monitor for unusual activity

3. **Data Privacy:**
   - Review what data is included in notifications
   - Ensure compliance with privacy policies
   - Consider sensitive information in task titles/descriptions

## Troubleshooting Commands

```bash
# Check webhook integrations
python manage.py shell -c "from notifications.models import WebhookIntegration; print(WebhookIntegration.objects.all())"

# Check recent notification logs
python manage.py shell -c "from notifications.models import NotificationLog; print(NotificationLog.objects.order_by('-created_at')[:5])"

# Manually trigger webhook for testing
python manage.py test_webhook --event-type task_completed

# Check if signals are working
python manage.py shell -c "from django.db.models.signals import post_save; print(post_save.receivers)"
```
