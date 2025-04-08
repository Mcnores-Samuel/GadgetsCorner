"""This module contains the views for revenue data."""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from gadgetsCorner.models.main_storage import MainStorage
from gadgetsCorner.models.accessories import Accessory_Sales
from gadgetsCorner.models.appliances import Appliance_Sales
from gadgetsCorner.models.refarbished_devices import RefarbishedDevicesSales
from django.utils import timezone
from django.db.models import Sum
import calendar


@login_required
def current_year_revenue(request):
    """Retruns the total revenue for the current year including other data calculations."""
    data = None
    current_year = timezone.now().year

    if request.method == 'GET' and request.user.is_superuser:
        data = MainStorage.objects.filter(stock_out_date__year=current_year,
            in_stock=False, sold=True, missing=False, pending=False, assigned=True
        )

    # Extract values (handle None cases)
    access_cost = Accessory_Sales.get_total_cost(year=current_year)
    access_revenue = Accessory_Sales.get_revenue(year=current_year)
    total_accessories_sold = Accessory_Sales.get_total_sold(year=current_year)
    appl_cost = Appliance_Sales.get_total_cost(year=current_year)
    appl_revenue = Appliance_Sales.get_revenue(year=current_year)
    total_appliances_sold = Appliance_Sales.get_total_sold(year=current_year)
    refarb_cost = RefarbishedDevicesSales.get_total_cost(year=current_year)
    refarb_revenue = RefarbishedDevicesSales.get_revenue(year=current_year)
    total_refarbished_sold = RefarbishedDevicesSales.get_total_sold(year=current_year)

    if data is None:
        return JsonResponse({'error': 'Invalid request.'})
    
    total = data.count()
    items_with_both_ps = data.filter(price__gt=0, cost__gt=0)
    t_items_wbps = items_with_both_ps.count()
    revenue_for_itwbps = items_with_both_ps.aggregate(
        total_revenue=Sum('price'),
        total_cost=Sum('cost')
    )

    items_with_cost_only = data.filter(price=0, cost__gt=0)
    total_items_with_cost_only = items_with_cost_only.count()
    revenue_for_itwco = items_with_cost_only.aggregate(
        total_revenue=Sum('price'),
        total_cost=Sum('cost')
    )

    items_with_price_only = data.filter(price__gt=0, cost=0)
    total_items_with_price_only = items_with_price_only.count()
    revenue_for_itwpo = items_with_price_only.aggregate(
        total_revenue=Sum('price'),
        total_cost=Sum('cost')
    )

    items_with_no_ps = data.filter(price=0, cost=0)
    total_items_with_no_ps = items_with_no_ps.count()
    revenue_for_itwnps = items_with_no_ps.aggregate(
        total_revenue=Sum('price'),
        total_cost=Sum('cost')
    )

    context = {
        'year': current_year,
        'total_calculated': total + total_accessories_sold + total_appliances_sold + total_refarbished_sold,
        'both_price_and_cost': t_items_wbps + total_accessories_sold + total_appliances_sold + total_refarbished_sold,
        'revenue': revenue_for_itwbps['total_revenue'] + access_revenue + appl_revenue + refarb_revenue,
        'cost': revenue_for_itwbps['total_cost'] + access_cost + appl_cost + refarb_cost,
        'cost_only': total_items_with_cost_only,
        'revenue_for_itwco': revenue_for_itwco['total_revenue'],
        'cost_for_itwco': revenue_for_itwco['total_cost'],
        'price_only': total_items_with_price_only,
        'revenue_for_itwpo': revenue_for_itwpo['total_revenue'],
        'cost_for_itwpo': revenue_for_itwpo['total_cost'],
        'no_price_or_cost': total_items_with_no_ps,
        'revenue_for_itwnps': revenue_for_itwnps['total_revenue'],
        'cost_for_itwnps': revenue_for_itwnps['total_cost']
    }

    return JsonResponse(context)


@login_required
def revenue_by_category(request):
    """Returns the total revenue for the current year by category."""
    current_year = timezone.now().year
    categories = set()
    data = None

    if request.method == 'GET' and request.user.is_superuser:
        data = MainStorage.objects.filter(stock_out_date__year=current_year,
            in_stock=False, sold=True, missing=False, pending=False, assigned=True, cost__gt=0, price__gt=0,
        )
    
    if data is None:
        return JsonResponse({'error': 'Invalid request.'})
    
    for item in data:
        categories.add(item.category)
    categories = list(categories)
    revenueByCategory = []
    for category in categories:
        items = data.filter(category=category)
        cost = items.aggregate(total_cost=Sum('cost'))
        revenue = items.aggregate(total_revenue=Sum('price'))
        revenueByCategory.append(
            {
                'category': category,
                'total_cost': cost['total_cost'],
                'total_revenue': revenue['total_revenue']
            }
        )
    revenueByCategory.append(
        {
            'category': 'Accessories',
            'total_cost': Accessory_Sales.get_total_cost(year=current_year),
            'total_revenue': Accessory_Sales.get_revenue(year=current_year)
        }
    )
    revenueByCategory.append(
        {
            'category': 'Appliances',
            'total_cost': Appliance_Sales.get_total_cost(year=current_year),
            'total_revenue': Appliance_Sales.get_revenue(year=current_year)
        }
    )
    revenueByCategory.append(
        {
            'category': 'Refarbished Devices',
            'total_cost': RefarbishedDevicesSales.get_total_cost(year=current_year),
            'total_revenue': RefarbishedDevicesSales.get_revenue(year=current_year)
        }
    )
    return JsonResponse(revenueByCategory, safe=False)


