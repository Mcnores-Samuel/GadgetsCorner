"""Add refurbished devices view.
This view allows the user to add refurbished devices to the database.
It checks if the user is an admin or belongs to a specific group.
If the user is an admin, they can add refurbished devices.
The view also handles the addition of new devices and updates existing ones.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gadgetsCorner.models.refarbished_devices import RefarbishedDevices
from django.contrib import messages
from django.utils import timezone


@login_required
def add_refarbished(request):
    if request.user.is_staff and request.user.is_superuser\
        or request.user.groups.filter(name='branches').exists():
        data = RefarbishedDevices.objects.all()
        name_set = set()
        model_set = set()
        for item in data:
            name_set.add(item.name)
            model_set.add(item.model)
        sorted_name_list = sorted(list(name_set))
        sorted_model_list = sorted(list(model_set))
        if request.method == 'POST':
            item = request.POST.get('name')
            model = request.POST.get('model')
            total = request.POST.get('quantity')
            cost = request.POST.get('cost_price')
            try:
                instance = RefarbishedDevices.objects.filter(name=item, model=model).first()
                if instance is None:
                    RefarbishedDevices.objects.create(
                        held_by=request.user, previous_total=0,
                        name=item, model=model, total=total, cost=cost,
                        date_added=timezone.now(), date_modified=timezone.now())
                    messages.success(request, 'Successfully added {} {}(s)'.format(total, item))
                else:
                    instance.previous_total = instance.total
                    instance.total += int(total)
                    instance.cost = cost
                    instance.date_modified = timezone.now()
                    instance.save()
                    messages.success(request, 'Successfully added {} {}(s)'.format(total, item))
            except Exception as e:
                messages.error(request, 'Something went wrong, please try again.')
        if request.user.groups.filter(name='branches').exists():
            return render(request, 'users/branches/add_refarbished.html', {'names': sorted_name_list, 'models': sorted_model_list})
        return render(request, 'users/admin_sites/add_refarbished.html', {'names': sorted_name_list, 'models': sorted_model_list})
    return render(request, 'users/admin_sites/add_refarbished.html', {'names': sorted_name_list, 'models': sorted_model_list})