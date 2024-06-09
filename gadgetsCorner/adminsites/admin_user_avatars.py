"""This module registers the UserAvatar model with the admin site."""
from django.contrib import admin


class UserAvatarAdmin(admin.ModelAdmin):
    """UserAvatar admin class for the admin panel."""
    list_display = ('user', 'image')
    search_fields = ('user__username',)

    list_per_page = 20