from faker import Faker
from base.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate 20 fake categories'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        for i in range(1, 21):
            category = Category(
                name=fake.unique.word(),
                slug=fake.slug(),
                description=fake.text(),
            )
            category.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully created 20 fake categories.'))
