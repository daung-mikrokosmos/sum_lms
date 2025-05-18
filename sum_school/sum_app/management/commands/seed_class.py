from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from sum_app.models.module import Module
from sum_app.models.module_class import Class  # adjust if needed

class Command(BaseCommand):
    help = 'Seed the database with 20 classes for each module'

    def handle(self, *args, **kwargs):
        modules = Module.objects.all()
        if not modules.exists():
            self.stdout.write(self.style.WARNING("No modules found. Please seed modules first."))
            return

        count = 0
        base_start = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0)

        for module in modules:
            for i in range(1, 21):  # 20 classes
                title = f"{module.name} - Class {i}"
                start_time = base_start + timedelta(days=i)
                end_time = start_time + timedelta(hours=2)

                class_obj, created = Class.objects.get_or_create(
                    module=module,
                    title=title,
                    defaults={
                        'start_time': start_time,
                        'end_time': end_time,
                        'canceled': False
                    }
                )

                if created:
                    count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created: {title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Already exists: {title}'))

        self.stdout.write(self.style.SUCCESS(f'Total new classes seeded: {count}'))
