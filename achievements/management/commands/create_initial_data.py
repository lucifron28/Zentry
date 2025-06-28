from django.core.management.base import BaseCommand
from achievements.models import Badge
from users.models import User
from tasks.models import Project, Task

class Command(BaseCommand):
    help = 'Create initial data for Zentry'

    def handle(self, *args, **options):
        # Create badges
        badges_data = [
            {
                'name': 'First Steps',
                'description': 'Complete your first task',
                'emoji': '🎯',
                'badge_type': 'tasks',
                'requirement_value': 1,
                'experience_reward': 50,
            },
            {
                'name': 'Task Master',
                'description': 'Complete 10 tasks',
                'emoji': '🏆',
                'badge_type': 'tasks',
                'requirement_value': 10,
                'experience_reward': 100,
            },
            {
                'name': 'Dedicated',
                'description': 'Maintain a 3-day streak',
                'emoji': '🔥',
                'badge_type': 'streak',
                'requirement_value': 3,
                'experience_reward': 75,
            },
            {
                'name': 'Streak Warrior',
                'description': 'Maintain a 7-day streak',
                'emoji': '⚡',
                'badge_type': 'streak',
                'requirement_value': 7,
                'experience_reward': 150,
            },
            {
                'name': 'Level Up',
                'description': 'Reach level 5',
                'emoji': '🌟',
                'badge_type': 'level',
                'requirement_value': 5,
                'experience_reward': 200,
            },
            {
                'name': 'Elite',
                'description': 'Reach level 10',
                'emoji': '💎',
                'badge_type': 'level',
                'requirement_value': 10,
                'experience_reward': 500,
            },
        ]

        for badge_data in badges_data:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults=badge_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created badge: {badge.name}')
                )

        # Create demo users
        demo_users = [
            {
                'username': 'alex_dev',
                'email': 'alex@zentry.dev',
                'first_name': 'Alex',
                'last_name': 'Developer',
                'avatar': '👨‍💻',
                'role': 'Frontend Developer',
                'level': 3,
                'experience_points': 250,
                'current_streak': 5,
                'tasks_completed': 12,
            },
            {
                'username': 'sarah_designer',
                'email': 'sarah@zentry.dev',
                'first_name': 'Sarah',
                'last_name': 'Designer',
                'avatar': '🎨',
                'role': 'UI/UX Designer',
                'level': 4,
                'experience_points': 320,
                'current_streak': 3,
                'tasks_completed': 18,
            },
            {
                'username': 'mike_backend',
                'email': 'mike@zentry.dev',
                'first_name': 'Mike',
                'last_name': 'Backend',
                'avatar': '⚙️',
                'role': 'Backend Developer',
                'level': 5,
                'experience_points': 450,
                'current_streak': 7,
                'tasks_completed': 25,
            },
        ]

        for user_data in demo_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('demo123')
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user.username}')
                )

        # Create a demo project
        admin_user = User.objects.get(username='admin')
        project, created = Project.objects.get_or_create(
            name='Zentry Development',
            defaults={
                'description': 'Building the ultimate gamified project management app',
                'emoji': '🚀',
                'created_by': admin_user,
            }
        )
        
        if created:
            # Add all users to the project
            all_users = User.objects.all()
            project.members.set(all_users)
            self.stdout.write(
                self.style.SUCCESS(f'Created project: {project.name}')
            )

            # Create demo tasks
            demo_tasks = [
                {
                    'title': 'Set up SvelteKit frontend',
                    'description': 'Initialize the frontend with SvelteKit and TailwindCSS',
                    'status': 'completed',
                    'emoji': '🎨',
                    'priority': 'high',
                    'experience_reward': 50,
                },
                {
                    'title': 'Design user authentication',
                    'description': 'Create login and registration forms',
                    'status': 'in_progress',
                    'emoji': '🔐',
                    'priority': 'high',
                    'experience_reward': 40,
                },
                {
                    'title': 'Implement task board',
                    'description': 'Create drag-and-drop task board with status columns',
                    'status': 'todo',
                    'emoji': '📋',
                    'priority': 'medium',
                    'experience_reward': 60,
                },
                {
                    'title': 'Add streak tracking',
                    'description': 'Implement daily streak tracking and rewards',
                    'status': 'todo',
                    'emoji': '🔥',
                    'priority': 'medium',
                    'experience_reward': 45,
                },
                {
                    'title': 'Create AI coach feature',
                    'description': 'Implement Zenturion AI coach with suggestions',
                    'status': 'todo',
                    'emoji': '🤖',
                    'priority': 'low',
                    'experience_reward': 80,
                },
            ]

            users_list = list(User.objects.all())
            for i, task_data in enumerate(demo_tasks):
                task = Task.objects.create(
                    project=project,
                    created_by=admin_user,
                    assigned_to=users_list[i % len(users_list)],
                    **task_data
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created task: {task.title}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully created initial data!')
        )
