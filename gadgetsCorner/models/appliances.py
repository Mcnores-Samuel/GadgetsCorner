"""This module contains the models for the appliances app"""
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum, F


class Appliances(models.Model):
    """This class represents the Appliances model.
    It stores the appliances available in the store.

    Attributes:
        held_by (ForeignKey): The user who holds the appliance.
        name (str): The name of the appliance.
        model (str): The model of the appliance.
        total (int): The total number of appliances available.
        cost (Decimal): The cost of the appliance.
        date_added (DateTime): The date the appliance was added.
        date_modified (DateTime): The date the appliance was last modified.
    """
    held_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    total = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.name} {self.model}"

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Appliances'


class Appliance_Sales(models.Model):
    """This class represents the Appliance_Sales model.
    It is used to store sales of appliances.

    Attributes:
        sold_by (ForeignKey): The user who sold the appliance.
        item (str): The name of the appliance.
        model (str): The model of the appliance.
        total (int): The total number of appliances sold.
        cost (Decimal): The cost of the appliance.
        date_sold (DateTime): The date the appliance was sold.
    """
    sold_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    item = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    total = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price_sold = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_sold = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.item} {self.model}"

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Appliance Sales'

    @classmethod
    def get_total_sold(cls, month=None, year=None):
        """Get the total number of accessories sold in a specific month and year."""
        total = 0
        if month:
            total = cls.objects.filter(
                date_sold__month=month, date_sold__year=year).aggregate(
                    models.Sum('total'))['total__sum'] or 0
        else:
            total = cls.objects.filter(date_sold__year=year).aggregate(
                models.Sum('total'))['total__sum'] or 0
        if total is None:
            total = 0
        return total
    
    @classmethod
    def get_total_cost(cls, month=None, year=None):
        """Get the total cost of accessories sold in a specific month and year."""
        total = 0
        if month:
            total = cls.objects.filter(
                date_sold__month=month, date_sold__year=year).aggregate(
                    total_cost=models.Sum(F('total') * F('cost')))['total_cost'] or 0
        else:
            total = cls.objects.filter(date_sold__year=year).aggregate(
                total_cost=models.Sum(F('total') * F('cost')))['total_cost'] or 0
        if total is None:
            total = 0
        return total
    
    @classmethod
    def get_revenue(cls, month=None, year=None):
        """Get the total revenue from accessories sold in a specific month and year."""
        total = 0
        if month:
            total = cls.objects.filter(
                date_sold__month=month, date_sold__year=year).aggregate(
                    total_revenue=models.Sum(F('total') * F('price_sold')))['total_revenue'] or 0
        else:
            total = cls.objects.filter(date_sold__year=year).aggregate(
                total_revenue=models.Sum(F('total') * F('price_sold')))['total_revenue'] or 0
        if total is None:
            total = 0
        return total
    
    @classmethod
    def get_profit(cls, month=None, year=None):
        """Get the total profit from accessories sold in a specific month and year."""
        cost = cls.get_total_cost(month, year)
        revenue = cls.get_revenue(month, year)
        profit = revenue - cost
        if profit is None:
            profit = 0
        return profit
