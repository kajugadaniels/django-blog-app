from faker import Faker
from base.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate 50 fake tags'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for i in range(1, 51):
            tag = Tag(
                name=fake.unique.word(),
                slug=fake.slug(),
            )
            tag.save()

        self.stdout.write(self.style.SUCCESS('Successfully created 50 fake tags.'))
