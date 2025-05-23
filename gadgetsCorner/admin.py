from django.contrib import admin
from .adminsites.admin_mainstorage import MainStorageAdmin
from .adminsites.admin_user_profile import UserAdminModel
from .adminsites.admin_user_avatars import UserAvatarAdmin
from .adminsites.admin_feedback import FeedbackAdmin
from .adminsites.admin_notification import NotificationsAdmin
from .adminsites.admin_contacts import ContactAdmin
from .adminsites.admin_refarbished_phone import RefarbishedDevicesAdmin, RefarbishedDevicesSalesAdmin
from .adminsites.accessories import AdminAccessories, AdminAccessary_Sales
from .adminsites.admin_appliances import AppliancesAdmin, Appliance_SalesAdmin
from .adminsites.admin_daily_expenses import DailyExpensesAdmin
from .models.user_profile import UserProfile, UserAvatar
from .models.main_storage import MainStorage
from .models.feedback import Feedback
from .models.notifications import Notifications
from .models.contacts import Contact
from .models.daily_expenses import DailyExpenses
from .models.refarbished_devices import RefarbishedDevices, RefarbishedDevicesSales
from .models.accessories import Accessories, Accessory_Sales
from .models.appliances import Appliances, Appliance_Sales



admin.site.site_url = "/gadgetsCorner/dashboard"
admin.site.site_header = "GADGETS CORNER ADMINISTRATION"
admin.site.site_title = "Gadgets Corner Admin"
admin.site.index_title = "Gadgets Corner"

admin.site.register(MainStorage, MainStorageAdmin)
admin.site.register(UserProfile, UserAdminModel)
admin.site.register(UserAvatar, UserAvatarAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(RefarbishedDevices, RefarbishedDevicesAdmin)
admin.site.register(Accessories, AdminAccessories)
admin.site.register(Accessory_Sales, AdminAccessary_Sales)
admin.site.register(Appliances, AppliancesAdmin)
admin.site.register(Appliance_Sales, Appliance_SalesAdmin)
admin.site.register(DailyExpenses, DailyExpensesAdmin)
admin.site.register(RefarbishedDevicesSales, RefarbishedDevicesSalesAdmin)