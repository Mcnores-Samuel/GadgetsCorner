"""This module contains a view for the liabilities json response."""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from gadgetsCorner.models.liabilities import Liability
from django.shortcuts import redirect
from django.contrib import messages


@login_required
def add_liability(request):
    """This function adds a liability."""
    if request.method == 'POST' and request.user.is_superuser:
        liability_type = request.POST.get('liabilityType')
        creditor = request.POST.get('liabilityCreditor')
        amount = request.POST.get('liabilityAmount')
        description = request.POST.get('liabilityDescription')
        interest_rate = request.POST.get('liabilityInterestRate')
        effective_date = request.POST.get('liabilityeffectiveDate')
        due_date = request.POST.get('liabilityDueDate')

        Liability.objects.create(
            type=liability_type,
            creditor=creditor,
            amount=amount,
            description=description,
            interest_rate=interest_rate,
            effective_date=effective_date,
            due_date=due_date,
            is_paid=False
        )
        messages.success(request, 'Liability added successfully.')
        return redirect('accounting')
    messages.error(request, 'Error adding liability.')
    return redirect('accounting')


@login_required
def total_liabilities(request):
    """This function returns the total liabilities."""
    if request.method == 'GET' and request.user.is_superuser:
        total = (Liability.total_current_liabilities() +
                 Liability.total_non_current_liabilities())
        return JsonResponse({'total_liabilities': total})
    return JsonResponse({'error': 'Invalid request.'})