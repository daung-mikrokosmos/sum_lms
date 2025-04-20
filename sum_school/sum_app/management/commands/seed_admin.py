from django.core.management.base import BaseCommand
from sum_app.models.admin import Admin
from django.contrib.auth.hashers import make_password
import os

class Command(BaseCommand):
    help = "Seed the database with an admin"

    def handle(self, *args, **kwargs):
        admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        admin_name = os.getenv("ADMIN_NAME", "Admin")

        if not Admin.objects.filter(email=admin_email).exists():
            admin = Admin(
                name=admin_name,
                email=admin_email,
                authority=1,
                admin_code="SUM-A000001",
                password=make_password(admin_password)  # Hash the password
            )
            admin.save()

            self.stdout.write(self.style.SUCCESS("Admin created successfully"))
        else:
            self.stdout.write(self.style.WARNING("Admin already exists"))
