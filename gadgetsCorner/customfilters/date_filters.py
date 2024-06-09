from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
from django.contrib import admin


class YesterdayFilter(admin.SimpleListFilter):
    """This class contains the yesterday filter"""
    title = _('Entry Date (Yesterday)')
    parameter_name = 'entry_date_yesterday'

    def lookups(self, request, model_admin):
        return (
            ('yesterday', _('Yesterday')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yesterday':
            yesterday = date.today() - timedelta(days=1)
            return queryset.filter(entry_date=yesterday)