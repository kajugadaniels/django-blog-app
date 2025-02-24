from faker import Faker
from base.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate 50 fake tags for a news report system'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Define tags relevant to a news report system
        tags = [
            "Climate Change", "Global Warming", "Sustainability", "Renewable Energy", "Green Tech", 
            "Agriculture", "Urbanization", "Wildlife", "Deforestation", "Pollution", 
            "Politics", "Election", "Corruption", "International Relations", "Crisis", 
            "Peace", "Security", "War", "Sports", "Football", "Basketball",
            "Technology", "Innovation", "Healthcare", "Economy", "Financial Crisis",
            "Youth", "Women Empowerment", "Mental Health", "Climate Action", "Carbon Emissions",
            "Energy Crisis", "Urban Development", "Disasters", "Floods", "Drought", 
            "Cybersecurity", "Data Privacy", "Tech Companies", "Artificial Intelligence", 
            "Digital Transformation", "Social Media", "Education", "Student Rights", "Literacy",
            "Human Rights", "Cultural Heritage", "Peacekeeping", "Humanitarian Efforts", 
            "Migration", "Refugees", "Agribusiness", "Water Resources"
        ]
        
        for i, tag_name in enumerate(tags, start=1):  # Create tags with ids from 1 to 50
            tag = Tag(
                name=tag_name,
                slug=fake.slug(),
            )
            tag.save()

        self.stdout.write(self.style.SUCCESS('Successfully created 50 fake tags.'))
