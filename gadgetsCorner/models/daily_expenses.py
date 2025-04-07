""""This module contains the models for the daily_expenses app"""
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum


class DailyExpenses(models.Model):
    """This class represents the DailyExpenses model.
    It stores the daily expenses of the store.

    Attributes:
        name (str): The name of the expense.
        amount (Decimal): The amount of the expense.
        date (DateTime): The date the expense was made.
    """
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.name} - {self.amount}"

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Daily Expenses'

    @classmethod
    def total_expenses(cls):
        """Returns the total expenses."""
        total = cls.objects.filter(
            date__year=timezone.now().year,
        ).aggregate(total_expenses=Sum('amount'))
        if total['total_expenses'] is None:
            return 0
        return total['total_expenses']
    
    @classmethod
    def total_current_month_expenses(cls):
        """Returns the total expenses for the current month."""
        total = cls.objects.filter(
            date__month=timezone.now().month,
            date__year=timezone.now().year
        ).aggregate(total_expenses=Sum('amount'))
        if total['total_expenses'] is None:
            return 0
        return total['total_expenses']