"""This module contains the sales target model,
which is used to store the sales target
"""
from django.db import models
from django.utils import timezone


class SalesTarget(models.Model):
    """This class represents the sales target model.
    It is used to store the sales target for each month.
    Attributes:
        target (Decimal): The sales target for the month.
        achieved (Decimal): The sales achieved for the month.
        month (str): The month of the year.
        year (int): The year.
    """
    target = models.DecimalField(max_digits=10, decimal_places=2)
    achieved = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField(default=timezone.now().month)
    year = models.IntegerField(default=timezone.now().year)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.month}/{self.year} - Target: {self.target}, Achieved: {self.achieved}"
    class Meta:
        ordering = ['-year', '-month']
        verbose_name_plural = 'Sales Targets'
        unique_together = ('month', 'year')
        verbose_name = 'Sales Target'

    @classmethod
    def get_sales_target(cls, month, year):
        """Get the sales target for a specific month and year."""
        try:
            return cls.objects.get(month=month, year=year)
        except cls.DoesNotExist:
            return None
        
    @classmethod
    def create_sales_target(cls, target=100,
                            month=timezone.now().month,
                            year=timezone.now().year):
        """Create a new sales target."""
        sales_target = cls.objects.filter(month=month, year=year).first()
        if sales_target:
            return sales_target
        # If no sales target exists for the month and year, create a new one
        if target <= 0:
            target = 100
        sales_target = cls(target=target, achieved=0, month=month, year=year)
        sales_target.save()
        return sales_target
    
    @classmethod
    def add_sales_achieved(cls, month, year, amount):
        """Add sales achieved for a specific month and year."""
        try:
            sales_target = cls.objects.get(month=month, year=year)
            sales_target.achieved = amount
            sales_target.save()
            return sales_target
        except cls.DoesNotExist:
            return None
        
    @classmethod
    def progress(cls, month, year):
        """Get the progress of sales for a specific month and year."""
        try:
            sales_target = cls.objects.get(month=month, year=year)
            return sales_target.achieved / sales_target.target * 100
        except cls.DoesNotExist:
            return None