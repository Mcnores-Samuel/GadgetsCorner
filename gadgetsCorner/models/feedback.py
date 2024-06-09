"""This module contains the feedback model,
which is used to store the feedback
"""
from django.db import models
from django.utils import timezone
from .user_profile import UserProfile


class Feedback(models.Model):
    """This class represents the feedback model."""
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE)
    feedback_type = models.CharField(
        max_length=20)
    feedback = models.TextField()
    read = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return a string representation of the model."""
        return "{}'s feedback".format(self.user)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Feedbacks'