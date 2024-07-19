from ..models.main_storage import MainStorage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..data_analysis_engine.admin_panel.mainstorage_analysis import MainStorageAnalysis
from ..models.accessories import Accessories
from ..models.appliances import Appliances


def get_daily_sales_json(request):
    """Returns a JSON object containing the daily sales data."""
    if request.method == 'GET':
        sales = MainStorageAnalysis().get_daily_sales()
        return JsonResponse(sales)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_weekly_sales_json(request):
    """Returns a JSON object containing the weekly sales data."""
    if request.method == 'GET':
        days = MainStorageAnalysis().get_weekly_sales()
        return JsonResponse(days)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_monthly_sales(request):
    """Returns a JSON object containing the monthly sales data."""
    if request.method == 'GET':
        sales = MainStorageAnalysis().get_monthly_sales()
        return JsonResponse(sales)
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
def get_yearly_sales_total(request):
    """Returns the total yearly sales."""
    if request.method == 'GET':
        sales = MainStorageAnalysis().get_sales_for_all_months(request.user)
        return JsonResponse(sales, safe=False)
    return JsonResponse({'error': 'Invalid request.'})