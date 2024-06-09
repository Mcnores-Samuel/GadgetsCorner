"""This module contains the views for the revenues app.

The revenues app is responsible for handling the revenue data of the system.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.prices import YellowPrices
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
        # Fetch all YellowPrices objects and store them in a dictionary
        prices_dict = {price.phone_type: price for price in YellowPrices.objects.all()}
        
        # Filter MainStorage items
        items = MainStorage.objects.filter(
            in_stock=False, sold=True, pending=False, missing=False,
            assigned=True, sales_type='Loan', price=0.00)
        
        # Iterate through items and update prices
        for item in items:
            price = prices_dict.get(item.phone_type)  # Get price based on phone type
            if price:
                item.price = price.selling_price
            else:
                try:
                    # If no price found, create a new YellowPrices object
                    YellowPrices.objects.create(
                        phone_type=item.phone_type,
                        selling_price=0.00,
                        cost_price=0.00,
                        date_added=timezone.now()
                    )
                except Exception as e:
                    continue
        # Bulk update all items
        MainStorage.objects.bulk_update(items, ['price'])
        
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
