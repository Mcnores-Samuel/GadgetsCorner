"""This module contains the notifications model,
which is used to store the notifications
"""
from django.db import models
from django.utils import timezone
from .user_profile import UserProfile


class Notifications(models.Model):
    """This class represents the notifications model."""
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE)
    general_notification = models.TextField()
    personal_notification = models.TextField()
    read = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
