from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Agency


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    """
    Admin for Agency model.
    """
    list_display = ('name', 'code', 'orientation', 'hibernation_start', 'hibernation_end', 'is_active')
    list_filter = ('orientation', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'email')
    ordering = ('name',)

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'code', 'address', 'phone', 'email')
        }),
        (_('Display Settings'), {
            'fields': ('orientation', 'hibernation_start', 'hibernation_end', 'logo')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
