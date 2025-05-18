from django.core.management.base import BaseCommand
from sum_app.models.module import Module
from sum_app.models.task import Task
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Seed 2 tasks (Assignment and Tutorial) for each module'

    def handle(self, *args, **kwargs):
        modules = Module.objects.all()

        if not modules.exists():
            self.stdout.write(self.style.ERROR("No modules found. Please seed modules first."))
            return

        count = 0
        for module in modules:
            task_data = [
                {
                    'title': f'{module.name} - Assignment',
                    'type': Task.TaskType.ASSIGNMENT
                },
                {
                    'title': f'{module.name} - Tutorial',
                    'type': Task.TaskType.TUTORIAL
                }
            ]

            for data in task_data:
                task, created = Task.objects.get_or_create(
                    module=module,
                    title=data['title'],
                    defaults={
                        'type': data['type'],
                        'max_score': 100,
                        'start_date': date.today(),
                        'end_date': date.today() + timedelta(days=7)
                    }
                )
                if created:
                    count += 1
                    self.stdout.write(self.style.SUCCESS(f"Created: {task.title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Already exists: {task.title}"))

        self.stdout.write(self.style.SUCCESS(f"Total new tasks seeded: {count}"))
