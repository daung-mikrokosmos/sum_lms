from django.core.management.base import BaseCommand
from sum_app.models import User
from django.contrib.auth.hashers import make_password
import os

class Command(BaseCommand):
    help = "Seed the database with an admin user"

    def handle(self, *args, **kwargs):
        admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        admin_name = os.getenv("ADMIN_NAME", "Admin")

        if not User.objects.filter(email=admin_email).exists():
            admin = User(
                name=admin_name,
                email=admin_email,
                is_admin=True,
                user_code="ADMIN001",
                password=make_password(admin_password)  # Hash the password
            )
            admin.save()

            self.stdout.write(self.style.SUCCESS("Admin user created successfully"))
        else:
            self.stdout.write(self.style.WARNING("Admin user already exists"))
