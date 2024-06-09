#!/usr/bin/env python3
from django import forms
from ..models.main_storage import MainStorage
from django.utils import timezone


class CombinedDataForm(forms.Form):
    """
    The CombinedDataForm is a Django form used for collecting and processing
    combined customer and phone data during the phone purchasing process.

    This form allows the user, typically an agent, to gather essential customer
    information and select a phone for sale. It is designed to facilitate the
    creation of customer and phone records simultaneously in the database.

    Form Fields:
    - Customer Information:
      - customer_name: Full name of the customer.
      - national_id: National identification number of the customer.
      - customer_contact: Primary contact number of the customer.
      - second_contact: Secondary contact number of the customer (optional).
      - first_witness_name: Name of the first witness.
      - first_witness_contact: Contact number of the first witness.
      - second_witness_name: Name of the second witness.
      - second_witness_contact: Contact number of the second witness.
      - customer_location: Customer's residential location.
      - nearest_school: Nearest school to the customer's location.
      - nearest_market_church_hospital: Nearest market, church, or hospital.
      - customer_email: Customer's email address (optional).

    - Phone Selection:
      - phone_type: Choice field for selecting the type of phone.
      - imei_number: Unique identification number of the selected phone.
      - payment_period: Payment period or plan for the phone.
    
    Methods:
    - __init__: Initializes the form, sets choices for phone_type based on
      available phone references, and dynamically sets choices for imei_number
      based on the agent's available stock.
    - save: Processes and saves the combined data, creating customer and phone
      records in the database.

    Usage:
    Agents or users can fill out this form to gather customer data and select a
    phone for sale. Upon submission, the form saves both customer and phone
    records in the database, facilitating efficient management of customer
    information and phone sales.

    Note:
    This form is typically used in a view where user authentication and data
    validation are handled.
    """
    PAYMENT = [
        ('Cash', 'Cash'),
        ('Loan', 'Loan'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT, widget=forms.Select(
            attrs={
                'class': 'form-control d-inline-block',
                'placeholder': 'Payment Method',
                'required': 'required',
            }
        ), label='Sales Type',
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def process_cash_payment(self, data_id):
        """
        The process_cash_payment function is responsible for processing a
        payment when the selected payment method is "Cash." In this scenario, customer
        data is not collected, and the function focuses on creating phone data records
        for the transaction.
        
        Functionality:
                Retrieves the relevant information about the selected phone and phone reference.
                Creates a phone data record in the database, capturing details such as the agent,
                IMEI number, phone type, selling price, deposit, and payment period.
                Returns the newly created phone data object.
        Usage:
                This function is called when a user selects "Cash" as the payment method during
                the phone purchasing process. It ensures that the transaction details are recorded
                without the need for collecting customer data.
        """
        selected_device = MainStorage.objects.get(id=data_id)
        selected_device.in_stock = False
        selected_device.sold = True
        selected_device.pending = True
        selected_device.stock_out_date = timezone.now()
        selected_device.sales_type = 'Cash'
        selected_device.save()
        return selected_device

    def process_loan_payment(self, data_id):
        """
        The process_loan_payment function handles the processing of a payment
        when the selected payment method is "Loan." In this case, it collects
        customer data and creates both customer and phone data records in the database.

        Functionality:
        - Retrieves the relevant information about the selected phone and phone reference.
        - Marks the selected phone as sold and updates its status in the database.

        Parameters:
        - data_id: The ID of the selected phone data record.

        Returns:
        - If the phone has already been sold, it returns a message indicating that
          the device is no longer available.
        """
        check_if_sold_already = MainStorage.objects.get(id=data_id)
        if not check_if_sold_already.sold:
            selected_device = MainStorage.objects.get(id=data_id)
            selected_device.in_stock = False
            selected_device.sold = True
            selected_device.pending = True
            selected_device.sales_type = 'Loan'
            selected_device.stock_out_date = timezone.now()
            selected_device.save()
            return selected_device
        else:
            return 'already sold'