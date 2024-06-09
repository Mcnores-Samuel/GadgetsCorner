"""This module contains the view functions for system routine updates."""
from django.utils import timezone
from ..data_analysis_engine.admin_panel.mainstorage_analysis import MainStorageAnalysis
from ..models.user_profile import UserProfile
from webpush import send_user_notification
from django.http import JsonResponse
from django.core.mail import send_mail
from os import environ

def morning_update(request):
    """The `morning_update` view function sends a morning update to all users.

    Functionality:
    - Sends a morning update to all users.
    - Provides a summary of the previous day's sales and stock status.
    - Sends a notification to all users.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Sends a morning update to all users.
    - Sends a notification to all users.

    Usage:
    - This view is executed as a scheduled task to provide a morning update to all users.
    - The morning update includes a summary of the previous day's sales and stock status.
    """
    if request.method == 'GET':
        # Get the previous day's date
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        # Get the daily sales data
        main_storage_analysis = MainStorageAnalysis()
        daily_sales_cash = main_storage_analysis.get_daily_sales('Cash', day=yesterday)
        daily_sales_loan = main_storage_analysis.get_daily_sales('Loan', day=yesterday)

        # Get the weekly sales data
        weekly_sales_cash = main_storage_analysis.get_weekly_sales('Cash')
        weekly_sales_loan = main_storage_analysis.get_weekly_sales('Loan')

        # Get the monthly sales data by agents
        monthly_sales_cash = main_storage_analysis.get_monthly_sales_by_agents('Cash')
        monthly_sales_loan = main_storage_analysis.get_monthly_sales_by_agents('Loan')

        # Send a morning update email
        yesterday = yesterday.strftime('%d %B, %Y')
        subject = 'Morning Update For Yesterday - {}'.format(yesterday)
        message = 'Morning Update - Yesterday On: {}\n\n'.format(yesterday)
        message += 'Daily Sales (Cash): {}\n'.format(len(daily_sales_cash))
        message += 'Daily Sales (Loan): {}\n'.format(len(daily_sales_loan))
        message += 'Weekly Sales (Cash): {}\n'.format(
            len(weekly_sales_cash['Monday'] + weekly_sales_cash['Tuesday'] +
                weekly_sales_cash['Wednesday'] + weekly_sales_cash['Thursday'] +
                weekly_sales_cash['Friday'] + weekly_sales_cash['Saturday'] +
                weekly_sales_cash['Sunday']))
        message += 'Weekly Sales (Loan): {}\n'.format(
            len(weekly_sales_loan['Monday'] + weekly_sales_loan['Tuesday'] +
                weekly_sales_loan['Wednesday'] + weekly_sales_loan['Thursday'] +
                weekly_sales_loan['Friday'] + weekly_sales_loan['Saturday'] +
                weekly_sales_loan['Sunday']))
        message += 'Total Current Monthly Sales (Cash): {}\n'.format(monthly_sales_cash[0][1])
        message += 'Total Current Monthly Sales (Loan): {}\n'.format(monthly_sales_loan[0][1])
        message += 'log in to the system to view more details. www.hafeezmw.com\n\n'
        message += 'Thank you for your hard work!\n\n'
        message += 'Hafeez Enterprise Team'
        from_email = 'noreply.hafeezmw@gmail.com'
        admin = UserProfile.objects.filter(is_staff=True, is_superuser=True, is_active=True)
        recipient_list = [admin.email for admin in admin]
        send_mail(subject, message, from_email, recipient_list)
        for admin in admin:
            send_user_notification(
                user=admin, payload={
                    "head": "Morning Update", "body": message,
                    'icon': environ.get('ICON_LINK')})
        return JsonResponse({'status': 'Morning update sent successfully.'})
    return JsonResponse({'status': 'Invalid request method.'})


