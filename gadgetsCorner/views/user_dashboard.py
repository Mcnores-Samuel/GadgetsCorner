#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the dashboard view function, which is the main entry point
for authenticated users into the application.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models.user_profile import UserAvatar, UserProfile
from ..models.main_storage import MainStorage
from django.utils import timezone
from webpush import send_user_notification
from django.shortcuts import redirect
import os


@login_required
def dashboard(request):
    """
    The `dashboard` view function is the main entry point for authenticated users
    into the application's dashboard.

    Functionality:
    - Checks if the user is authenticated and has the appropriate permissions.
    - Renders the dashboard page, providing access to various application features.
    - May include different views, options, and functionalities based on user roles.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - Renders the application's dashboard page.
    - Redirects unauthenticated users to the sign-in page.

    Usage:
    - Authenticated users access this view to interact with the application's core
      functionalities.
    - Customizes the dashboard interface based on user roles and permissions.

    Note:
    - User authentication and authorization should be managed by the authentication
      and authorization systems.
    """
    if request.user.is_staff:
        user = request.user
        admin_url = '/' + os.environ.get('ADMIN_URL') + '/'
        avatar = UserAvatar.objects.get(
            user=request.user) if UserAvatar.objects.filter(
                user=request.user).exists() else None
        context = {
            'profile': user.email[0],
            'user': user,
            'admin_url': admin_url,
            'avatar': avatar,
        }
        return render(request, 'users/admin_sites/main.html', context)
    return redirect('sign_in')
