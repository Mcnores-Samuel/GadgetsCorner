"""This module contains the networth view."""
from gadgetsCorner.models.main_storage import MainStorage
from gadgetsCorner.models.refarbished_devices import RefarbishedDevices
from gadgetsCorner.models.appliances import Appliances
from gadgetsCorner.models.accessories import Accessories
from gadgetsCorner.models.assets import FixedAssets
from gadgetsCorner.models.liabilities import Liability
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def networth(request):
    """This function returns the networth of the company."""
    if request.method == 'GET' and request.user.is_superuser:
        total_assets = (
            MainStorage.total_cost() + RefarbishedDevices.total_cost() +
            Appliances.total_cost() + Accessories.total_cost())
        total_liabilities = (Liability.total_current_liabilities() +
                             Liability.total_non_current_liabilities())
        total_fixed_assets = FixedAssets.total_assets_cost()
        networth = (total_assets + total_fixed_assets) - total_liabilities
        return JsonResponse({'networth': networth})
    return JsonResponse({'error': 'Invalid request.'})
