"""This module contains the Contact class,
which is used to represent a contacts details
for all users in the system.
"""
from django.db import models
from .user_profile import UserProfile


class Contact(models.Model):
    """A class used to represent a contact.

    Attributes:
        user (UserProfile): The user profile of the contact.
        name (str): The name of the contact.
        email (str): The email address of the contact.
        phone (str): The phone number of the contact.
        address (str): The address of the contact.
        city (str): The city of the contact.
        state (str): The state of the contact.
        zip_code (str): The zip code of the contact.
        current_location (str): The current location of the contact.
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    current_location = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        """Return the string representation of the contact."""
        return self.name
