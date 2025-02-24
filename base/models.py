import os
import random
import string
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import format_html
from django.contrib.auth.models import User
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.exceptions import ValidationError

def category_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    return f'categories/category_{slugify(instance.name)}_{timestamp}{file_extension}'

def article_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    return f'articles/article_{slugify(instance.name)}_{timestamp}{file_extension}'

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

class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = ProcessedImageField(
        upload_to=article_image_path,
        processors=[ResizeToFill(1080, 600)],
        # format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,
    )
    caption = models.CharField(max_length=255, null=True, blank=True)

    def image_preview(self):
        """Display a thumbnail of the article image in the list view."""
        if self.image:
            return format_html('<img src="{}" width="50" height="50" />', self.image.url)
        return "No image"
    image_preview.short_description = "Image Preview"

    def __str__(self):
        return self.caption if self.caption else "No Caption"

    class Meta:
        verbose_name_plural = "Article Images"

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"

    class Meta:
        verbose_name_plural = "Comments"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('expired', 'Expired')], default='active')
    plan = models.CharField(max_length=50, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')])

    def __str__(self):
        return f"{self.user.username} - {self.plan}"

    class Meta:
        verbose_name_plural = "Subscriptions"

class ArticleSubscription(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    view_permission = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subscription.user.username} - {self.article.title}"

    class Meta:
        verbose_name_plural = "Article Subscriptions"

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_term = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search by {self.user.username} for {self.search_term}"

    class Meta:
        verbose_name_plural = "Search Histories"

class Alert(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    target_users = models.ManyToManyField(User, related_name='alerts')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Alerts"