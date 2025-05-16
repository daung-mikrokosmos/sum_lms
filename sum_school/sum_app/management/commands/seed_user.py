from django.core.management.base import BaseCommand
from sum_app.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Seed the database with multiple students and teachers"

    def handle(self, *args, **kwargs):
        users = [
            # Students
            {
                "name": "Student One",
                "email": "student1@example.com",
                "is_teacher": False,
                "password": "student123",
            },
            {
                "name": "Student Two",
                "email": "student2@example.com",
                "is_teacher": False,
                "password": "student123",
            },
            {
                "name": "Student Three",
                "email": "student3@example.com",
                "is_teacher": False,
                "password": "student123",
            },

            # Teachers
            {
                "name": "Teacher One",
                "email": "teacher1@example.com",
                "is_teacher": True,
                "password": "teacher123",
            },
            {
                "name": "Teacher Two",
                "email": "teacher2@example.com",
                "is_teacher": True,
                "password": "teacher123",
            },
            {
                "name": "Teacher Three",
                "email": "teacher3@example.com",
                "is_teacher": True,
                "password": "teacher123",
            },
        ]

        for data in users:
            if User.objects.filter(email=data["email"]).exists():
                self.stdout.write(self.style.WARNING(f"⚠️ User with email {data['email']} already exists."))
                continue

            user = User.objects.create(
                name=data["name"],
                email=data["email"],
                is_teacher=data["is_teacher"],
                is_approved=True,
                password=make_password(data["password"])
                # user_code will be auto-generated in model
            )

            role = "Teacher" if user.is_teacher else "Student"
            self.stdout.write(self.style.SUCCESS(f"✅ {role} '{user.name}' created successfully with code {user.user_code}!"))
