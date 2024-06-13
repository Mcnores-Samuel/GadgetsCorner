from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models.user_profile import UserProfile
from ..models.main_storage import MainStorage
from ..models.accessories import Accessory_Sales
from ..models.appliances import Appliance_Sales
from django.contrib.auth.models import Group
from django.utils import timezone
from ..data_analysis_engine.admin_panel.mainstorage_analysis import MainStorageAnalysis


@login_required
def get_source_stock(request):
    """Returns a JSON object containing the daily stock data."""
    if request.method == 'GET':
        main_shop_staff = Group.objects.get(name='main_shop')
        representatives = UserProfile.objects.filter(groups=main_shop_staff)
        data_set = MainStorage.objects.filter(
            agent__in=representatives,
            in_stock=True, sold=False,
            missing=False, assigned=True)
        stock = {}
        for data in data_set:
            stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
        stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
        return JsonResponse(stock, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def get_yearly_product_sales(request):
    """This function returns a JSON object containing
    the yearly product sales data for overall sales.
    """
    if request.method == 'GET':
        year = timezone.now().date().year
        data_set = MainStorage.objects.filter(
            in_stock=False, assigned=True,
            sold=True, missing=False,
            pending=False, stock_out_date__year=year)
        accessory = Accessory_Sales.objects.filter(date_sold__year=year)
        appliance = Appliance_Sales.objects.filter(date_sold__year=year)
        products = {}
        for product in data_set:
            products[product.phone_type] = products.get(product.phone_type, 0) + 1
        for product in accessory:
            products[product.item + f"({product.model})"] = products.get(product.item + f"({product.model})", 0) + product.total
        for product in appliance:
            products[product.item + f"({product.model})"] = products.get(product.item + f"({product.model})", 0) + product.total
        products = sorted(products.items(), key=lambda x: x[1], reverse=True)
        return JsonResponse(products, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


def admin_stock_analysis(request):
    """This function returns a JSON object containing the daily stock data."""
    if request.method == 'GET':
        estimated_revenue = MainStorageAnalysis().estimated_revenue()
        estimated_profit = MainStorageAnalysis().estimated_profit()
        print(estimated_revenue)
        print(estimated_profit)
        context = {
            'estimated_revenue': estimated_revenue,
            'estimated_profit': estimated_profit
        }
        return JsonResponse(context, safe=False)
    return JsonResponse({'error': 'Invalid request.'})