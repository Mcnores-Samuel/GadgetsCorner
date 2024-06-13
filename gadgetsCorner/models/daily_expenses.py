""""This module contains the models for the daily_expenses app"""
from django.db import models
from django.utils import timezone
from django.conf import settings


class DailyExpenses(models.Model):
    """This class represents the DailyExpenses model.
    It stores the daily expenses of the store.

    Attributes:
        name (str): The name of the expense.
        amount (Decimal): The amount of the expense.
        date (DateTime): The date the expense was made.
    """
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.name} - {self.amount}"

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Daily Expenses'