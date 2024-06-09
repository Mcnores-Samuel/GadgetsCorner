"""Admin site for user profile model."""
from django.contrib.auth.admin import UserAdmin


class UserAdminModel(UserAdmin):
    """User admin model."""
    list_display = (
        'email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined',
        'last_login'
    )

    list_per_page = 20
    
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    search_fields = ('email', 'username', 'first_name', 'last_name')