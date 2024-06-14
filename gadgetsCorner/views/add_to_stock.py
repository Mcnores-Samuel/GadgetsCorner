"""This module contains a view function for adding phones to stock."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.main_storage import MainStorage
from ..models.accessories import Accessories
from ..models.appliances import Appliances
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
import json
from django.contrib import messages


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
        model_names = set()
        category_names = set()
        spec_names = set()
        for phone in data:
            if phone.name is not None:
                phone_names.add(phone.name)
                model_names.add(phone.phone_type)
                category_names.add(phone.category)
                spec_names.add(phone.spec)
        sorted_phone_list = sorted(list(phone_names))
        sorted_model_list = sorted(list(model_names))
        sorted_category_list = sorted(list(category_names))
        sorted_spec_list = sorted(list(spec_names))
        if request.method == 'POST':
            data = json.loads(request.POST.get('data'))
            name = request.POST.get('name')
            cost_price = request.POST.get('cost_price')
            supplier = request.POST.get('supplier')
            category = request.POST.get('category')
            spec = request.POST.get('spec')
            phone_type = request.POST.get('model')
            already_exists = []
            for item in data:
                try:
                    MainStorage.objects.create(
                        device_imei=item[0], device_imei_2=item[1], name=name,
                        phone_type=phone_type, category=category,
                        spec=spec, in_stock=True, sales_type='##', contract_no='##',
                        entry_date=timezone.now(), stock_out_date=timezone.now(),
                        collected_on=timezone.now(), assigned=True, sold=False,
                        issue=False, paid=False, cost=cost_price, price=0.00, agent=request.user,
                        recieved=True, on_display=False, pending=False, missing=False,
                        supplier=supplier, faulty=False, assigned_from='Gadgets Corner',
                        updated_by=user.username, comment='##'
                    )
                except Exception as e:
                    already_exists.append(item)
            return JsonResponse({'status': 200, 'data': already_exists})
    return render(request, 'users/admin_sites/add_to_stock.html',
                  {'phone_names': sorted_phone_list, 'models': sorted_model_list,
                   'categories': sorted_category_list, 'specs': sorted_spec_list})


@login_required
def add_accessaries(request):
    if request.user.is_staff and request.user.is_superuser:
        data = Accessories.objects.all()
        name_set = set()
        model_set = set()
        for item in data:
            name_set.add(item.item)
            model_set.add(item.model)
        sorted_name_list = sorted(list(name_set))
        sorted_model_list = sorted(list(model_set))
        if request.method == 'POST':
            item = request.POST.get('accessary_name')
            model = request.POST.get('model')
            total = request.POST.get('quantity')
            cost = request.POST.get('cost_price')
            try:
                instance = Accessories.objects.filter(item=item, model=model).first()
                if instance is None:
                    Accessories.objects.create(
                        held_by=request.user,
                        item=item, model=model, total=total, previous_total=0, cost_per_item=cost,
                        date_added=timezone.now(), date_modified=timezone.now())
                    messages.success(request, 'Successfully added {} {}(s)'.format(total, item))
                else:
                    instance.previous_total = instance.total
                    instance.total += int(total)
                    instance.cost_per_item = cost
                    instance.date_modified = timezone.now()
                    instance.save()
                    messages.success(request, 'Successfully added {} {}(s)'.format(total, item))
            except Exception as e:
                messages.error(request, 'Something went wrong, please try again.')
        return render(request, 'users/admin_sites/add_accessaries.html', {'names': sorted_name_list, 'models': sorted_model_list})
    return render(request, 'users/admin_sites/add_accessaries.html', {'names': sorted_name_list, 'models': sorted_model_list})


@login_required
def add_appliances(request):
    if request.user.is_staff and request.user.is_superuser:
        data = Appliances.objects.all()
        name_set = set()
        model_set = set()
        for item in data:
            name_set.add(item.name)
            model_set.add(item.model)
        sorted_name_list = sorted(list(name_set))
        sorted_model_list = sorted(list(model_set))
        if request.method == 'POST':
            item = request.POST.get('appliance_name')
            model = request.POST.get('model')
            total = request.POST.get('quantity')
            cost = request.POST.get('cost_price')
            try:
                instance = Appliances.objects.filter(name=item, model=model).first()
                if instance is None:
                    Appliances.objects.create(
                        name=item, model=model, total=total, cost=cost,
                        date_added=timezone.now(), date_modified=timezone.now())
                    messages.success(request, 'Successfully added {} {}(s)'.format(total, item))
                else:
                    instance.total += int(total)
                    instance.cost = cost
                    instance.date_modified = timezone.now()
                    instance.save()
                    messages.success(request, 'Successfully added {} {}(s)'.format(total, item))
            except Exception as e:
                messages.error(request, 'Something went wrong, please try again.')
        return render(request, 'users/admin_sites/add_appliances.html', {'names': sorted_name_list, 'models': sorted_model_list})
    return render(request, 'users/admin_sites/add_appliances.html', {'names': sorted_name_list, 'models': sorted_model_list})