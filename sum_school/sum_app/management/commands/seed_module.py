from django.core.management.base import BaseCommand
from sum_app.models.module import Module
from sum_app.models.program import Program
from sum_app.models.user import User
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Seed the database with sample modules'

    def handle(self, *args, **kwargs):
        modules_data = [
            {
                'name': 'Introduction to Programming',
                'module_code': 'P1-1001',
                'program_id': 1,
                'teacher_id': 4,
                'credit': 3
            },
            {
                'name': 'Database Fundamentals',
                'module_code': 'P1-1002',
                'program_id': 1,
                'teacher_id': 5,
                'credit': 3
            },
            {
                'name': 'Web Development',
                'module_code': 'P1-1003',
                'program_id': 1,
                'teacher_id': 6,
                'credit': 3
            },
            {
                'name': 'Introduction to Python',
                'module_code': 'P2-1001',
                'program_id': 2,
                'teacher_id': 4,
                'credit': 4
            },
            {
                'name': 'Python Fundamentals',
                'module_code': 'P2-1002',
                'program_id': 2,
                'teacher_id': 5,
                'credit': 4
            },
            {
                'name': 'Python Web Development',
                'module_code': 'P2-1003',
                'program_id': 2,
                'teacher_id': 6,
                'credit': 4
            },
        ]

        for data in modules_data:
            try:
                program = Program.objects.get(program_id=data['program_id'])
            except ObjectDoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"⚠ Program with ID {data['program_id']} not found. Skipping module '{data['name']}'."
                ))
                continue

            try:
                teacher = User.objects.get(user_id=data['teacher_id'], is_teacher=True)
            except ObjectDoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"⚠ Teacher with ID {data['teacher_id']} not found. Setting NULL for module '{data['name']}'."
                ))
                teacher = None

            module, created = Module.objects.get_or_create(
                module_code=data['module_code'],
                defaults={
                    'name': data['name'],
                    'program': program,
                    'teacher': teacher,
                    'credit': data['credit']
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Module "{module.name}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'ℹ Module "{module.name}" already exists.'))
