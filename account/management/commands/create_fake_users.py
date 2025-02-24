from faker import Faker
from account.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate 10 fake users with the role of editor'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = []
        
        for _ in range(10):
            user = User(
                email=fake.email(),
                name=fake.name(),
                phone_number=fake.phone_number(),
                role='editor',  # Ensure role is 'editor'
                is_active=True,
                is_staff=False
            )
            user.set_password(fake.password())  # Generate fake password
            user.save()
            users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(users)} users.'))
