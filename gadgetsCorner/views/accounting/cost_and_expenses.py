"""This module contains the cost and expenses view."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from gadgetsCorner.models.main_storage import MainStorage
from gadgetsCorner.models.refarbished_devices import RefarbishedDevices
from gadgetsCorner.models.appliances import Appliances
from gadgetsCorner.models.accessories import Accessories


@login_required
def availableStockCost(request):
    """Returns the total cost of available stock."""
    if request.method == 'GET':
        total_cost = MainStorage.total_cost()
        total_refarbished_cost = RefarbishedDevices.total_cost()
        total_appliance_cost = Appliances.total_cost()
        total_accessory_cost = Accessories.total_cost()
        
        if total_refarbished_cost is not None:
            total_cost += total_refarbished_cost
        
        if total_appliance_cost is not None:
            total_cost += total_appliance_cost

        if total_accessory_cost is not None:
            total_cost += total_accessory_cost
        
        return JsonResponse({'total_cost': total_cost})
    return JsonResponse({'error': 'Invalid request.'})