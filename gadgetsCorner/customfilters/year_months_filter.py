from django.utils.translation import gettext_lazy as _
from calendar import month_name
from datetime import datetime
from django.contrib import admin

class YearMonthFilter(admin.SimpleListFilter):
    """This class contains the year month filter
    for the main storage model.

    Attributes:
        title (str): The title of the filter.
        parameter_name (str): The parameter name of the filter.
    """
    title = _('Stock Out Date (Year-Month)')
    parameter_name = 'stock_out_date_year_month'

    def lookups(self, request, model_admin):
        months = [(str(i), month_name[i]) for i in range(1, 13)]
        return months

    def queryset(self, request, queryset):
        if self.value():
            year = datetime.now().year
            month = int(self.value())
            return queryset.filter(stock_out_date__year=year, stock_out_date__month=month)