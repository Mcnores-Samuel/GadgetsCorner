"""This model represent the entire stock available and sold in all posts."""
from ...models.main_storage import MainStorage
from ...models.accessories import Accessory_Sales
from ...models.appliances import Appliance_Sales
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class MainStorageAnalysis:
    """This class contains methods for analyzing the MainStorage model."""
    def __init__(self, *args, **kwargs):
        pass

    def get_daily_sales(self, sales_type, day=timezone.now().date()):
        """Returns a dictionary containing the daily sales data."""
        data_set = MainStorage.objects.filter(
            stock_out_date=day,
            sold=True, in_stock=False,
            sales_type=sales_type)
        sales = {}
        for data in data_set:
            sales[data.phone_type] = sales.get(data.phone_type, 0) + 1
        return sales
    
    def get_weekly_sales(self, sales_type):
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
            sold=True, in_stock=False,
            sales_type=sales_type)
        if sales_type == 'Cash':
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
    
    # def get_monthly_sales_by_agents(self, sales_type):
    #     """Returns a dictionary containing the monthly sales data."""
    #     agents = AgentProfile.objects.all().order_by('user__username')
    #     sales_by_agent = {}
    #     current_month = timezone.now().date().month
    #     current_year = timezone.now().date().year
    #     total_sales = MainStorage.objects.filter(
    #         stock_out_date__month=current_month,
    #         stock_out_date__year=current_year,
    #         sold=True, in_stock=False, sales_type=sales_type,
    #         missing=False, pending=False, assigned=True,
    #         recieved=True, issue=False, faulty=False)
    #     for agent in agents:
    #         sales_by_agent[str(agent.user.username).lower().capitalize()] = MainStorage.objects.filter(
    #                 agent=agent.user,
    #                 stock_out_date__month=current_month,
    #                 stock_out_date__year=current_year,
    #                 sold=True, in_stock=False, sales_type=sales_type,
    #                 missing=False, pending=False, assigned=True,
    #                 recieved=True, issue=False, faulty=False).count()
    #     sales_by_agent['Total'] = total_sales.count()
    #     sales_by_agent = sorted(sales_by_agent.items(), key=lambda x: x[1], reverse=True)
    #     return sales_by_agent
    
    def get_agent_stock_in(self, agent):
        """Returns a dictionary containing the agent's stock in data."""
        stock_in = MainStorage.objects.filter(
            agent=agent,
            in_stock=True, assigned=True,
            missing=False, sold=False, pending=False,
            faulty=False, issue=False, recieved=True, paid=False)
        stock = {}
        for data in stock_in:
            stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
        return stock
    
    def get_agent_stock_out(self, agent):
        """Returns a dictionary containing the agent's stock out data."""
        current_month = timezone.now().date().month
        current_year = timezone.now().date().year
        stock_out = MainStorage.objects.filter(
            agent=agent, in_stock=False,
            assigned=True, missing=False,
            sold=True, pending=False, faulty=False,
            stock_out_date__month=current_month,
            stock_out_date__year=current_year,
            recieved=True, issue=False)
        stock = {}
        for data in stock_out:
            stock[data.phone_type] = stock.get(data.phone_type, 0) + 1
        stock = sorted(stock.items(), key=lambda x: x[1], reverse=True)
        return stock
    
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
        return sales
    
    # def overall_stock(self):
    #     """This function returns a JSON object containing
    #     the overall stock data.
    #     """
    #     agents = AgentProfile.objects.all().order_by('user__username')
    #     stock = 0
    #     for agent in agents:
    #         stock += MainStorage.objects.filter(
    #             agent=agent.user,
    #             in_stock=True, assigned=True,
    #             sold=False, missing=False,
    #             pending=False, faulty=False, recieved=True,
    #             issue=False).count()
    #     return stock
    
    # def overall_sales(self):
    #     """This function returns a JSON object containing
    #     the overall sales data.
    #     """
    #     month = timezone.now().date().month
    #     year = timezone.now().date().year

    #     agents = AgentProfile.objects.all().order_by('user__username')
    #     sales = 0
    #     for agent in agents:
    #         sales += MainStorage.objects.filter(
    #             agent=agent.user,
    #             in_stock=False, assigned=True,
    #             sold=True, missing=False,
    #             pending=False, faulty=False,
    #             stock_out_date__month=month,
    #             stock_out_date__year=year).count()
    #     return sales
    
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
            total += accessory.price_sold
        for appliance in appliances:
            total += appliance.price_sold
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
        total = 0
        for phone in phones:
            total += phone.price - phone.cost
        for accessory in accessories:
            total += accessory.profit
        for appliance in appliances:
            total += appliance.profit
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
        total = 0
        for phone in phones:
            if phone.price < phone.cost:
                total += phone.cost - phone.price
        return total