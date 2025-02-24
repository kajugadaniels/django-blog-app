from django import forms
from base.models import *
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget

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

class ArticleAdminForm(forms.ModelForm):
    """Custom form for Article admin to use CKEditor on content field."""
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget(),  # Use CKEditor widget for content field
        }

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1
    fields = ['image', 'caption', 'image_preview']
    readonly_fields = ['image_preview']  # Make the image preview readonly

    def image_preview(self, obj):
        """Display a thumbnail of the article image in the inline form."""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image Preview"

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm  # Specify the custom form for CKEditor
    list_display = ('title', 'slug', 'author', 'category', 'status', 'published_at', 'image_preview', 'edit_link', 'delete_link')
    search_fields = ('title', 'content', 'author__username', 'category__name')
    list_filter = ('status', 'published_at', 'category')
    list_per_page = 20
    inlines = [ArticleImageInline]  # Inline the ArticleImage model into the ArticleAdmin

    # This method adds an image preview column in the list display
    def image_preview(self, obj):
        """Display a thumbnail of the article image in the list view."""
        if obj.articleimage_set.first():  # Check if an article image exists for the article
            return format_html('<img src="{}" width="50" height="50" />', obj.articleimage_set.first().image.url)
        return "No image"
    image_preview.short_description = "Image Preview"

    def edit_link(self, obj):
        url = reverse("admin:base_article_change", args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_link.short_description = "Edit"
    
    def delete_link(self, obj):
        url = reverse("admin:base_article_delete", args=[obj.pk])
        return format_html('<a class="button" href="{}">Delete</a>', url)
    delete_link.short_description = "Delete"

# @admin.register(ArticleImage)
# class ArticleImageAdmin(admin.ModelAdmin):
#     list_display = ('article', 'image_preview', 'caption', 'edit_link', 'delete_link')
#     search_fields = ('article__title', 'caption')
#     list_filter = ('article',)
#     list_per_page = 20

#     def image_preview(self, obj):
#         """Display a thumbnail of the article image in the list view."""
#         if obj.image:
#             return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
#         return "No image"
#     image_preview.short_description = "Image Preview"

#     def edit_link(self, obj):
#         url = reverse("admin:base_articleimage_change", args=[obj.pk])
#         return format_html('<a class="button" href="{}">Edit</a>', url)
#     edit_link.short_description = "Edit"
    
#     def delete_link(self, obj):
#         url = reverse("admin:base_articleimage_delete", args=[obj.pk])
#         return format_html('<a class="button" href="{}">Delete</a>', url)
#     delete_link.short_description = "Delete"

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

@admin.register(ArticleSubscription)
class ArticleSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('article', 'subscription', 'view_permission', 'edit_link', 'delete_link')
    search_fields = ('article__title', 'subscription__user__username')
    list_filter = ('view_permission',)
    list_per_page = 20

    def edit_link(self, obj):
        url = reverse("admin:base_articlesubscription_change", args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_link.short_description = "Edit"
    
    def delete_link(self, obj):
        url = reverse("admin:base_articlesubscription_delete", args=[obj.pk])
        return format_html('<a class="button" href="{}">Delete</a>', url)
    delete_link.short_description = "Delete"

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_term', 'created_at', 'edit_link', 'delete_link')
    search_fields = ('user__username', 'search_term')
    list_filter = ('created_at',)
    list_per_page = 20

    def edit_link(self, obj):
        url = reverse("admin:base_searchhistory_change", args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_link.short_description = "Edit"
    
    def delete_link(self, obj):
        url = reverse("admin:base_searchhistory_delete", args=[obj.pk])
        return format_html('<a class="button" href="{}">Delete</a>', url)
    delete_link.short_description = "Delete"

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_active', 'edit_link', 'delete_link')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'is_active')
    list_per_page = 20

    def edit_link(self, obj):
        url = reverse("admin:base_alert_change", args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_link.short_description = "Edit"
    
    def delete_link(self, obj):
        url = reverse("admin:base_alert_delete", args=[obj.pk])
        return format_html('<a class="button" href="{}">Delete</a>', url)
    delete_link.short_description = "Delete"