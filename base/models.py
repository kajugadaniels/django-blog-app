import os
import random
import string
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.exceptions import ValidationError

def category_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    return f'categories/category_{slugify(instance.name)}_{timestamp}{file_extension}'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    image = ProcessedImageField(
        upload_to=category_image_path,
        processors=[ResizeToFill(800, 800)],
        # format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _generate_unique_slug(self):
        """Generate a unique slug by appending 7 random numbers."""
        base_slug = slugify(self.name)
        slug = f"{base_slug}"
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}"
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else "Unnamed Category"

    class Meta:
        verbose_name_plural = "Categories"

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def _generate_unique_slug(self):
        """Generate a unique slug by appending 7 random numbers."""
        base_slug = slugify(self.name)
        slug = base_slug
        while Tag.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{random.randint(1000, 9999)}"
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tags"

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='articles')
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    language = models.CharField(max_length=50, default='en')
    views = models.PositiveIntegerField(default=0)

    def _generate_unique_slug(self):
        """Generate a unique slug by appending 7 random numbers."""
        base_slug = slugify(self.title)
        slug = base_slug
        while Article.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{random.randint(1000, 9999)}"
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Articles"
