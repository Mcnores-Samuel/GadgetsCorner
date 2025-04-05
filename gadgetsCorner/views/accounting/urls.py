from django.urls import path
from gadgetsCorner.views.accounting.revenue import (
    current_year_revenue, revenue_by_category, calculateCreditRevenue,
    lastyearBycurrentMonth, revenue_growth, average_order_value, calculateCashRevenue
)
from gadgetsCorner.views.accounting.accounting import accounting, cost_and_expenses
from gadgetsCorner.views.accounting.assets import add_assets, total_assets
from gadgetsCorner.views.accounting.cost_and_expenses import availableStockCost
from gadgetsCorner.views.accounting.expenses import expenses, get_total_expenses
from gadgetsCorner.views.accounting.liabilities import add_liability, total_liabilities
from gadgetsCorner.views.accounting.networth import networth


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
    path('add_assets/', add_assets, name='add_assets'),
    path('total_assets/', total_assets, name='total_assets'),
    path('availableStockCost/', availableStockCost, name='availableStockCost'),
    path('expenses/', expenses, name='expenses'),
    path('get_total_expenses/', get_total_expenses, name='get_total_expenses'),
    path('add_liability/', add_liability, name='add_liability'),
    path('total_liabilities/', total_liabilities, name='total_liabilities'),
    path('networth/', networth, name='networth'),
]