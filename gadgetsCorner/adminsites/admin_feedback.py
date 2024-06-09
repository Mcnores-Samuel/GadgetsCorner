"""This module contains the admin feedback panel view,
which is used to display the feedback panel
"""
from django.contrib import admin


class FeedbackAdmin(admin.ModelAdmin):
    """This model represent the entire stock available and sold in all posts"""
    list_display = ('user', 'read', 'feedback_type', 'feedback', 'date')

    search_fields = ('user__username', 'feedback_type', 'date')

    list_filter = ('feedback_type', 'date', 'read')

    list_per_page = 50