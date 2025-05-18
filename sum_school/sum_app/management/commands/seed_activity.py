from django.core.management.base import BaseCommand
from sum_app.models.module import Module
from sum_app.models.activity import Activity
from django.utils.text import slugify
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed the database with sample activities for each module'

    def handle(self, *args, **kwargs):
        modules = Module.objects.all()
        if not modules.exists():
            self.stdout.write(self.style.WARNING("No modules found. Please seed modules first."))
            return

        count = 0
        for module in modules:
            activities_data = [
                {
                    'title': f'{module.name} - Presentation',
                    'description': f'A student presentation for the module {module.name}.',
                    'type': Activity.ActivityType.PRESENTATION
                },
                {
                    'title': f'{module.name} - Debate',
                    'description': f'A debate session related to {module.name}.',
                    'type': Activity.ActivityType.DEBATE
                }
            ]
            
            for index, activity_data in enumerate(activities_data):
                schedule_date = timezone.localdate() - timedelta(days=1) if index < 1 else timezone.localdate() + timedelta(days=3)

                activity, created = Activity.objects.get_or_create(
                    title=activity_data['title'],
                    module=module,
                    defaults={
                        'description': activity_data['description'],
                        'type': activity_data['type'],
                        'schedule': schedule_date
                    }
                )

                if created:
                    count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created: {activity.title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Already exists: {activity.title}'))

        self.stdout.write(self.style.SUCCESS(f'Total new activities seeded: {count}'))
