from ..models.refarbished_devices import RefarbishedDevices
from django.contrib import admin


class RefarbishedDevicesAdmin(admin.ModelAdmin):
  """RefarbishedDevices admin class for the admin panel."""
  list_display = ('held_by', 'device_name', 'model', 'total', 'previous_total', 
                  'cost', 'original_price', 'date_added', 'date_modified')
  search_fields = ('held_by__user__username', 'device_name')
  list_per_page = 20