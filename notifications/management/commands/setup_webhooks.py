from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tasks.models import Project
from notifications.models import WebhookIntegration

User = get_user_model()


class Command(BaseCommand):
    help = 'Create example webhook integrations for Discord and Microsoft Teams'

    def add_arguments(self, parser):
        parser.add_argument(
            '--discord-url',
            type=str,
            help='Discord webhook URL',
            default='https://discord.com/api/webhooks/CHANNEL_ID/TOKEN'
        )
        parser.add_argument(
            '--teams-url',
            type=str,
            help='Microsoft Teams webhook URL', 
            default='https://outlook.office.com/webhook/WEBHOOK_ID/IncomingWebhook/CONNECTOR_ID'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating example webhook integrations...'))
        
        # Get the first project and user (assuming they exist from initial data)
        try:
            project = Project.objects.first()
            user = User.objects.first()
            
            if not project:
                self.stdout.write(self.style.ERROR('No projects found. Please create some projects first.'))
                return
                
            if not user:
                self.stdout.write(self.style.ERROR('No users found. Please create some users first.'))
                return
            
            # Create Discord webhook integration
            discord_webhook, created = WebhookIntegration.objects.get_or_create(
                name="Team Discord Notifications",
                webhook_type="discord",
                defaults={
                    'webhook_url': options['discord_url'],
                    'project': project,
                    'created_by': user,
                    'event_types': ['task_completed', 'badge_earned', 'project_created', 'milestone_reached'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created Discord webhook integration: {discord_webhook.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Discord webhook integration already exists: {discord_webhook.name}')
                )
            
            # Create Microsoft Teams webhook integration
            teams_webhook, created = WebhookIntegration.objects.get_or_create(
                name="Team Microsoft Teams Notifications",
                webhook_type="teams",
                defaults={
                    'webhook_url': options['teams_url'],
                    'project': project,
                    'created_by': user,
                    'event_types': ['task_completed', 'badge_earned', 'daily_streak'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created Teams webhook integration: {teams_webhook.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Teams webhook integration already exists: {teams_webhook.name}')
                )
            
            self.stdout.write('\n' + self.style.SUCCESS('🎉 Webhook integrations setup complete!'))
            
            # Display setup instructions
            self.stdout.write('\n' + self.style.WARNING('📋 SETUP INSTRUCTIONS:'))
            self.stdout.write('\nTo use these webhook integrations:')
            self.stdout.write('\n1. DISCORD SETUP:')
            self.stdout.write('   • Go to your Discord server settings')
            self.stdout.write('   • Navigate to Integrations > Webhooks')
            self.stdout.write('   • Create a new webhook and copy the URL')
            self.stdout.write(f'   • Update the webhook URL in the admin or via API: {discord_webhook.id}')
            
            self.stdout.write('\n2. MICROSOFT TEAMS SETUP:')
            self.stdout.write('   • Go to your Teams channel')
            self.stdout.write('   • Click the three dots (...) > Connectors')
            self.stdout.write('   • Find "Incoming Webhook" and configure it')
            self.stdout.write('   • Copy the webhook URL')
            self.stdout.write(f'   • Update the webhook URL in the admin or via API: {teams_webhook.id}')
            
            self.stdout.write('\n3. TESTING:')
            self.stdout.write('   • Use the Django admin to test webhooks')
            self.stdout.write('   • Or use the API endpoint: POST /api/notifications/webhook-integrations/{id}/test/')
            self.stdout.write('   • Complete tasks to trigger automatic notifications')
            
            self.stdout.write('\n4. API ENDPOINTS:')
            self.stdout.write('   • GET /api/notifications/webhook-integrations/ - List all webhooks')
            self.stdout.write('   • POST /api/notifications/webhook-integrations/ - Create new webhook')
            self.stdout.write('   • PUT /api/notifications/webhook-integrations/{id}/ - Update webhook')
            self.stdout.write('   • POST /api/notifications/webhook-integrations/{id}/test/ - Test webhook')
            self.stdout.write('   • GET /api/notifications/notification-logs/ - View notification history')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating webhook integrations: {e}'))
