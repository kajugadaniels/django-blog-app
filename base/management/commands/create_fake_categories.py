from faker import Faker
from base.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate 20 fake categories for a news report system'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Define categories relevant to a news report system
        categories = [
            "Politics", "Environment", "Sports", "Technology", "Health", 
            "Economy", "Education", "Culture", "Entertainment", "Science",
            "International", "Local", "Business", "Environment & Nature", 
            "Agriculture", "Energy", "Travel", "Lifestyle", "Opinion", "Law"
        ]
        
        for i, category_name in enumerate(categories, start=1):  # Create categories with ids from 1 to 20
            category = Category(
                name=category_name,
                slug=fake.slug(),
                description=fake.text(),
            )
            category.save()

        self.stdout.write(self.style.SUCCESS('Successfully created 20 fake categories.'))
