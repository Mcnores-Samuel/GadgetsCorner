from ..models.main_storage import MainStorage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..data_analysis_engine.admin_panel.mainstorage_analysis import MainStorageAnalysis
from ..models.accessories import Accessories, Accessory_Sales
from ..models.appliances import Appliances, Appliance_Sales
from django.utils import timezone


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
        today = timezone.now().date()
        sales = MainStorageAnalysis().get_daily_sales('Cash')
        accessories = Accessory_Sales.objects.filter(date_sold__date=today)
        appliances = Appliance_Sales.objects.filter(date_sold__date=today)

        # Calculate the total sales for the day
        for item in appliances:
            try:
                sales[item.item] += item.total
            except KeyError:
                sales[item.item] = item.total

        # Calculate the total sales for the day
        for item in accessories:
            try:
                sales[item.item + f"({item.model})"] += item.total
            except KeyError:
                sales[item.item + f"({item.model})"] = item.total
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
        data_set = MainStorage.objects.filter(
            in_stock=True, sold=False, missing=False, assigned=True, recieved=True, faulty=False,
            pending=False, issue=False)
        accessaries = Accessories.objects.all()
        appliances = Appliances.objects.all()

        total = 0
        stock = {}
        for item in appliances:
            stock[item.name + f"({item.model})"] = item.total
            total += item.total
            
        for item in accessaries:
            stock[item.item + f"({item.model})"] = item.total
            total += item.total
        stock['Phones'] = data_set.count()
        total += data_set.count()
        stock['Total'] = total
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