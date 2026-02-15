from rest_framework.routers import DefaultRouter

from notification.apis.views import NotificationViewSet

router = DefaultRouter()
router.register(r"", NotificationViewSet, basename="notifications")

urlpatterns = []
urlpatterns += router.urls
