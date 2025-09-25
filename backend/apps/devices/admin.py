from django.contrib import admin
from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip_address', 'agency', 'status', 'last_seen', 'is_active']
    list_filter = ['status', 'agency', 'is_active', 'orientation']
    search_fields = ['name', 'ip_address', 'mac_address']
    readonly_fields = ['last_seen']
    ordering = ['agency', 'name']
