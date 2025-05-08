from django.core.management.base import BaseCommand
from sum_app.models import User
from django.contrib.auth.hashers import make_password
import os

class Command(BaseCommand):
    help = "Seed the database with a student and a teacher"

    def handle(self, *args, **kwargs):
        # --- Student ---
        student_email = os.getenv("STUDENT_EMAIL", "student@example.com")
        student_password = os.getenv("STUDENT_PASSWORD", "student123")
        student_name = os.getenv("STUDENT_NAME", "Student")

        if not User.objects.filter(email=student_email).exists():
            student = User.objects.create(
                name=student_name,
                email=student_email,
                is_teacher=False,
                is_approved=True,
                user_code="SSM-000001",
                password=make_password(student_password)
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Student '{student.name}' created successfully!"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ Student with email {student_email} already exists."))

        # --- Teacher ---
        teacher_email = os.getenv("TEACHER_EMAIL", "teacher@example.com")
        teacher_password = os.getenv("TEACHER_PASSWORD", "teacher123")
        teacher_name = os.getenv("TEACHER_NAME", "Teacher")

        if not User.objects.filter(email=teacher_email).exists():
            teacher = User.objects.create(
                name=teacher_name,
                email=teacher_email,
                is_teacher=True,
                is_approved=True,
                user_code="SSM-000002",
                password=make_password(teacher_password)
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Teacher '{teacher.name}' created successfully!"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ Teacher with email {teacher_email} already exists."))
