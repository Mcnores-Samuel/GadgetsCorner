"""This module defines the view for the expense table.
This module contains the view for the expense table, including the function to
update and delete expenses.
"""
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from gadgetsCorner.models.daily_expenses import DailyExpenses
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def expense_view(request):
    """This function returns the expense page."""
    if request.method == 'GET':
        expenses = DailyExpenses.objects.all()
        paginator = Paginator(expenses, 12)
        page_number = request.GET.get("page")
        try:
            expenses = paginator.page(page_number)
        except PageNotAnInteger:
            expenses = paginator.page(1)
        except EmptyPage:
            expenses = paginator.page(paginator.num_pages)
        return render(request, 'users/admin_sites/expense.html', {'expenses': expenses})
    return redirect('dashboard')


@login_required
def update_expense(request):
    """This function updates the expense."""
    if request.method == 'POST' and request.user.is_superuser:
        expense_id = request.POST.get('expenseId')
        category = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        try:
            expense = DailyExpenses.objects.get(id=expense_id)
            expense.category = category
            expense.description = description
            expense.amount = amount
            expense.save()
            messages.success(request, 'Expense updated successfully.')
        except DailyExpenses.DoesNotExist:
            messages.error(request, 'Expense not found.')
        except Exception as e:
            messages.error(request, f'Error updating expense: {e}')
    return redirect('expense_view')


@login_required
def delete_expense(request):
    """This function deletes the expense."""
    if request.method == 'POST' and request.user.is_superuser:
        expense_id = request.POST.get('expenseId')
        try:
            expense = DailyExpenses.objects.get(id=expense_id)
            expense.delete()
            messages.success(request, 'Expense deleted successfully.')
        except DailyExpenses.DoesNotExist:
            messages.error(request, 'Expense not found.')
        except Exception as e:
            messages.error(request, f'Error deleting expense: {e}')
    return redirect('expense_view')