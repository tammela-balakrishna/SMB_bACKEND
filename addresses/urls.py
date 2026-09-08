from rest_framework.routers import DefaultRouter

from .views import CustomerAddressViewSet


router = DefaultRouter()

router.register(
    r"",
    CustomerAddressViewSet,
    basename="customer-address",
)

urlpatterns = router.urls