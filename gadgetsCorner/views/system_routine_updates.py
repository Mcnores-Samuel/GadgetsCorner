"""This module contains the view functions for system routine updates."""
from django.utils import timezone
from ..models.main_storage import MainStorage
from ..models.accessories import Accessories, Accessory_Sales
from ..models.appliances import Appliances, Appliance_Sales
from ..models.daily_expenses import DailyExpenses
from ..models.user_profile import UserProfile
from webpush import send_user_notification
from django.http import JsonResponse
from django.core.mail import send_mail
from os import environ


def system_routine_update(request):
    """Send a system routine update to admin users.

    This function sends a system routine update to all admin users
    via web push notifications and email. The update contains
    information about the current system status and performance.

    Args:
        request: The HTTP request object.

    Returns:
        A JSON response indicating the status of the update.

    Raises:
        None.
    """
    if request.method == 'GET':
        # Get the current day's date
        today = timezone.now().date()
        # Send an evening update email
        today = today.strftime('%d %B, %Y')
        subject = "Daily Stock And Sales Update - {}".format(today)
        accessory_sales_details = {}
        total_sales = 0
        revenue_generated = 0
        net_profit_generated = 0
        total_loss = 0
        total_expenses = 0
        expenses_details = {}
        expenses = DailyExpenses.objects.filter(date__date=timezone.now().date())
        for expense in expenses:
            total_expenses += expense.amount
            if expense.name in expenses_details:
                expenses_details[expense.name] += expense.amount
            else:
                expenses_details[expense.name] = expense.amount
        accessory_sales = Accessory_Sales.objects.filter(date_sold__date=timezone.now().date())
        for sale in accessory_sales:
            if sale.item + f" ({sale.model})" in accessory_sales_details:
                total_sales += sale.total
                revenue_generated += sale.total * sale.price_sold
                net_profit_generated += sale.profit
                if sale.cost > sale.price_sold:
                    total_loss += sale.cost - sale.price_sold
                accessory_sales_details[sale.item + f" ({sale.model})"] += sale.total
            else:
                total_sales += sale.total
                revenue_generated += sale.total * sale.price_sold
                net_profit_generated += sale.profit
                if sale.cost > sale.price_sold:
                    total_loss += sale.cost - sale.price_sold
                accessory_sales_details[sale.item + f" ({sale.model})"] = sale.total

        appliance_sales_details = {}
        appliance_sales = Appliance_Sales.objects.filter(date_sold__date=timezone.now().date())
        for sale in appliance_sales:
            if sale.item + f" ({sale.model})" in appliance_sales_details:
                total_sales += sale.total
                revenue_generated += sale.total * sale.price_sold
                net_profit_generated += sale.profit
                if sale.cost > sale.price_sold:
                    total_loss += sale.cost - sale.price_sold
                appliance_sales_details[sale.item + f" ({sale.model})"] += sale.total
            else:
                total_sales += sale.total
                revenue_generated += sale.total * sale.price_sold
                net_profit_generated += sale.profit
                if sale.cost > sale.price_sold:
                    total_loss += sale.cost - sale.price_sold
                appliance_sales_details[sale.item + f" ({sale.model})"] = sale.total

        net_profit_generated = net_profit_generated - total_loss - total_expenses

        phone_sales = MainStorage.objects.filter(
            in_stock=False, pending=False, issue=False,
            sold=True, faulty=False, missing=False, stock_out_date=timezone.now().date())
        phone_sales_details = {}
        for sale in phone_sales:
            if sale.phone_type + f" ({sale.phone_type}) ({sale.spec})" in phone_sales_details:
                total_sales += 1
                revenue_generated += sale.price
                if sale.price > sale.cost:
                    net_profit_generated += sale.price - sale.cost
                else:
                    total_loss += sale.cost - sale.price
                phone_sales_details[sale.phone_type + f" ({sale.phone_type}) ({sale.spec})"] += 1
            else:
                total_sales += 1
                revenue_generated += sale.price
                if sale.price > sale.cost:
                    net_profit_generated += sale.price - sale.cost
                else:
                    total_loss += sale.cost - sale.price
                phone_sales_details[sale.phone_type + f" ({sale.phone_type}) ({sale.spec})"] = 1
        
        accessory_stock = Accessories.objects.all()
        appliance_stock = Appliances.objects.all()
        total_accessories = 0
        total_appliances = 0
        total_phone = 0
        store_value_estimate = 0
        accessory_stock_details = {}
        appliance_stock_details = {}
        phone_stock_details = {}

        for accessory in accessory_stock:
            total_accessories += accessory.total
            if accessory.item + f" ({accessory.model})" in accessory_stock_details:
                store_value_estimate += accessory.total * accessory.cost_per_item
                accessory_stock_details[accessory.item + f" ({accessory.model})"] += accessory.total
            else:
                store_value_estimate += accessory.total * accessory.cost_per_item
                accessory_stock_details[accessory.item + f" ({accessory.model})"] = accessory.total

        for appliance in appliance_stock:
            total_appliances += appliance.total
            if appliance.name + f" ({appliance.model})" in appliance_stock_details:
                store_value_estimate += appliance.total * appliance.cost
                appliance_stock_details[appliance.name + f" ({appliance.model})"] += appliance.total
            else:
                store_value_estimate += appliance.total * appliance.cost
                appliance_stock_details[appliance.name + f" ({appliance.model})"] = appliance.total

        phone_stock = MainStorage.objects.filter(
            in_stock=True, pending=False, issue=False, sold=False, faulty=False, missing=False)
        
        for phone in phone_stock:
            total_phone += 1
            if phone.phone_type + f" ({phone.phone_type}) ({phone.spec})" in phone_stock_details:
                store_value_estimate += phone.cost
                phone_stock_details[phone.phone_type + f" ({phone.phone_type}) ({phone.spec})"] += 1
            else:
                store_value_estimate += phone.cost
                phone_stock_details[phone.phone_type + f" ({phone.phone_type}) ({phone.spec})"] = 1

        admin_list = UserProfile.objects.filter(is_staff=True, is_superuser=True)
        users = [admin.email for admin in admin_list ]
        html_message = f"""
            <html>
                            <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            color: #333;
                            margin: 0;
                            padding: 0;
                            width: 100%;
                            height: 100%;
                        }}
                        h1 {{
                            background-color: #022842;
                            color: white;
                            padding: 10px;
                            text-align: center;
                        }}
                        h2 {{
                            color: #022842;
                            text-align: center;
                            background-color: #f2f2f2;
                        }}
                        h3 {{
                            color: #022842;
                        }}
                        p {{
                            font-size: 14px;
                        }}
                        table {{
                            width: 100%;
                            border-collapse: collapse;
                        }}
                        th, td {{
                            border: 1px solid #f2f2f2;
                            padding: 8px;
                            text-align: left;
                        }}

                        th {{
                            background-color: #022842;
                            color: white;
                        }}

                        tr:nth-child(even) {{
                            background-color: #f2f2f2;
                        }}
                        .section-header {{
                            background-color: #f2f2f2;
                            padding: 5px;
                            border-left: 4px solid #022842;
                            margin-top: 20px;
                        }}
                        footer {{
                            background-color: #022842;
                            color: white;
                            padding: 10px;
                            text-align: center;
                            position: fixed;
                            bottom: 0;
                            width: 100%;
                        }}
                    </style>
                </head>
                <body>
                    <h1>Gadgets Corner System Updates - {today}</h1>
                    <h3>Total Sales: {total_sales}</h3>
                    <h3>Total Revenue Generated: MK{revenue_generated:,}</h3>
                    <h3>Total Net Profit Generated: MK{net_profit_generated:,}</h3>
                    <h3>Total Loss: MK{total_loss:,}</h3>
                    <h3>Total Expenses: MK{total_expenses:,}</h3>

                    <h2>Expenses Details</h2>
                    <table>
                        <tr>
                            <th>Expense</th>
                            <th>Amount</th>
                        </tr>
                        {"".join([f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in expenses_details.items()])}
                    </table>
                    
                    <h2>Accessories Sales Details</h2>
                    <table>
                        <tr>
                            <th>Item</th>
                            <th>Total Sold</th>
                        </tr>
                        {"".join([f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in accessory_sales_details.items()])}
                    </table>
                    <h2>Appliance Sales Details</h2>
                    <table>
                        <tr>
                            <th>Item</th>
                            <th>Total Sold</th>
                        </tr>
                        {"".join([f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in appliance_sales_details.items()])}
                    </table>
                    <h2>Phone Sales Details</h2>
                    <table>
                        <tr>
                            <th>Item</th>
                            <th>Total Sold</th>
                        </tr>
                        {"".join([f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in phone_sales_details.items()])}
                    </table>
                    <h1>Current Stock Details</h1>
                    <h2>Current Store Value Estimate: MK{store_value_estimate:,}</h2>
                    <h2> Total Items In Stock: {total_accessories + total_appliances + total_phone}</h2>
                    <h2>Accessories Stock Details: Total => {total_accessories}</h2>
                    <table>
                        <tr>
                            <th>Item</th>
                            <th>Total In Stock</th>
                        </tr>
                        {"".join([f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in accessory_stock_details.items() if value > 0])}
                    </table>
                    <h2>Appliance Stock Details: Total => {total_appliances}</h2>
                    <table>
                        <tr>
                            <th>Item</th>
                            <th>Total In Stock</th>
                        </tr>
                        {"".join([f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in appliance_stock_details.items() if value > 0])}
                    </table>
                    <h2>Phone Stock Details: Total => {total_phone}</h2>
                    <table>
                        <tr>
                            <th>Item</th>
                            <th>Total In Stock</th>
                        </tr>
                        {"".join([f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in phone_stock_details.items() if value > 0])}
                    </table>
                    <footer>
                      <p>For more information, Please vist the <a href="https://gadgets-corner.vercel.app/">Gadgets Corner app</a> website.</p>
                      <p>For any queries, please contact the Gadgets Corner admin team.</p>
                    </footer>
                </body>
            </html>
        """
        from_email = 'system.gadgetscorner@gmail.com'
        send_mail(subject, '', from_email, users,
                  html_message=html_message, fail_silently=True)
        return JsonResponse({'status': 'Evening update sent successfully.'})
    return JsonResponse({'status': 'Invalid request method.'})
    