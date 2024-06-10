#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module contains the views for the application."""
from django.shortcuts import render
from ..forms import *
from django.contrib.auth.decorators import login_required
from ..models.user_profile import UserProfile
from ..models.main_storage import MainStorage
from ..models.accessories import Accessories, Accessory_Sales
from ..forms.filters import FilterAgentAndData, FilterAgentAndDataSales
from django.utils import timezone
import os


@login_required
def main_stock_details(request):
    """The `main_storage` view function is responsible for handling the display of the
    application's main_storage page.
    """
    if request.method == 'GET' and request.user.is_staff:
        data_set = MainStorage.objects.filter(
            agent=request.user, in_stock=True, sold=False,
            missing=False, assigned=True).order_by('id')
        accessories = Accessories.objects.all()
        total = data_set.count()
        stock = {}
        for data in accessories:
            stock[data.item + f"({data.model})"] = stock.get(data.item + f"({data.model})", 0) + data.total
            total += data.total
        for data in data_set:
            stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
        stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
        data_url = '/' + os.environ.get('ADMIN_URL') + '/'
    context = {'stock': stock, 'user': request.user.username, 'total': total, 'data_url': data_url}
    return render(request, 'users/admin_sites/main_stock_details.html', context)


@login_required
def main_sales_details(request):
    """The `main_storage` view function is responsible for handling the display of the
    application's main_storage page.

    Functionality:
        - Checks if the user is authenticated and is a staff member. Only staff members
            are allowed to access this view.
        - Renders the main storage page, displaying all phones in the main storage.
        - Implements search and filtering functionality.

    Note:
        This view assumes user authentication and validation of staff status have been
        handled in the authentication system and UserProfile model.
    """
    if request.method == 'GET' and request.user.is_staff:
        form = FilterAgentAndDataSales(request.GET)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            stock = {}
            data_set = MainStorage.objects.filter(
                in_stock=False, sold=True,
                assigned=True, pending=False, missing=False,
                stock_out_date__month=month, stock_out_date__year=year).order_by('id')
            accessories = Accessory_Sales.objects.filter(
                date_sold__month=month, date_sold__year=year)
            total = data_set.count()
            for data in accessories:
                stock[data.item + f"({data.model})"] = stock.get(data.item + f"({data.model})", 0) + data.total
                total += data.total
            for data in data_set:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1

            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
            context = {'stock': stock, 'user': request.user.username,
                       'form': form, 'total': total}
            return render(request, 'users/admin_sites/main_sales_details.html', context)
        else:
            form = FilterAgentAndDataSales()
            year = timezone.now().date().year
            month = timezone.now().date().month
            data_set = MainStorage.objects.filter(
                agent=request.user,
                in_stock=False, sold=True,
                missing=False, assigned=True, pending=False,
                stock_out_date__month=month, stock_out_date__year=year)
            accessories = Accessory_Sales.objects.filter(
                date_sold__month=month, date_sold__year=year)
            total = data_set.count()
            stock = {}
            for data in accessories:
                stock[data.item + f"({data.model})"] = stock.get(data.item + f"({data.model})", 0) + data.total
                total += data.total
            for data in data_set:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
    context = {'form': form, 'stock': stock,
               'user': request.user.username,
               'total': total}
    return render(request, 'users/admin_sites/main_sales_details.html', context)

