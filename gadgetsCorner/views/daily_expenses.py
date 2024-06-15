"""This module contains a view function for adding daily expenses."""
from ..models.daily_expenses import DailyExpenses
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def add_daily_expense(request):
    """This view function is responsible for handling the addition of daily expenses.

    Functionality:
    - Checks if the user is authenticated and is an agent. Only agents are allowed
      to access this view.
    - Renders the add daily expense form.
    - If the form is submitted, the daily expense is added.

    Parameters:
    - request: The HTTP request object containing user information.

    Returns:
    - If the user is not authenticated or is not an agent, it returns a 403 Forbidden
      response.
    - If the agent is authenticated and has stock, it renders the add daily expense form.

    Usage:
    Agents access this view to add daily expenses.
    It ensures that only agents are able to access this view.
    """
    if request.user.is_staff and request.user.is_superuser:
        user = request.user
        data = DailyExpenses.objects.all()
        if request.method == 'POST':
            name = request.POST.get('name')
            amount = request.POST.get('amount')
            DailyExpenses.objects.create(
                added_by=user, name=name, amount=amount, date=timezone.now())
            messages.success(request, '{} spent on {} has been added to the daily expenses.'.format(amount, name))
        return redirect('dashboard')
    return redirect('dashboard')