from django.urls import path
from gadgetsCorner.views.accounting.revenue import (
    current_year_revenue, revenue_by_category, calculateCreditRevenue,
    lastyearBycurrentMonth, revenue_growth, average_order_value, calculateCashRevenue
)
from gadgetsCorner.views.accounting.accounting import accounting, cost_and_expenses

urlpatterns = [
    path('accounting/', accounting, name='accounting'),
    path('cost_and_expenses/', cost_and_expenses, name='cost_and_expenses'),
    path('current_year_revenue/', current_year_revenue, name='current_year_revenue'),
    path('revenue_by_category/', revenue_by_category, name='revenue_by_category'),
    path('calculateCreditRevenue/', calculateCreditRevenue, name='calculateCreditRevenue'),
    path('lastyearBycurrentMonth/', lastyearBycurrentMonth, name='lastyearBycurrentMonth'),
    path('revenue_growth/', revenue_growth, name='revenue_growth'),
    path('average_order_value/', average_order_value, name='average_order_value'),
    path('calculateCashRevenue/', calculateCashRevenue, name='calculateCashRevenue'),
]