@login_required
def calculateCreditRevenue(request):
    """Calculate the credit revenue Sort by Month"""
    if request.method == 'GET':
        months = list(calendar.month_name[1:])
        revenue = {}
        if request.user.is_superuser:
            for month in months:
                items = MainStorage.objects.filter(
                    in_stock=False, sold=True, pending=False, missing=False, cost__gt=0, price__gt=0,
                    assigned=True, sales_type='Loan', stock_out_date__month=months.index(month)+1,
                    stock_out_date__year=timezone.now().year)
                total = sum([item.price for item in items])
                revenue[month] = total
        return JsonResponse(revenue, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def calculateCashRevenue(request):
    """Calculate the cash revenue Sort by Month"""
    if request.method == 'GET':
        months = list(calendar.month_name[1:])
        revenue = {}
        if request.user.is_superuser:
            for month in months:
                total_revenue = 0
                total_revenue = Accessory_Sales.get_revenue(
                    month=months.index(month)+1, year=timezone.now().year
                ) + Appliance_Sales.get_revenue(
                    month=months.index(month)+1, year=timezone.now().year
                ) + RefarbishedDevicesSales.get_revenue(
                    month=months.index(month)+1, year=timezone.now().year
                )
                items = MainStorage.objects.filter(
                    in_stock=False, sold=True, pending=False, missing=False, cost__gt=0, price__gt=0,
                    assigned=True, sales_type='Cash', stock_out_date__month=months.index(month)+1,
                    stock_out_date__year=timezone.now().year)
                total = sum([item.price for item in items])
                revenue[month] = total + total_revenue
        return JsonResponse(revenue, safe=False)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def lastyearBycurrentMonth(request):
    """Calculate the total revenue for the last year by the current month."""
    if request.method == 'GET':
        current_month = timezone.now().month
        last_year = timezone.now().year - 1
        data = None
        if request.user.is_superuser:
            data = MainStorage.objects.filter(
                in_stock=False, sold=True, missing=False, pending=False, assigned=True,
                stock_out_date__month__lte=current_month,
                stock_out_date__year=last_year, price__gt=0,
            )
        group_by_month = {}
        for i in range(1, current_month+1):
            items = data.filter(stock_out_date__month=i)
            total = sum([item.price for item in items])
            total += Accessory_Sales.get_revenue(
                month=i, year=last_year
            ) + Appliance_Sales.get_revenue(
                month=i, year=last_year
            ) + RefarbishedDevicesSales.get_revenue(
                month=i, year=last_year
            )
            group_by_month[timezone.datetime(last_year, i, 1).strftime('%B')] = total
        return JsonResponse(group_by_month)
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def revenue_growth(request):
    """Calculate the revenue growth."""
    if request.method == 'GET':
        current_year = timezone.now().year
        last_year = current_year - 1
        current_month = timezone.now().month
        current_year_data = None
        last_year_data = None
        if request.user.is_superuser:
            current_year_data = MainStorage.objects.filter(
                in_stock=False, sold=True, missing=False, pending=False, assigned=True,
                stock_out_date__year=current_year, price__gt=0, stock_out_date__month__lte=current_month
            )
            last_year_data = MainStorage.objects.filter(
                in_stock=False, sold=True, missing=False, pending=False, assigned=True,
                stock_out_date__year=last_year, price__gt=0, stock_out_date__month__lte=current_month
            )
        current_year_revenue = sum([item.price for item in current_year_data])
        current_year_revenue += Accessory_Sales.get_revenue(
            year=current_year
        ) + Appliance_Sales.get_revenue(
            year=current_year
        ) + RefarbishedDevicesSales.get_revenue(
            year=current_year
        )
        last_year_revenue = sum([item.price for item in last_year_data])
        last_year_revenue += Accessory_Sales.get_revenue(
            year=last_year
        ) + Appliance_Sales.get_revenue(
            year=last_year
        )
        if current_year_revenue == 0 and last_year_revenue == 0:
            return JsonResponse({'growth': 0})
        if last_year_revenue == 0:
            return JsonResponse({'growth': 100})
        
        if current_year_revenue == 0:
            return JsonResponse({'growth': -100})
        growth = (current_year_revenue - last_year_revenue) / last_year_revenue * 100
        growth = round(growth, 2)
        return JsonResponse({'growth': growth})
    return JsonResponse({'error': 'Invalid request.'})


@login_required
def average_order_value(request):
    """Calculate the average order value."""
    if request.method == 'GET':
        current_year = timezone.now().year
        current_month = timezone.now().month
        data = MainStorage.objects.filter(
            in_stock=False, sold=True, missing=False, pending=False, assigned=True,
            stock_out_date__year=current_year, cost__gt=0, price__gt=0, stock_out_date__month__lte=current_month
        )
        total_revenue = sum([item.price for item in data])
        total_revenue += Accessory_Sales.get_revenue(
            month=current_month, year=current_year
        ) + Appliance_Sales.get_revenue(
            month=current_month, year=current_year
        ) + RefarbishedDevicesSales.get_revenue(
            month=current_month, year=current_year
        )
        total_orders = data.count()
        total_orders += Accessory_Sales.get_total_sold(
            month=current_month, year=current_year
        ) + Appliance_Sales.get_total_sold(
            month=current_month, year=current_year
        ) + RefarbishedDevicesSales.get_total_sold(
            month=current_month, year=current_year
        )
        if total_orders == 0:
            return JsonResponse({'average_order_value': 0})
        average_order_value = total_revenue / total_orders
        average_order_value = round(average_order_value, 2)
        return JsonResponse({'average_order_value': average_order_value})
    return JsonResponse({'error': 'Invalid request.'})