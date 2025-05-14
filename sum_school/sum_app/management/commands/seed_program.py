from django.core.management.base import BaseCommand
from django.utils import timezone
from sum_app.models import Program
from datetime import date


class Command(BaseCommand):
    help = "Seed initial data for Program model"

    def handle(self, *args, **kwargs):
        programs = [
            {
                "name": "Computer Science Basics",
                "program_code": "CSB",
                "start_date": date(2025, 6, 1),
                "end_date": date(2025, 9, 30),
                "fees": 150000,
            },
            {
                "name": "Advanced Python Programming",
                "program_code": "APP",
                "start_date": date(2025, 7, 15),
                "end_date": date(2025, 10, 15),
                "fees": 200000,
            },
            {
                "name": "Data Science Bootcamp",
                "program_code": "DSB",
                "start_date": date(2025, 8, 1),
                "end_date": date(2025, 11, 30),
                "fees": 250000,
            },
            {
                "name": "Web Development Fundamentals",
                "program_code": "WBF",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Introduction to Python Programming",
                "program_code": "PYT",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Web Development with Django",
                "program_code": "WDJ",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Data Science and Machine Learning",
                "program_code": "DSM",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Digital Marketing Fundamentals",
                "program_code": "DMF",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Android App Development",
                "program_code": "AAD",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Blockchain Basics",
                "program_code": "BLK",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Cloud Computing and AWS",
                "program_code": "CCA",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Cybersecurity Fundamentals",
                "program_code": "CSF",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "UI/UX Design Principles",
                "program_code": "UIX",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Game Development with Unity",
                "program_code": "GDU",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Artificial Intelligence and Deep Learning",
                "program_code": "AID",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Virtual Reality Development",
                "program_code": "VRD",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Networking Fundamentals",
                "program_code": "NET",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Project Management Basics",
                "program_code": "PMB",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Software Testing and Automation",
                "program_code": "STA",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
            {
                "name": "Internet of Things (IoT) Basics",
                "program_code": "IOT",
                "start_date": date(2025, 5, 20),
                "end_date": date(2025, 8, 20),
                "fees": 180000,
            },
        ]

        for prog_data in programs:
            program, created = Program.objects.get_or_create(
                program_code=prog_data["program_code"], defaults=prog_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Program "{program.name}" created.')
                )
            else:
                self.stdout.write(f'Program "{program.name}" already exists.')
