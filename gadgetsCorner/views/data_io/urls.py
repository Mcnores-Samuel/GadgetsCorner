from django.urls import path
from gadgetsCorner.views.data_io.assets_view import (
    assets_view, update_asset, delete_asset
)
from gadgetsCorner.views.data_io.liability_view import (
    liabilities_view, update_liability, delete_liability, mark_as_paid
)
from gadgetsCorner.views.data_io.expense_view import (
    expense_view, update_expense, delete_expense
)
from gadgetsCorner.views.data_io import sales_register
from gadgetsCorner.views.data_io import add_refarbished

urlpatterns = [
    path('assets_view/', assets_view, name='assets_view'),
    path('update_asset/', update_asset, name='update_asset'),
    path('delete_asset/', delete_asset, name='delete_asset'),
    path('liabilities_view/', liabilities_view, name='liabilities_view'),
    path('update_liability/', update_liability, name='update_liability'),
    path('delete_liability/', delete_liability, name='delete_liability'),
    path('mark_as_paid/', mark_as_paid, name='mark_as_paid'),
    path('expense_view/', expense_view, name='expense_view'),
    path('update_expense/', update_expense, name='update_expense'),
    path('delete_expense/', delete_expense, name='delete_expense'),
    path('refarbished_sales/', sales_register.refarbished_sales, name='refarbished_sales'),
    path('add_refarbished/', add_refarbished.add_refarbished, name='add_refarbished'),
]