"""This module contains the views for the revenues app.

The revenues app is responsible for handling the revenue data of the system.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect


@login_required
def accounting(request):
    """Display the revenues page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.user.is_superuser and request.method == 'GET':
        return render(request, 'users/admin_sites/accounting.html')
    return redirect('/')


@login_required
def cost_and_expenses(request):
    """Display the cost and expenses page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    return render(request, 'users/admin_sites/cost_and_expenses.html')
    
    

# @login_required
# def getCostAndRevenue(request):
#     """Returns a JSON object containing the total cost and revenue."""
#     if request.method == 'GET':
#         total_cost = 0
#         total_revenue = 0
#         if request.user.is_superuser:
#             total_refarbished_cost = RefarbishedDevices.total_cost()
#             total_appliance_cost = Appliances.total_cost()
#             total_accessory_cost = Accessories.total_cost()
#             total_cost = MainStorage.total_cost()
#             total_cost += total_refarbished_cost
#             total_cost += total_appliance_cost
#             total_cost += total_accessory_cost
#             total_revenue = MainStorage.total_revenue()
#         elif request.user.groups.filter(name='branches').exists():
#             total_cost = MainStorage.total_cost(agent=request.user)
#             total_revenue = MainStorage.total_revenue(
#                 agent=request.user, month=timezone.now().month)
#         return JsonResponse({
#             'total_cost': total_cost,
#             'total_revenue': total_revenue
#         })
#     return JsonResponse({'error': 'Invalid request.'})