#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models.main_storage import MainStorage
from django.core.mail import send_mail
from ..models.user_profile import UserProfile
from django.utils import timezone


@login_required
def sale_on_cash(request):
    """The `sale_on_cash` view function is responsible for handling the sale of a
    phone on cash.
    """
    if request.method == 'POST':
        user = request.user
        if user.groups.filter(name='agents').exists():
            device_imei = request.POST.get('device_imei')
            amount = request.POST.get('amount')
            cassproof_image = request.FILES.get('cash_proof')
            admin = UserProfile.objects.filter(is_staff=True, is_superuser=True, is_active=True)
            admin_list = [admin.email for admin in admin]
            device = MainStorage.objects.get(device_imei=device_imei)
            device.in_stock = False
            device.pending = True
            device.sold = True
            device.sales_type = 'Cash'
            device.price = amount
            device.stock_out_date = timezone.now()
            device.trans_image = cassproof_image
            device.save()
            messages.success(request, 'Your sale has been successfully processed and is pending approval.')
            return redirect('in_stock')
        messages.error(request, 'An error occurred while processing your sale. Please try again or contact the administrator.')
    return redirect('in_stock')
