"""This module contains the admin sites for the appliances app."""
from django.contrib import admin


class AppliancesAdmin(admin.ModelAdmin):
    """This class represents the AppliancesAdmin model.
    It is used to customize the admin interface for the Appliances model.
    """
    list_display = ('name', 'model', 'total', 'cost', 'date_added', 'date_modified')
    list_filter = ('name', 'model', 'total', 'cost', 'date_added', 'date_modified')
    search_fields = ('name', 'model', 'total', 'cost', 'date_added', 'date_modified')
    ordering = ('-id',)

    list_per_page = 50


class Appliance_SalesAdmin(admin.ModelAdmin):
    """This class represents the Appliance_SalesAdmin model.
    It is used to customize the admin interface for the Appliance_Sales model.
    """
    list_display = ('sold_by', 'item', 'model', 'total', 'cost', 'price_sold', 'profit', 'date_sold')
    list_filter = ('sold_by', 'item', 'model', 'total', 'cost', 'date_sold')
    search_fields = ('sold_by', 'item', 'model', 'total', 'cost', 'date_sold')
    ordering = ('-id',)

    list_per_page = 50