from django.core.management.base import BaseCommand
from sum_app.models.admin import Admin
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Seed the database with multiple admins"

    def handle(self, *args, **kwargs):
        admin_arr = [
            {
                'name': 'Admin 1',
                'email': 'admin1@gmail.com',
                'authority': 1,
                'password': 'admin123'
            },
            {
                'name': 'Admin 2',
                'email': 'admin2@gmail.com',
                'authority': 2,
                'password': 'admin123'
            },
            {
                'name': 'Admin 3',
                'email': 'admin3@gmail.com',
                'authority': 3,
                'password': 'admin123'
            },
        ]

        for admin_data in admin_arr:
            if Admin.objects.filter(email=admin_data["email"]).exists():
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Admin with email "{admin_data["email"]}" already exists.')
                )
                continue

            admin = Admin(
                name=admin_data["name"],
                email=admin_data["email"],
                authority=admin_data["authority"],
                password=make_password(admin_data["password"])
                # admin_code will be auto-generated in save()
            )
            admin.save()

            self.stdout.write(
                self.style.SUCCESS(f'✅ Admin "{admin.name}" created with code {admin.admin_code}.')
            )
