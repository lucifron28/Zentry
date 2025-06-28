from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from notifications.services import trigger_webhook_notifications
from tasks.models import Project

User = get_user_model()


class Command(BaseCommand):
    help = 'Trigger a test webhook notification manually'

    def add_arguments(self, parser):
        parser.add_argument(
            '--event-type',
            type=str,
            choices=['task_completed', 'badge_earned', 'project_created', 'milestone_reached', 'daily_streak'],
            default='task_completed',
            help='Type of event to simulate'
        )
        parser.add_argument(
            '--project-id',
            type=int,
            help='Project ID to use for testing'
        )

    def handle(self, *args, **options):
        event_type = options['event_type']
        project_id = options.get('project_id')
        
        try:
            # Get project for context
            if project_id:
                project = Project.objects.get(id=project_id)
            else:
                project = Project.objects.first()
                
            if not project:
                self.stdout.write(self.style.ERROR('No projects found. Please create a project first.'))
                return
            
            user = User.objects.first()
            if not user:
                self.stdout.write(self.style.ERROR('No users found. Please create a user first.'))
                return
            
            # Create test data based on event type
            if event_type == 'task_completed':
                data = {
                    'task_id': 999,
                    'task_title': 'Test Task Completion',
                    'task_description': 'This is a test task completion notification',
                    'user_name': user.username,
                    'user_id': user.id,
                    'project_name': project.name,
                    'project_id': project.id,
                    'points': 25,
                    'completed_at': '2024-01-15T10:30:00Z'
                }
                
            elif event_type == 'badge_earned':
                data = {
                    'badge_id': 999,
                    'badge_name': 'Test Achievement Badge',
                    'badge_description': 'You earned this badge for testing webhook notifications!',
                    'user_name': user.username,
                    'user_id': user.id,
                    'earned_at': '2024-01-15T10:30:00Z'
                }
                
            elif event_type == 'project_created':
                data = {
                    'project_id': project.id,
                    'project_name': f'Test Project - {project.name}',
                    'project_description': 'This is a test project creation notification',
                    'user_name': user.username,
                    'user_id': user.id,
                    'created_at': '2024-01-15T10:30:00Z'
                }
                
            elif event_type == 'milestone_reached':
                data = {
                    'milestone_name': '50% Project Completion',
                    'project_name': project.name,
                    'project_id': project.id,
                    'progress': 50,
                    'user_name': user.username,
                    'user_id': user.id
                }
                
            elif event_type == 'daily_streak':
                data = {
                    'user_name': user.username,
                    'user_id': user.id,
                    'streak_days': 7,
                    'streak_type': 'Daily task completion'
                }
            
            self.stdout.write(f'Triggering {event_type} webhook notification...')
            
            # Trigger the webhook notifications
            trigger_webhook_notifications(event_type, data, project.id)
            
            self.stdout.write(self.style.SUCCESS(f'✓ Webhook notification triggered successfully!'))
            self.stdout.write(f'Event: {event_type}')
            self.stdout.write(f'Project: {project.name}')
            self.stdout.write('\nCheck the notification logs in the admin or via API to see the results.')
            
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Project with ID {project_id} not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error triggering webhook notification: {e}'))
