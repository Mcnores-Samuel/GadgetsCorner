"""This module contains the ContactAdmin class,
which is used to customize the
admin interface for the Contact model.
"""
from django.contrib import admin


class ContactAdmin(admin.ModelAdmin):
    """The `ContactAdmin` class is used to customize the
    admin interface for the Contact model.
    """
    list_display = ('user', 'name', 'email', 'phone', 'address', 'city',
                    'state', 'zip_code', 'current_location')
    search_fields = ('user', 'name', 'email', 'phone', 'address', 'city',
                     'state', 'zip_code', 'current_location')
