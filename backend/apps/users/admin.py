from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for User model.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'agency', 'is_active')
    list_filter = ('role', 'agency', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Info'), {
            'fields': ('role', 'agency', 'phone')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional Info'), {
            'fields': ('role', 'agency', 'phone', 'first_name', 'last_name', 'email')
        }),
    )
