#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module contains the views for the application."""
from django.shortcuts import render
from ..forms import *
from django.contrib.auth.decorators import login_required
from ..models.user_profile import UserProfile
from ..models.main_storage import MainStorage
from ..forms.filters import FilterAgentAndData, FilterAgentAndDataSales
from django.contrib.auth.models import Group
from django.utils import timezone
import os


@login_required
def main_stock_details(request):
    """The `main_storage` view function is responsible for handling the display of the
    application's main_storage page.
    """
    if request.method == 'GET' and request.user.is_staff:
        form = FilterAgentAndData(request.GET)
        if form.is_valid():
            user = form.cleaned_data['user']
            stock = {}
            data_set = MainStorage.objects.filter(
                agent=user.user, in_stock=True, sold=False, assigned=True).order_by('id')
            total = data_set.count()
            for data in data_set:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1

            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
            data_url = '/' + os.environ.get('ADMIN_URL') + '/' + f'system_core_1/mainstorage/?agent={user.user.username}&in_stock__exact=1'
            context = {'stock': stock, 'user': user.user.username, 'form': form, 'total': total, 'data_url': data_url}
            return render(request, 'users/admin_sites/main_stock_details.html', context)
        else:
            form = FilterAgentAndData()
            main_shop_staff = Group.objects.get(name='main_shop')
            representatives = UserProfile.objects.filter(groups=main_shop_staff)
            data_set = MainStorage.objects.filter(
                agent__in=representatives,
                in_stock=True, sold=False,
                missing=False, assigned=True)
            total = data_set.count()
            stock = {}
            for data in data_set:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
            data_url = '/' + os.environ.get('ADMIN_URL') + '/' + 'system_core_1/mainstorage/?agent=Hafeez-Enterprise&in_stock__exact=1'
    context = {'form': form, 'stock': stock, 'user': representatives[0].username, 'total': total, 'data_url': data_url}
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
            user = form.cleaned_data['user']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            stock = {}
            data_set = MainStorage.objects.filter(
                agent=user.user, in_stock=False, sold=True,
                assigned=True, pending=False, missing=False,
                stock_out_date__month=month, stock_out_date__year=year).order_by('id')
            total = data_set.count()
            for data in data_set:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1

            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
            context = {'stock': stock, 'user': user.user.username,
                       'form': form, 'total': total}
            return render(request, 'users/admin_sites/main_sales_details.html', context)
        else:
            form = FilterAgentAndDataSales()
            main_shop_staff = Group.objects.get(name='main_shop')
            representatives = UserProfile.objects.filter(groups=main_shop_staff)
            year = timezone.now().date().year
            month = timezone.now().date().month
            data_set = MainStorage.objects.filter(
                agent__in=representatives,
                in_stock=False, sold=True,
                missing=False, assigned=True, pending=False,
                stock_out_date__month=month, stock_out_date__year=year)
            total = data_set.count()
            stock = {}
            for data in data_set:
                stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
            stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
    context = {'form': form, 'stock': stock,
               'user': representatives[0].username,
               'total': total}
    return render(request, 'users/admin_sites/main_sales_details.html', context)

