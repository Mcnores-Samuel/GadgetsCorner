from django.contrib import admin
from ..models.main_storage import MainStorage
from ..customfilters.date_filters import YesterdayFilter
from ..customfilters.year_months_filter import YearMonthFilter
from ..customfilters.agent_filter import AgentFilter, SpecialAgentsFilter


class MainStorageAdmin(admin.ModelAdmin):
    list_display = ('assigned_to', 'device_imei', 'device_imei_2', 'name', 'phone_type', 'spec', 'recieved', 'on_display',
                    'faulty', 'in_stock', 'pending', 'missing', 'assigned', 'sold', 'paid', 'issue', 'sales_type', 'cost', 'price', 'contract_no',
                    'assigned_from', 'updated_by', 'entry_date', 'stock_out_date','collected_on', 'comment', 'supplier'
    )
    search_fields = ('device_imei', 'device_imei_2', 'name', 'phone_type', 'entry_date', 'category', 'agent__username',
                     'contract_no', 'sales_type', 'stock_out_date', 'assigned', 'sold', 'paid', 'collected_on', 'supplier')
    list_filter = ('in_stock', 'on_display', 'missing', 'faulty', 'pending', 'category', 'supplier', 'sales_type', 'assigned', 'sold', 'paid',
                   'entry_date', 'collected_on', 'stock_out_date', SpecialAgentsFilter, AgentFilter, YesterdayFilter, YearMonthFilter)
    
    list_per_page = 50

    actions = ['verify_stock_recieved',
               'unverify_stock_recieved', 'unassign_select', 'mark_as_sold',
               'missing', 'approve_pending', 'unapprove_pending']
    
    class Meta:
        ordering = ['-entry_date']

    def assigned_to(self, obj):
        return obj.agent
    
    def missing(self, request, queryset):
        for obj in queryset:
            if obj:
                obj.missing = True
                obj.save()
    missing.short_description = "Mark as missing"

    
    def mark_as_sold(self, request, queryset):
        """Mark the phone as sold"""
        for obj in queryset:
            if obj:
                obj.in_stock = False
                obj.assigned = True
                obj.recieved = True
                obj.sold = True
                obj.save()
    mark_as_sold.short_description = "Mark as sold"

    def approve_pending(self, request, queryset):
        """Approve pending phones"""
        for obj in queryset:
            if obj:
                obj.pending = False
                obj.save()
    approve_pending.short_description = "Approve pending Sales"

    def unapprove_pending(self, request, queryset):
        """Unapprove pending phones"""
        for obj in queryset:
            if obj:
                obj.pending = True
                obj.save()
    unapprove_pending.short_description = "Unapprove pending Sales"

    def verify_stock_recieved(self, request, queryset):
        """Verify stock recieved by the agent"""
        for obj in queryset:
            if obj:
                obj.recieved = True
                obj.save()
    verify_stock_recieved.short_description = "Verify stock recieved"

    def unverify_stock_recieved(self, request, queryset):
        """Unverify stock recieved by the agent"""
        for obj in queryset:
            if obj:
                obj.recieved = False
                obj.save()
    unverify_stock_recieved.short_description = "Unverify stock recieved"

    def unassign_select(self, request, queryset):
        """Unassign the phone from an agent in MainStorage when requested"""
        for obj in queryset:
            try:
                device = MainStorage.objects.get(device_imei=obj.device_imei, in_stock=True,
                                                 assigned=True)
                device.agent = None
                device.recieved = False
                device.assigned = False
                device.in_stock = True
                device.sold = False
                device.contract_no = '##'
                device.sales_type = '##'
                device.stock_out_date = device.entry_date
                device.save()
            except MainStorage.DoesNotExist:
                pass
    unassign_select.short_description = "Unassign selected phones"

    def save_model(self, request, obj, form, change):
        """Override the save_model method to add the current user to the agent field"""
        data = MainStorage.objects.filter(name=obj.name,
                                          in_stock=True).first()
        if not change and data:
                obj.category = data.category
                obj.phone_type = data.phone_type
                obj.spec = data.spec
                obj.screen_size = data.screen_size
                obj.battery = data.battery
                obj.camera = data.camera
                obj.os = data.os
                obj.sales_type = data.sales_type
                obj.contract_no = data.contract_no
                if not obj.assigned_from:
                    obj.assigned_from = data.assigned_from
                obj.updated_by = request.user.username
                obj.recieved = True
                obj.assigned = True
                obj.save()
                return super().save_model(request, obj, form, change)
        obj.updated_by = request.user.username
        obj.save()
        return super().save_model(request, obj, form, change)