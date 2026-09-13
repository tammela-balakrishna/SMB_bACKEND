from rest_framework.routers import DefaultRouter

from .views import (
    DeviceTokenViewSet,
    NotificationViewSet,
)


router = DefaultRouter()

router.register(
    "",
    NotificationViewSet,
    basename="notifications",
)

router.register(
    "devices",
    DeviceTokenViewSet,
    basename="device-tokens",
)

urlpatterns = router.urls