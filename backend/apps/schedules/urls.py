from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet

app_name = 'schedules'

router = DefaultRouter()
router.register(r'', ScheduleViewSet)

urlpatterns = router.urls
