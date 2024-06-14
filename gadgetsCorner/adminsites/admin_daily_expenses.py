"""This module contains the admin sites for the daily_expenses app."""
from django.contrib import admin


class DailyExpensesAdmin(admin.ModelAdmin):
    """This class represents the DailyExpensesAdmin model.
    It is used to customize the admin interface for the DailyExpenses model.
    """
    list_display = ('added_by', 'name', 'amount', 'date')
    list_filter = ('date',)
    search_fields = ('name', 'amount', 'date')
    ordering = ('-id',)

    list_per_page = 50