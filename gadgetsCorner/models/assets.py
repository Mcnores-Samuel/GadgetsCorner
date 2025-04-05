"""The model for the fixed assets table.
This module defines the FixedAssets model, which represents
a fixed asset in the system.
It includes fields for the name, description, date purchased,
cost, useful life, salvage value, and depreciation of the asset.
It also includes methods for calculating the total cost and
current value of the assets.
"""
from django.db import models
from django.db.models import Sum


class FixedAssets(models.Model):
    """The model for the fixed assets table.

    Attributes:
        name (CharField): The name of the asset.
        description (TextField): The description of the asset.
        date_purchased (DateTimeField): The date the asset was purchased.
        cost (DecimalField): The cost of the asset.
        useful_life (IntegerField): The useful life of the asset.
        salvage_value (DecimalField): The salvage value of the asset.
        depreciation (DecimalField): The depreciation of the asset.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_purchased = models.DateTimeField()
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    useful_life = models.IntegerField()
    salvage_value = models.DecimalField(max_digits=20, decimal_places=2)
    depreciation = models.DecimalField(max_digits=20, decimal_places=2)


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'fixed_assets'
        verbose_name = 'Fixed Asset'
        verbose_name_plural = 'Fixed Assets'
        indexes = [
            models.Index(fields=['date_purchased'])
        ]

    @classmethod
    def total_assets_cost(cls):
        """Returns the total cost of the assets."""
        total = cls.objects.aggregate(total_cost=Sum('cost'))
        if total['total_cost'] is None:
            return 0
        return total['total_cost']
    
    @classmethod
    def total_assets_current_value(cls):
        """Returns the total current value of the assets."""
        total = cls.objects.aggregate(total_current_value=Sum('depreciation'))
        if total['total_current_value'] is None:
            return 0
        return total['total_current_value']