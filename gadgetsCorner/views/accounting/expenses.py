"""This module contains the views for the expenses table."""
from gadgetsCorner.models.daily_expenses import DailyExpenses as Expenses
from gadgetsCorner.models.user_profile import UserProfile
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse


@login_required
def expenses(request):
    """This function returns the expenses page."""
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('date')

        try:
            Expenses.objects.create(
                amount=amount, description=description,
                date=date, category=category, added_by=request.user)
            messages.success(request, 'Expense added successfully')
        except UserProfile.DoesNotExist:
            messages.error(request, "Error occured while adding expenses")
        return redirect('accounting')
    return redirect('accounting')


@login_required
def get_total_expenses(request):
    """This function returns the total expenses."""
    if request.method == 'GET':
        total_expenses = Expenses.total_expenses()
        return JsonResponse({'total_expenses': total_expenses})
    return JsonResponse({'error': 'Invalid request.'})

        