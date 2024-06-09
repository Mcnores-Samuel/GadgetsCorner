from ..models.main_storage import MainStorage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from ..models.user_profile import UserProfile
from ..data_analysis_engine.admin_panel.mainstorage_analysis import MainStorageAnalysis


@login_required
def get_daily_sales_json_loan(request):
    """Returns a JSON object containing the daily sales data."""
    if request.method == 'GET':
        sales = MainStorageAnalysis().get_daily_sales('Loan')
        return JsonResponse(sales)
    return JsonResponse({'error': 'Invalid request.'})


def get_daily_sales_json_cash(request):
    """Returns a JSON object containing the daily sales data."""
    if request.method == 'GET':
        sales = MainStorageAnalysis().get_daily_sales('Cash')
        return JsonResponse(sales)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_weekly_sales_json_loan(request):
    """Returns a JSON object containing the weekly sales data."""
    if request.method == 'GET':
        days = MainStorageAnalysis().get_weekly_sales('Loan')
        return JsonResponse(days)
    return JsonResponse({'error': 'Invalid request.'})


def get_weekly_sales_json_cash(request):
    """Returns a JSON object containing the weekly sales data."""
    if request.method == 'GET':
        days = MainStorageAnalysis().get_weekly_sales('Cash')
        return JsonResponse(days)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_sale_by_agent_monthy_loan(request):
    """Returns a JSON object containing the monthly sales data by agent."""
    if request.method == 'GET':
        sales_by_agent = MainStorageAnalysis().get_monthly_sales_by_agents('Loan')
        return JsonResponse(sales_by_agent, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_sale_by_agent_monthy_cash(request):
    """Returns a JSON object containing the monthly sales data by agent."""
    if request.method == 'GET':
        sales_by_agent = MainStorageAnalysis().get_monthly_sales_by_agents('Cash')
        return JsonResponse(sales_by_agent, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_main_stock_analysis(request):
    """Returns a JSON object containing the main stock analysis."""
    if request.method == 'GET':
        main_shop_staff = Group.objects.get(name='main_shop')
        representatives = UserProfile.objects.filter(groups=main_shop_staff)
        data_set = MainStorage.objects.filter(
            agent__in=representatives, in_stock=True, sold=False,
            missing=False, assigned=True, recieved=True, faulty=False,
            pending=False, issue=False)
        stock = {}
        stock[representatives[0].username] = data_set.count()
        stock['Target Capacity'] = 1000
        stock['Total'] = data_set.count()
        return JsonResponse(stock)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_individual_agent_stock(request):
    """Returns a JSON object containing the individual agent's stock."""
    if request.method == 'GET':
        agent = request.user
        stock = MainStorageAnalysis().get_agent_stock_in(agent)
        return JsonResponse(stock)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_individual_agent_stock_out(request):
    """Returns a JSON object containing the individual agent's stock."""
    if request.method == 'GET':
        agent = request.user
        stock = MainStorageAnalysis().get_agent_stock_out(agent)
        return JsonResponse(stock, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_yearly_sales(request):
    """Returns a JSON object containing the yearly sales data."""
    if request.method == 'GET':
        sales, overall = MainStorageAnalysis().get_sales_for_all_months(request.user)
        return JsonResponse(sales, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_yearly_sales_total(request):
    """Returns the total yearly sales."""
    if request.method == 'GET':
        sales = MainStorageAnalysis().get_sales_for_all_months(request.user)
        return JsonResponse(sales[1], safe=False)
    return JsonResponse({'error': 'Invalid request.'})