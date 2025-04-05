"""The model for the liability table.
This module defines the `Liability` model, which represents a liability in the system.
It includes fields for the type of liability, creditor, amount, description, effective date,
due date, and whether the liability has been paid.
It also includes methods for calculating the total current and non-current liabilities.
"""
from django.db import models
from django.db.models import Sum


class Liability(models.Model):
    """The model for the liability table.

    Attributes:
        type (CharField): The type of liability.
        creditor (CharField): The creditor of the liability.
        amount (DecimalField): The amount of the liability.
        description (TextField): The description of the liability.
        effective_date (DateTimeField): The date the liability commenced.
        due_date (DateTimeField): The date the liability is due.
        is_paid (BooleanField): Whether the liability has been paid.
    """
    LIABILITIES_TYPE = [
        ('current', 'Current Liability'),
        ('non_current', 'Non-Current Liability')
    ]

    type = models.CharField(max_length=255, choices=LIABILITIES_TYPE)
    creditor = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    effective_date = models.DateTimeField()
    due_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date_paid = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.creditor} - {self.amount}'
    
    class Meta:
        db_table = 'liabilities'
        verbose_name = 'Liability'
        verbose_name_plural = 'Liabilities'
        indexes = [
            models.Index(fields=['effective_date'])
        ]

    @classmethod
    def total_current_liabilities(cls):
        """Returns the total current liabilities."""
        total = cls.objects.filter(
            type='current',
            is_paid=False
        ).aggregate(total_current_liabilities=Sum('amount'))
        if total['total_current_liabilities'] is None:
            return 0
        return total['total_current_liabilities']
    
    @classmethod
    def total_non_current_liabilities(cls):
        """Returns the total non-current liabilities."""
        total = cls.objects.filter(
            type='non_current',
            is_paid=False
        ).aggregate(total_non_current_liabilities=Sum('amount'))
        if total['total_non_current_liabilities'] is None:
            return 0
        return total['total_non_current_liabilities']