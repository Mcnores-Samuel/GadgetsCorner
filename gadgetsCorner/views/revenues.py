"""This module contains the views for the revenues app.

The revenues app is responsible for handling the revenue data of the system.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.main_storage import MainStorage
from django.http import JsonResponse
from django.utils import timezone


@login_required
def revenues(request):
    """Display the revenues page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    return render(request, 'users/admin_sites/revenues.html')


@login_required
def updateCreditPrices(request):
    """Update the credit prices."""
    if request.method == 'GET':
        return JsonResponse({'status': 'success'})
    

@login_required
def calculateCreditRevenue(request):
    """Calculate the credit revenue Sort by Month"""
    if request.method == 'GET':
        # Filter MainStorage items
        months = ['January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October',
            'November', 'December']
        revenue = {}
        for month in months:
            items = MainStorage.objects.filter(
                in_stock=False, sold=True, pending=False, missing=False,
                assigned=True, sales_type='Loan', stock_out_date__month=months.index(month)+1,
                stock_out_date__year=timezone.now().year)
            total = sum([item.price for item in items])
            revenue[month] = total
        return JsonResponse(revenue, safe=False)
