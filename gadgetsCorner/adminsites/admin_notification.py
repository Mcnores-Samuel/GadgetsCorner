"""This module contains the admin notification panel view,
which is used to display the notification panel
"""
from django.contrib import admin


class NotificationsAdmin(admin.ModelAdmin):
    """This model represent the entire stock available and sold in all posts"""
    list_display = ('user', 'general_notification', 'personal_notification',
                    'read', 'date')

    search_fields = ('user__username', 'general_notification',
                     'personal_notification', 'date')

    list_filter = ('read', 'date')

    list_per_page = 50