def afternoon_update(request):
    """The `afternoon_update` view function sends an afternoon update to all users.

    Functionality:
    - Sends an afternoon update to all users.
    - Provides a summary of the current day's sales and stock status.
    - Sends a notification to all users.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Sends an afternoon update to all users.
    - Sends a notification to all users.

    Usage:
    - This view is executed as a scheduled task to provide an afternoon update to all users.
    - The afternoon update includes a summary of the current day's sales and stock status.
    """
    if request.method == 'GET':
        # Get the current day's date
        today = timezone.now().date()
        # Get the daily sales data
        main_storage_analysis = MainStorageAnalysis()
        daily_sales_cash = main_storage_analysis.get_daily_sales('Cash', day=today)
        daily_sales_loan = main_storage_analysis.get_daily_sales('Loan', day=today)

        # Get the weekly sales data
        weekly_sales_cash = main_storage_analysis.get_weekly_sales('Cash')
        weekly_sales_loan = main_storage_analysis.get_weekly_sales('Loan')

        # Get the monthly sales data by agents
        monthly_sales_cash = main_storage_analysis.get_monthly_sales_by_agents('Cash')
        monthly_sales_loan = main_storage_analysis.get_monthly_sales_by_agents('Loan')

        # Send an afternoon update email
        today = today.strftime('%d %B, %Y')
        subject = 'Afternoon Update - {}'.format(today)
        message = 'Afternoon Update - For Today On: {}\n\n'.format(today)
        message += 'Daily Sales (Cash): {}\n'.format(len(daily_sales_cash))
        message += 'Daily Sales (Loan): {}\n'.format(len(daily_sales_loan))
        message += 'Weekly Sales (Cash): {}\n'.format(
            len(weekly_sales_cash['Monday'] + weekly_sales_cash['Tuesday'] +
                weekly_sales_cash['Wednesday'] + weekly_sales_cash['Thursday'] +
                weekly_sales_cash['Friday'] + weekly_sales_cash['Saturday'] +
                weekly_sales_cash['Sunday']))
        message += 'Weekly Sales (Loan): {}\n'.format(
            len(weekly_sales_loan['Monday'] + weekly_sales_loan['Tuesday'] +
                weekly_sales_loan['Wednesday'] + weekly_sales_loan['Thursday'] +
                weekly_sales_loan['Friday'] + weekly_sales_loan['Saturday'] +
                weekly_sales_loan['Sunday']))
        message += 'Total Current Monthly Sales (Cash): {}\n'.format(monthly_sales_cash[0][1])
        message += 'Total Current Monthly Sales (Loan): {}\n'.format(monthly_sales_loan[0][1])
        message += 'log in to the system to view more details. www.hafeezmw.com\n\n'
        message += 'Thank you for your hard work!\n\n'
        message += 'Hafeez Enterprise Team'
        from_email = 'noreply.hafeezmw@gmail.com'
        admin = UserProfile.objects.filter(is_staff=True, is_superuser=True, is_active=True)
        recipient_list = [admin.email for admin in admin]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        for admin in admin:
            send_user_notification(
                user=admin, payload={
                    "head": "Morning Update", "body": message,
                    'icon': environ.get('ICON_LINK')})
        return JsonResponse({'status': 'Afternoon update sent successfully.'})
    return JsonResponse({'status': 'Invalid request method.'})


def evening_update(request):
    """The `evening_update` view function sends an evening update to all users.

    Functionality:
    - Sends an evening update to all users.
    - Provides a summary of the current day's sales and stock status.
    - Sends a notification to all users.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Sends an evening update to all users.
    - Sends a notification to all users.

    Usage:
    - This view is executed as a scheduled task to provide an evening update to all users.
    - The evening update includes a summary of the current day's sales and stock status.
    """
    if request.method == 'GET':
        # Get the current day's date
        today = timezone.now().date()
        # Get the daily sales data
        main_storage_analysis = MainStorageAnalysis()
        daily_sales_cash = main_storage_analysis.get_daily_sales('Cash', day=today)
        daily_sales_loan = main_storage_analysis.get_daily_sales('Loan', day=today)

        # Get the weekly sales data
        weekly_sales_cash = main_storage_analysis.get_weekly_sales('Cash')
        weekly_sales_loan = main_storage_analysis.get_weekly_sales('Loan')

        # Get the monthly sales data by agents
        monthly_sales_cash = main_storage_analysis.get_monthly_sales_by_agents('Cash')
        monthly_sales_loan = main_storage_analysis.get_monthly_sales_by_agents('Loan')

        # Send an evening update email
        today = today.strftime('%d %B, %Y')
        subject = 'Evening Update - {}'.format(today)
        message = 'Evening Update - {}\n\n'.format(today)
        message += 'Daily Sales (Cash): {}\n'.format(len(daily_sales_cash))
        message += 'Daily Sales (Loan): {}\n'.format(len(daily_sales_loan))
        message += 'Weekly Sales (Cash): {}\n'.format(
            len(weekly_sales_cash['Monday'] + weekly_sales_cash['Tuesday'] +
                weekly_sales_cash['Wednesday'] + weekly_sales_cash['Thursday'] +
                weekly_sales_cash['Friday'] + weekly_sales_cash['Saturday'] +
                weekly_sales_cash['Sunday']))
        message += 'Weekly Sales (Loan): {}\n'.format(
            len(weekly_sales_loan['Monday'] + weekly_sales_loan['Tuesday'] +
                weekly_sales_loan['Wednesday'] + weekly_sales_loan['Thursday'] +
                weekly_sales_loan['Friday'] + weekly_sales_loan['Saturday'] +
                weekly_sales_loan['Sunday']))
        message += 'Total Current Monthly Sales (Cash): {}\n'.format(monthly_sales_cash[0][1])
        message += 'Total Current Monthly Sales (Loan): {}\n'.format(monthly_sales_loan[0][1])
        message += 'log in to the system to view more details. www.hafeezmw.com\n\n'
        message += 'Thank you for your hard work!\n\n'
        message += 'Hafeez Enterprise Team'
        from_email = 'noreply.hafeezmw@gmail.com'
        admin = UserProfile.objects.filter(is_staff=True, is_superuser=True, is_active=True)
        recipient_list = [admin.email for admin in admin]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        for admin in admin:
            send_user_notification(
                user=admin, payload={
                    "head": "Morning Update", "body": message,
                    'icon': environ.get('ICON_LINK')})
        return JsonResponse({'status': 'Evening update sent successfully.'})
    return JsonResponse({'status': 'Invalid request method.'})
    