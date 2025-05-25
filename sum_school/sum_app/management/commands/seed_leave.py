from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from sum_app.models import Leave, Program, User


class Command(BaseCommand):
    help = 'Seed 5 Leave records for the first 5 programs'

    def handle(self, *args, **options):
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("No user found. Seed a user first."))
            return

        programs = Program.objects.all()[:5]
        if not programs:
            self.stdout.write(self.style.ERROR("No programs found. Seed programs first."))
            return

        for i, program in enumerate(programs):
            leave = Leave.objects.create(
                user=user,
                program=program,
                start_date=timezone.localdate() + timedelta(days=i),
                end_date=timezone.localdate() + timedelta(days=i+2),
                reason=f"Auto-generated leave for {program.name}",
                approve_status=(i % 2 == 0)
            )
            self.stdout.write(self.style.SUCCESS(f"Created Leave: {leave}"))
