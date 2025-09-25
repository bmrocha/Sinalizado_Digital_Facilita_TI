from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('auth/', include('apps.users.urls')),
    path('agencies/', include('apps.agencies.urls')),
    path('content/', include('apps.content.urls')),
    path('schedules/', include('apps.schedules.urls')),
    path('devices/', include('apps.devices.urls')),
]
