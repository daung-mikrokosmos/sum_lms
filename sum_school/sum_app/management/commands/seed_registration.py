from django.core.management.base import BaseCommand
from sum_app.models.registration import Registration
from sum_app.models.program import Program
from sum_app.models.user import User

class Command(BaseCommand):
    help = 'Seed 6 registrations (3 students and 3 teachers) for the first 3 programs'

    def handle(self, *args, **kwargs):
        programs = Program.objects.all()[:3]
        users = User.objects.filter(user_id__in=[1, 2, 3, 4, 5, 6])

        if programs.count() < 3 or users.count() < 6:
            self.stdout.write(self.style.ERROR("Make sure there are at least 3 programs and 6 users (IDs 1–6)."))
            return

        student_ids = [1, 2, 3]
        teacher_ids = [4, 5, 6]
        count = 0

        for program in programs:
            student_count = Registration.objects.filter(program=program, teacher_flag=False).count()

            for sid in student_ids:
                user = User.objects.get(user_id=sid)
                student_count += 1
                student_code = f"{program.program_code}-{student_count}"

                reg, created = Registration.objects.get_or_create(
                    user=user,
                    program=program,
                    defaults={
                        'nickname': f"{user.name} Nickname",
                        'student_code': student_code,
                        'teacher_flag': False,
                        'scholared': False,
                        'payment_status': Registration.PaymentStatus.NOT_PAID,
                    }
                )
                if created:
                    count += 1
                    self.stdout.write(self.style.SUCCESS(f"Created student: {reg}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Student exists: {reg}"))

            for tid in teacher_ids:
                user = User.objects.get(user_id=tid)

                # Teachers don’t need student_code, give them dummy or skip
                reg, created = Registration.objects.get_or_create(
                    user=user,
                    program=program,
                    defaults={
                        'nickname': f"{user.name}_teacher",
                        'teacher_flag': True,
                        'scholared': False,
                        'payment_status': Registration.PaymentStatus.SCHOLARED,
                    }
                )
                if created:
                    count += 1
                    self.stdout.write(self.style.SUCCESS(f"Created teacher: {reg}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Teacher exists: {reg}"))

        self.stdout.write(self.style.SUCCESS(f"Total new registrations created: {count}"))
