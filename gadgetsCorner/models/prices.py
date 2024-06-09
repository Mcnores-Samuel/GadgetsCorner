"""This module contains the YellowPrices class which is used to
store the prices of the products in the system.
"""
from django.db import models
from django.utils import timezone


class YellowPrices(models.Model):
    """This class contains the prices of the products in the system."""
    phone_type = models.CharField(max_length=50, unique=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Yellow Prices"

    def __str__(self):
        return "{} set at {}".format(self.phone_type, self.selling_price)
    