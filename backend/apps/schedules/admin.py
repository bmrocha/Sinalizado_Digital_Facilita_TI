from django.contrib import admin
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['content', 'start_time', 'end_time', 'priority', 'is_active', 'get_days_display']
    list_filter = ['is_active', 'priority', 'content__agency']
    search_fields = ['content__title']
    ordering = ['-priority', 'start_time']

    def get_days_display(self, obj):
        return ', '.join(obj.get_days_display())
    get_days_display.short_description = 'Days'
