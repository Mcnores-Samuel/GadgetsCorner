#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the home_page view function, which is the main entry point
for unauthenticated users into the application.
"""
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from ..forms.sign_in_form import SignInForm
from django_email_verification import verify_view, verify_token
from django.http import HttpResponse
from ..models.user_profile import UserAvatar
from django.contrib import messages
from ..models.main_storage import MainStorage
from ..models.user_profile import UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from webpush import send_user_notification
import json


def home_page(request):
    """The `home_page` view function is the main entry point for unauthenticated users
    into the application.

    Functionality:
    - Checks if the user is authenticated.
    - Renders the home page, providing access to various application features.
    - May include different views, options, and functionalities based on user roles.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the application's home page.
    - Redirects authenticated users to the dashboard.

    Usage:
    - Unauthenticated users access this view to interact with the application's core
      functionalities.
    - Customizes the home page interface based on user roles and permissions.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_staff:
                        messages.success(request, f'Welcome {user.username}!!')
                        return redirect(reverse('dashboard'))
                    elif user.groups.filter(name='agents').exists():
                        messages.success(request, f'Welcome {user.username}!!')
                        return redirect(reverse('dashboard'))
                    else:
                        messages.success(request, f'Welcome {user.username}!!')
                        return redirect(reverse('dashboard'))
                else:
                    messages.error(request, 'Your account is not active')
            else:
                messages.error(request, 'Invalid login credentials')
    else:
        form = SignInForm()

    context = {'form': form}
    if request.user.is_authenticated:
        avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
        context['avatar'] = avatar
        context['profile'] = request.user.email[0]
        return redirect(reverse('dashboard'))
    return redirect(reverse('sign_in'))


@verify_view
def confirm(request, token):
    """The `confirm` view function is responsible for handling the confirmation of
    user accounts.
    """
    success, user = verify_token(token)
    return HttpResponse(f'Account verified, {user.username}' if success else 'Invalid token')


@login_required
@csrf_exempt
def dispatch_stock(request):
    """This view function is responsible for dispatching stock to agents.

    Functionality:
    - Checks if the user is authenticated.
    - Renders the dispatch stock page.
    - Allows dispatching multiple stock items to agents.
    - Provides options to filter agents and stock items.
    - Allows the user to select agents and stock items for dispatch.
    - Validates the dispatch request and updates the stock and agent records.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the dispatch stock page.
    - Redirects unauthenticated users to the login page.

    Usage:
    - Authenticated users access this view to dispatch stock to agents.
    - The view provides options to filter agents and stock items for dispatch.
    - The user can select agents and stock items for dispatch.
    - The view validates the dispatch request and updates the stock and agent records.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.method == 'POST' and request.user.is_staff and request.user.is_superuser:
        data = request.POST.get('data', None)
        date = request.POST.get('date', None)
        agent = request.POST.get('agent', None)
        if data:
            scanned_items = json.loads(data)
            date = json.loads(date)
            agent = json.loads(agent)
            not_in_stock = []
            for item in scanned_items:
                try:
                    stock_item = MainStorage.objects.get(device_imei=item)
                    stock_item.collected_on = date
                    stock_item.recieved = False
                    stock_item.agent = UserProfile.objects.get(username=agent)
                    stock_item.save()
                except MainStorage.DoesNotExist:
                    not_in_stock.append(item)
            return JsonResponse({'status': 200, 'not_in_stock': not_in_stock})
        else:
            return JsonResponse({'status': 400, 'error': 'No data received'})
    else:
        agents = UserProfile.objects.filter(groups__name='agents')
        agents = sorted(agents, key=lambda x: x.username)
        special_outlets = UserProfile.objects.filter(groups__name='special_sales')
        agents = list(set(agents + sorted(special_outlets, key=lambda x: x.username)))
    return render(request, 'users/admin_sites/dispatch.html', {'agents': sorted(agents, key=lambda x: x.username)})

