from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet

app_name = 'devices'

router = DefaultRouter()
router.register(r'', DeviceViewSet)

urlpatterns = router.urls
