"""This module contains a view function for adding phones to stock."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.main_storage import MainStorage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from ..models.user_profile import UserProfile
from django.utils import timezone
from django.http import JsonResponse
import json


@login_required
@csrf_exempt
def add_to_stock(request):
    """This view function is responsible for handling the addition of phones to stock.

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Renders the add to stock form.
    - If the form is submitted, the phone is added to stock.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not an agent, it returns a 403 Forbidden
      response.
    - If the agent is authenticated and has stock, it renders the add to stock form.

    Usage:
    Agents access this view to add phones to stock.
    It ensures that only agents are able to access this view.
    """
    if request.user.is_staff and request.user.is_superuser:
        user = request.user
        data = MainStorage.objects.all()
        phone_names = set()
        for phone in data:
            if phone.name is not None:
                phone_names.add(phone.name)
        sorted_phone_list = sorted(list(phone_names))
        if request.method == 'POST':
            data = json.loads(request.POST.get('data'))
            name = request.POST.get('name')
            cost_price = request.POST.get('cost_price')
            supplier = request.POST.get('supplier')
            instance = MainStorage.objects.filter(name=name).first()
            main_shop_staff = Group.objects.get(name='main_shop')
            representatives = UserProfile.objects.filter(groups=main_shop_staff)
            agent = representatives.first()
            already_exists = []
            for item in data:
                try:
                    MainStorage.objects.create(
                        device_imei=item[0], device_imei_2=item[1], name=name,
                        phone_type=instance.phone_type, category=instance.category,
                        spec=instance.spec, in_stock=True, sales_type='##', contract_no='##',
                        entry_date=timezone.now(), stock_out_date=timezone.now(),
                        collected_on=timezone.now(), assigned=True, sold=False,
                        issue=False, paid=False, cost=cost_price, price=0.00, agent=agent,
                        recieved=True, on_display=False, pending=False, missing=False,
                        supplier=supplier, faulty=False, assigned_from='Gadgets Corner',
                        updated_by=user.username, comment='##'
                    )
                except Exception as e:
                    already_exists.append(item)
            return JsonResponse({'status': 200, 'data': already_exists})
    return render(request, 'users/admin_sites/add_to_stock.html', {'phone_names': sorted_phone_list})