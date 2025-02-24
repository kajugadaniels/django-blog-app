from account.models import *
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone_number', 'role', 'is_active', 'is_staff', 'image_preview', 'edit_link', 'delete_link')
    search_fields = ('email', 'name', 'phone_number', 'role')
    list_filter = ('role', 'is_active', 'is_staff', 'created_at')
    list_per_page = 20

    def image_preview(self, obj):
        """Display a thumbnail of the user image in the list view."""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image Preview"

    def edit_link(self, obj):
        url = reverse("admin:account_user_change", args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_link.short_description = "Edit"
    
    def delete_link(self, obj):
        url = reverse("admin:account_user_delete", args=[obj.pk])
        return format_html('<a class="button" href="{}">Delete</a>', url)
    delete_link.short_description = "Delete"
