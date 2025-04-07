"""This module contains the views for the liability table."""
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from gadgetsCorner.models.liabilities import Liability
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone


@login_required
def liabilities_view(request):
    """This function returns the liabilities page."""
    if request.method == 'GET':
        liabilities = Liability.objects.all()
        paginator = Paginator(liabilities, 12)
        page_number = request.GET.get("page")
        try:
            liabilities = paginator.page(page_number)
        except PageNotAnInteger:
            liabilities = paginator.page(1)
        except EmptyPage:
            liabilities = paginator.page(paginator.num_pages)
        return render(request, 'users/admin_sites/liabilities.html', {'liabilities': liabilities})
    return render(request, 'users/admin_sites/liabilities.html')


@login_required
def update_liability(request):
    """This function updates the liability."""
    if request.method == 'POST' and request.user.is_superuser:
        liability_type = request.POST.get('liabilityType')
        liability_creditor = request.POST.get('liabilityCreditor')
        liability_amount = request.POST.get('liabilityAmount')
        liability_description = request.POST.get('liabilityDescription')
        liability_id = request.POST.get('liabilityId')
        interest_rate = request.POST.get('liabilityInterestRate')
        try:
            interest_rate = float(interest_rate)
        except ValueError:
            messages.error(request, 'Interest rate must be a number.')
            return redirect('liabilities_view')
        try:
            liability = Liability.objects.get(id=liability_id)
            liability.type = liability_type
            liability.creditor = liability_creditor
            try:
                liability_amount = float(liability_amount)
            except ValueError:
                messages.error(request, 'Amount must be a number.')
                return redirect('liabilities_view')
            liability.amount = liability_amount
            liability.description = liability_description
            liability.interest_rate = interest_rate
            liability.save()
            messages.success(request, 'Liability updated successfully.')
        except Liability.DoesNotExist:
            messages.error(request, 'Liability not found.')
        except Exception as e:
            messages.error(request, f'Error updating liability: {e}')
    return redirect('liabilities_view')


@login_required
def delete_liability(request):
    """This function deletes the liability."""
    if request.method == 'POST' and request.user.is_superuser:
        liability_id = request.POST.get('liabilityId')

        try:
            liability = Liability.objects.get(id=liability_id)
            liability.delete()
            messages.success(request, 'Liability deleted successfully.')
        except Liability.DoesNotExist:
            messages.error(request, 'Liability not found.')
        except Exception as e:
            messages.error(request, f'Error deleting liability: {e}')
    return redirect('liabilities_view')


@login_required
def mark_as_paid(request):
    """This function marks the liability as paid."""
    if request.method == 'POST' and request.user.is_superuser:
        liability_id = request.POST.get('liabilityId')

        try:
            liability = Liability.objects.get(id=liability_id)
            liability.is_paid = True
            liability.date_paid = timezone.now()
            liability.save()
            messages.success(request, 'Liability marked as paid successfully.')
        except Liability.DoesNotExist:
            messages.error(request, 'Liability not found.')
        except Exception as e:
            messages.error(request, f'Error marking liability as paid: {e}')
    return redirect('liabilities_view')