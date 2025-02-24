from faker import Faker
from base.models import *
from account.models import *
import random
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate 100 fake articles for a news report system'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Define article categories and their content themes
        east_african_countries = ['Rwanda', 'Kenya', 'Tanzania', 'Burundi', 'DRC']
        fake_content = [
            "The government of {country} has launched a new initiative to boost local businesses amidst the global recession.",
            "Experts in {country} have warned about the rising temperatures affecting agriculture and food security in rural areas.",
            "The {country} economy has been heavily impacted by the recent political instability, and experts are calling for urgent reforms.",
            "Despite challenges, {country} continues to expand its infrastructure with new roads and railways enhancing trade routes across the region.",
            "Sports enthusiasts in {country} are excited for the upcoming international football tournament, where the national team hopes to qualify."
        ]

        for i in range(1, 101):  # Generate 100 articles with ids from 1 to 100
            author = random.choice(User.objects.filter(role='editor'))  # Random user (editor role)
            category = random.choice(Category.objects.all())  # Random category from predefined categories
            tags = random.sample(list(Tag.objects.all()), 3)  # Random 3 tags
            
            article = Article(
                title=fake.sentence(),
                slug=fake.slug(),
                content=fake_content[random.randint(0, 4)].format(country=random.choice(east_african_countries)),
                author=author,
                category=category,
                published_at=fake.date_this_year(),
                status='published',
                language='en',
                views=random.randint(100, 5000)
            )
            article.save()
            
            # Add tags to the article
            article.tags.set(tags)
            
            # Create fake article image
            article_image = ArticleImage(
                article=article,
                image=fake.image_url(width=1080, height=600),  # Placeholder image URL
                caption=fake.sentence()
            )
            article_image.save()

        self.stdout.write(self.style.SUCCESS('Successfully created 100 fake articles with images.'))
