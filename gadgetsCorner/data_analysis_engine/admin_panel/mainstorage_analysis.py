"""This model represent the entire stock available and sold in all posts."""
from ...models.main_storage import MainStorage
from ...models.accessories import Accessory_Sales
from ...models.appliances import Appliance_Sales
from ...models.daily_expenses import DailyExpenses
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class MainStorageAnalysis:
    """This class contains methods for analyzing the MainStorage model."""
    def __init__(self, *args, **kwargs):
        pass

    def get_daily_sales(self, day=timezone.now().date()):
        """Returns a dictionary containing the daily sales data."""
        data_set = MainStorage.objects.filter(
            stock_out_date=day,
            sold=True, in_stock=False)
        sales = {}
        for data in data_set:
            sales[data.phone_type] = sales.get(data.phone_type, 0) + 1
        
        accessories = Accessory_Sales.objects.filter(
            date_sold=day)
        
        for accessory in accessories:
            sales[f"{accessory.item}({accessory.model})"] = accessory.total
        
        appliances = Appliance_Sales.objects.filter(
            date_sold=day)
        
        for appliance in appliances:
            sales[f"{appliance.item}({appliance.model})"] = appliance.total
        return sales
    
    def get_weekly_sales(self):
        """Returns a dictionary containing the weekly sales data."""
        current_week = timezone.now().date()
        week_days = ['Monday', 'Tuesday', 'Wednesday',
                     'Thursday', 'Friday', 'Saturday',
                     'Sunday']
        days = {day: [] for day in week_days}
        monday = current_week - timezone.timedelta(
            days=current_week.weekday())
        sunday = monday + timezone.timedelta(days=6)

        data_set = MainStorage.objects.filter(
            stock_out_date__range=[monday, sunday],
            sold=True, in_stock=False)
        
        accessories = Accessory_Sales.objects.filter(
            date_sold__range=[monday, sunday])
        for accessory in accessories:
            item = {f"{accessory.item}({accessory.model})": accessory.total}
            days[week_days[accessory.date_sold.weekday()]].append(item)
            item = {}

        appliances = Appliance_Sales.objects.filter(
            date_sold__range=[monday, sunday])
        for appliance in appliances:
            item = {f"{appliance.item}({appliance.model})": appliance.total}
            days[week_days[appliance.date_sold.weekday()]].append(item)
            item = {}

        for data in data_set:
            item = {data.phone_type: 1}
            days[week_days[data.stock_out_date.weekday()]].append(item)
            item = {}
        return days
    
    def get_monthly_sales(self):
        """Returns a dictionary containing the monthly sales data."""
        current_month = timezone.now().date().month
        current_year = timezone.now().date().year
        data_set = MainStorage.objects.filter(
            stock_out_date__month=current_month,
            stock_out_date__year=current_year,
            sold=True, in_stock=False)
        sales = {}
        total = 0
        for data in data_set:
            total += 1
            sales[f"{data.stock_out_date}"] = sales.get(f"{data.stock_out_date}", 0) + 1

        accessories = Accessory_Sales.objects.filter(
            date_sold__month=current_month,
            date_sold__year=current_year)
        for accessory in accessories:
            total += accessory.total
            sales[f"{accessory.date_sold.date()}"] = sales.get(f"{accessory.date_sold.date()}", 0) + accessory.total

        appliances = Appliance_Sales.objects.filter(
            date_sold__month=current_month,
            date_sold__year=current_year)
        for appliance in appliances:
            total += appliance.total
            sales[f"{appliance.date_sold.date()}"] = sales.get(f"{appliance.date_sold.date()}", 0) + appliance.total
        sales['Total'] = total
        sales = {key: value for key, value in sorted(sales.items(), key=lambda item: item[0])}
        return sales

    def get_sales_for_all_months(self, agent):
        """Returns a dictionary containing the agent's sales for all months."""
        months = ['January', 'February', 'March', 'April', 'May',
                  'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        sales = {}
        for month in months:
            total = MainStorage.objects.filter(
                in_stock=False,
                assigned=True, sold=True, missing=False,
                pending=False, stock_out_date__month=months.index(month)+1,
                stock_out_date__year=timezone.now().date().year,
                issue=False, recieved=True, faulty=False).count()
            sales[month] = total

        for month in months:
            data = Accessory_Sales.objects.filter(
                date_sold__month=months.index(month)+1,
                date_sold__year=timezone.now().date().year)
            for item in data:
                sales[month] += item.total
            data = Appliance_Sales.objects.filter(
                date_sold__month=months.index(month)+1,
                date_sold__year=timezone.now().date().year)
            for item in data:
                sales[month] += item.total
        return sales
    
    def pending_sales(self, request):
        """This function returns a list of all pending sales.
        It also returns the total number of pending sales.
        """
        all_pending_sales = MainStorage.objects.filter(
            pending=True, in_stock=False,
            assigned=True, sold=True, missing=False,
            faulty=False, issue=False).order_by('stock_out_date')
        total_pending_sales = all_pending_sales.count()
        
        all_pending_sales = Paginator(all_pending_sales, 12)
        page = request.GET.get('page')

        try:
            all_pending_sales = all_pending_sales.get_page(page)
        except PageNotAnInteger:
            all_pending_sales = all_pending_sales.page(1)
        except EmptyPage:
            all_pending_sales = all_pending_sales.page(all_pending_sales.num_pages)
        return all_pending_sales, total_pending_sales
    
    def estimated_revenue(self):
        """This function returns the estimated revenue from all sales."""
        current_month = timezone.now().date().month
        current_year = timezone.now().date().year
        phones = MainStorage.objects.filter(
            in_stock=False, assigned=True,
            sold=True, missing=False,
            pending=False, stock_out_date__month=current_month,
            stock_out_date__year=current_year)
        accessories = Accessory_Sales.objects.filter(
            date_sold__month=current_month,
            date_sold__year=current_year)
        appliances = Appliance_Sales.objects.filter(
            date_sold__month=current_month,
            date_sold__year=current_year)
        total = 0
        for phone in phones:
            total += phone.price
        for accessory in accessories:
            total += (accessory.price_sold * accessory.total)
        for appliance in appliances:
            total += (appliance.price_sold * appliance.total)
        return total
    
    def estimated_profit(self):
        """This function returns the estimated profit from all sales."""
        current_month = timezone.now().date().month
        current_year = timezone.now().date().year
        phones = MainStorage.objects.filter(
            in_stock=False, assigned=True,
            sold=True, missing=False,
            pending=False, stock_out_date__month=current_month,
            stock_out_date__year=current_year)
        accessories = Accessory_Sales.objects.filter(
            date_sold__month=current_month,
            date_sold__year=current_year)
        appliances = Appliance_Sales.objects.filter(
            date_sold__month=current_month,
            date_sold__year=current_year)
        daily_expenses = DailyExpenses.objects.filter(
            date__month=current_month,
            date__year=current_year)
        
        total = 0
        for phone in phones:
            total += phone.price - phone.cost
        for accessory in accessories:
            total += accessory.profit
        for appliance in appliances:
            total += appliance.profit
        for expense in daily_expenses:
            total -= expense.amount
        return total
    
    def estimated_loss(self):
        """This function returns the estimated loss from all sales."""
        current_month = timezone.now().date().month
        current_year = timezone.now().date().year
        phones = MainStorage.objects.filter(
            in_stock=False, assigned=True,
            sold=True, missing=False,
            pending=False, stock_out_date__month=current_month,
            stock_out_date__year=current_year)
        accessories = Accessory_Sales.objects.filter(
            date_sold__month=current_month,
            date_sold__year=current_year)
        total = 0
        for phone in phones:
            if phone.price < phone.cost:
                total += phone.cost - phone.price
        for accessory in accessories:
            if accessory.cost> accessory.price_sold:
                total += (accessory.cost * accessory.total) - (accessory.price_sold * accessory.total)
        return total
    
    def total_sold(self, month, year):
        """This function returns the sales for a given month and year."""
        phones = MainStorage.get_total_sold(month, year)
        accessories = Accessory_Sales.get_total_sold(month, year)
        appliances = Appliance_Sales.get_total_sold(month, year)
        total = phones + accessories + appliances
        return total