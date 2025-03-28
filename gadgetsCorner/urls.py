from django.urls import path
from django.contrib.auth import views as auth_views

from .views.data_io import data_updates

from .views.auth import registration_view

from .views.analytics import data_for_charts, sales_register
from .views import (central_display, home_page, user_dashboard, search_and_filters)
from .views.stock_analysis import (get_source_stock, get_yearly_product_sales, admin_stock_analysis)
from .views.feedback import feedback
from .views.data_io.add_to_stock import add_to_stock, add_accessaries, add_appliances
from .views.pending_sales import total_pending_sales, revert_to_stock, pending_sales
from .views.defects import defects
from  .views import revenues
from .views.system_routine_updates import system_routine_update
from .views.data_io.daily_expenses import add_daily_expense


urlpatterns = [
    # home page
    path('', home_page.home_page, name='home_page'),
    # registration
    path('sign_up/', registration_view.sign_up, name='sign_up'),
    path('sign_in/', registration_view.sign_in, name='sign_in'),
    path('sign_out/', registration_view.sign_out, name='sign_out'),
    path('resend_confirmation_email', registration_view.resend_confirmation_email, name='resend_confirmation_email'),
    # Data on actions on data and admin panel
    path('dashboard/', user_dashboard.dashboard, name='dashboard'),
    path('main_stock_details/', central_display.main_stock_details, name='main_stock_details'),
    path('main_sales_details/', central_display.main_sales_details, name='main_sales_details'),
    path('uploadBulkSales/', sales_register.uploadBulkSales, name='uploadBulkSales'),
    path('accessary_sales/', sales_register.accessary_sales, name='accessary_sales'),
    path('appliance_sales/', sales_register.appliance_sales, name='appliance_sales'),
    path('revenues/', revenues.revenues, name='revenues'),
    path('revert_to_stock/', revert_to_stock, name='revert_to_stock'),
    path('pending_sales/', pending_sales, name='pending_sales'),
    path('add_daily_expense/', add_daily_expense, name='add_daily_expense'),
    path('defects/', defects, name='defects'),
    # General access points
    path('profile/', data_updates.profile, name='profile'),
    path('feedback/', feedback, name='feedback'),
    path('add_to_stock/', add_to_stock, name='add_to_stock'),
    path('add_accessaries/', add_accessaries, name='add_accessaries'),
    path('add_appliances/', add_appliances, name='add_appliances'),
    path('data_search/', search_and_filters.data_search, name='data_search'),
    path('upload_image/', data_updates.upload_image, name='upload_image'),
    path('change_password/', data_updates.change_password, name='change_password'),
    path('combinedData_collection/<int:data_id>/', sales_register.combinedData_collection, name='combinedData_collection'),
    path('add_contract_number/', data_updates.add_contract_number, name='add_contract_number'),
    # Concurent system operations with data analysis
    path('get_daily_sales_json/', data_for_charts.get_daily_sales_json, name='get_daily_sales_json'),
    path('get_weekly_sales_json/', data_for_charts.get_weekly_sales_json, name='get_weekly_sales_json'),
    path('get_monthly_sales/', data_for_charts.get_monthly_sales, name='get_monthly_sales'),
    path('get_source_stock/', get_source_stock, name='get_source_stock'),
    path('get_yearly_product_sales/', get_yearly_product_sales, name='get_yearly_product_sales'),
    path('get_main_stock_analysis/', data_for_charts.get_main_stock_analysis, name='get_main_stock_analysis'),
    path('admin_stock_analysis/', admin_stock_analysis, name='admin_stock_analysis'),
    path('total_pending_sales/', total_pending_sales, name='total_pending_sales'),
    path('get_yearly_sales_total/', data_for_charts.get_yearly_sales_total, name='get_yearly_sales_total'),
    #system email and notifications auto updates
    path('system_routine_update/', system_routine_update, name='system_routine_update'),
    # Revenue analysis and concurent operations
    path('updateCreditPrices/', revenues.updateCreditPrices, name='updateCreditPrices'),
    path('calculateCreditRevenue/', revenues.calculateCreditRevenue, name='calculateCreditRevenue'),
    # reseting user password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_complete.html'), name='password_reset_complete'),
]