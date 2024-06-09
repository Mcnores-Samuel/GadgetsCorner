#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains combined data collection view function, which is responsible
for handling the collection of customer and phone data during the phone purchasing
process by agents.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models.main_storage import MainStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from webpush import send_user_notification
from os import environ
from ..models.user_profile import UserProfile


@login_required
def combinedData_collection(request, data_id):
    """
    The `combinedData_collection` view function is a Django view responsible for
    handling the collection of customer and phone data during the phone purchasing
    process by agents.

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Verifies if the agent has available stock of phones.
    - Renders either the combined data form or an "out of stock" message based on
      the agent's stock availability.
    - If the agent has stock and submits the form, customer and phone records are
      created in the database.
    - If the agent is out of stock, a message is displayed, instructing them to
      contact the office for stock replenishment.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not an agent, it returns a 403 Forbidden
      response.
    - If the agent is authenticated and has stock, it renders the combined data form.
    - If the agent is out of stock, it renders an "out of stock" message.

    Usage:
    Agents access this view to collect customer data and select phones for sale.
    It ensures that agents with available stock can proceed with data collection,
    while agents without stock are notified to contact the office for replenishment.

    Note:
    This view assumes user authentication and validation of agent status have been
    handled in the authentication system and AgentProfile model.
    """
    if request.user.is_staff and request.user.is_superuser:
        if request.method == 'POST':
            payment = request.POST.get('payment_method')
            item = MainStorage.objects.get(id=data_id)
            if item.in_stock and not item.sold:
                if payment == 'Cash':
                    price = request.POST.get('price')
                    item.in_stock = False
                    item.sold = True
                    item.pending = True
                    item.sales_type = 'Cash'
                    item.stock_out_date = timezone.now()
                    item.price = price
                    messages.success(request, '{} of imei {} sold successfully'.format(
                        item.name, item.device_imei
                    ))
                    item.save()
                    payload = {'head': 'Sales Notification', 'body': '{} of imei {} sold successfully'.format(
                        item.name, item.device_imei
                    ), 'icon': environ.get('ICON_LINK')}
                    send_user_notification(user=request.user, payload=payload, ttl=1000)
                    return redirect('data_search')
                elif payment == 'Loan':
                    mbo = request.POST.get('mbo')
                    contract_number = request.POST.get('contract_number')
                    item.contract_no = contract_number
                    item.in_stock = False
                    item.sold = True
                    item.pending = True
                    item.sales_type = 'Loan'
                    item.stock_out_date = timezone.now()
                    messages.success(request, '{} of imei {} sold successfully'.format(
                        item.name, item.device_imei
                    ))
                    item.save()
                    payload = {'head': 'Sales Notification', 'body': '{} of imei {} sold successfully'.format(
                        item.name, item.device_imei
                    ), 'icon': environ.get('ICON_LINK')}
                    send_user_notification(user=request.user, payload=payload, ttl=1000)
                    return redirect('data_search')
                messages.error(request, 'Invalid payment method')
            else:
                messages.error(request, 'Phone out of stock')
    if request.user.is_staff and request.user.is_superuser:
        mbos = UserProfile.objects.filter(groups__name='MBOs')
        return render(request, 'users/admin_sites/salespoint.html', {'mbos': mbos})
    mbos = UserProfile.objects.filter(groups__name='MBOs')
    return render(request, 'registration/salespoint.html', {'mbos': mbos})


@login_required
@csrf_exempt
def uploadBulkSales(request):
    """
    The `uploadBulkSales` view function is a Django view responsible for
    handling the bulk upload of sales data by all outlets

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Verifies if the agent has available stock of phones.
    """
    if request.method == 'POST' and request.user.is_staff and request.user.is_superuser:
        data = request.POST.get('data', None)
        date = request.POST.get('date', None)
        sales_type = request.POST.get('sales_type', None)
        if data:
            scanned_items = json.loads(data)
            date = json.loads(date)
            sales_type = json.loads(sales_type)
            not_in_stock = []
            for item in scanned_items:
                try:
                    stock_item = MainStorage.objects.get(device_imei=item)
                    stock_item.stock_out_date = date
                    stock_item.sold = True
                    stock_item.in_stock = False
                    if sales_type == 'Loan':
                        stock_item.sales_type = sales_type
                        stock_item.pending = True
                    else:
                        stock_item.sales_type = sales_type
                        stock_item.pending = False
                        stock_item.paid = True
                    stock_item.save()
                except MainStorage.DoesNotExist:
                    not_in_stock.append(item)
            return JsonResponse({'status': 200, 'not_in_stock': not_in_stock})
        else:
            return JsonResponse({'status': 400, 'error': 'No data received'})
    return render(request, 'users/admin_sites/upload_sales.html')