"""This file is used to register the models in the admin site for the accessories app"""
from django.contrib import admin


class AdminAccessories(admin.ModelAdmin):
    """This class is used to register the models in the admin site for the accessories app"""
    list_display = ('held_by', 'item', 'model', 'total', 'previous_total', 'cost_per_item', 'date_added', 'date_modified')
    search_fields = ('held_by', 'item', 'model', 'total', 'previous_total', 'cost_per_item', 'date_added', 'date_modified')
    list_filter = ('held_by', 'item', 'model', 'total', 'previous_total', 'cost_per_item', 'date_added', 'date_modified')

    list_per_page = 50

    class Meta:
        ordering = ['-item']


class AdminAccessary_Sales(admin.ModelAdmin):
    """This class is used to register the models in the admin site for the accessories app"""
    list_display = ('item', 'model', 'total', 'cost', 'price_sold', 'profit', 'date_sold', 'sold_by')
    search_fields = ('item', 'model', 'sold_by', 'date_sold')
    list_filter = ('item', 'model', 'cost', 'date_sold', 'sold_by')

    list_per_page = 50

    class Meta:
        ordering = ['-item']