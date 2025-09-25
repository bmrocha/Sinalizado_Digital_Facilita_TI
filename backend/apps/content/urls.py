from rest_framework.routers import DefaultRouter
from .views import ContentViewSet

app_name = 'content'

router = DefaultRouter()
router.register(r'', ContentViewSet)

urlpatterns = router.urls
