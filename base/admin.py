from django import forms
from base.models import *
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'edit_link', 'delete_link')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    list_per_page = 20

    def image_preview(self, obj):
        """Display a thumbnail of the category image in the list view."""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image Preview"

    def edit_link(self, obj):
        url = reverse("admin:base_category_change", args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_link.short_description = "Edit"
    
    def delete_link(self, obj):
        url = reverse("admin:base_category_delete", args=[obj.pk])
        return format_html('<a class="button" href="{}">Delete</a>', url)
    delete_link.short_description = "Delete"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'edit_link', 'delete_link')
    search_fields = ('name',)
    list_filter = ('name',)
    list_per_page = 20

    def edit_link(self, obj):
        url = reverse("admin:base_tag_change", args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_link.short_description = "Edit"
    
    def delete_link(self, obj):
        url = reverse("admin:base_tag_delete", args=[obj.pk])
        return format_html('<a class="button" href="{}">Delete</a>', url)
    delete_link.short_description = "Delete"

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'category', 'status', 'published_at', 'edit_link', 'delete_link')
    search_fields = ('title', 'content', 'author__username', 'category__name')
    list_filter = ('status', 'published_at', 'category')
    list_per_page = 20

    def edit_link(self, obj):
        url = reverse("admin:base_article_change", args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_link.short_description = "Edit"
    
    def delete_link(self, obj):
        url = reverse("admin:base_article_delete", args=[obj.pk])
        return format_html('<a class="button" href="{}">Delete</a>', url)
    delete_link.short_description = "Delete"

@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('article', 'image_preview', 'caption', 'edit_link', 'delete_link')
    search_fields = ('article__title', 'caption')
    list_filter = ('article',)
    list_per_page = 20

    def image_preview(self, obj):
        """Display a thumbnail of the article image in the list view."""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image Preview"

    def edit_link(self, obj):
        url = reverse("admin:base_articleimage_change", args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_link.short_description = "Edit"
    
    def delete_link(self, obj):
        url = reverse("admin:base_articleimage_delete", args=[obj.pk])
        return format_html('<a class="button" href="{}">Delete</a>', url)
    delete_link.short_description = "Delete"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'content', 'created_at', 'edit_link', 'delete_link')
    search_fields = ('article__title', 'user__username', 'content')
    list_filter = ('created_at', 'updated_at', 'article')
    list_per_page = 20

    def edit_link(self, obj):
        url = reverse("admin:base_comment_change", args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_link.short_description = "Edit"
    
    def delete_link(self, obj):
        url = reverse("admin:base_comment_delete", args=[obj.pk])
        return format_html('<a class="button" href="{}">Delete</a>', url)
    delete_link.short_description = "Delete"

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'status', 'edit_link', 'delete_link')
    search_fields = ('user__username', 'plan')
    list_filter = ('status', 'start_date', 'end_date')
    list_per_page = 20

    def edit_link(self, obj):
        url = reverse("admin:base_subscription_change", args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_link.short_description = "Edit"
    
    def delete_link(self, obj):
        url = reverse("admin:base_subscription_delete", args=[obj.pk])
        return format_html('<a class="button" href="{}">Delete</a>', url)
    delete_link.short_description = "Delete"