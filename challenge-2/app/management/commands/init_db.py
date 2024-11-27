from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Populates the user database with dummy data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin',
            type=str,
            help='Admin password file location',
        )

    def handle(self, *args, **kwargs):
        pass_path = kwargs['admin']

        # Admin setup 
        with open(pass_path, 'r') as f:
            password = f.read().strip().replace('\n', '')

        User.objects.create(
            username='admin',
            password=password
        )

        # Dummy entries
        fake = Faker()
        for _ in range(10):
            User.objects.create(
                username=fake.user_name(),
                password=fake.password(length=20)
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully set up db.'))
