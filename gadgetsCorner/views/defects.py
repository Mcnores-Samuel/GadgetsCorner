"""This module contains the views related to the defects."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.main_storage import MainStorage


@login_required
def defects(request):
    """This function returns the defects page."""
    data = MainStorage.objects.filter(faulty=True).order_by('-entry_date')
    return render(request, 'users/admin_sites/defects.html', {'data': data})