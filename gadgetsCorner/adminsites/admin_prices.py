from django.contrib import admin


class AdminYellowPrices(admin.ModelAdmin):
    """This class represents the admin interface for the YellowPrices model.

    Attributes:
      list_display (tuple): The fields to display in the admin interface.
      search_fields (tuple): The fields to search in the admin interface.
      list_filter (tuple): The fields to filter in the admin interface.
      list_per_page (int): The number of items to display per page.
    """
    list_display = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    search_fields = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    list_filter = ('phone_type', 'cost_price', 'selling_price', 'date_added')
    list_per_page = 50

