from rest_framework.routers import DefaultRouter

from .views import (
    VehicleBrandViewSet,
    VehicleModelViewSet,
    VehicleVariantViewSet,
    VehicleYearViewSet,

)


router = DefaultRouter()

# Vehicles
router.register(
    r"brands",
    VehicleBrandViewSet,
    basename="vehicle-brand",
)

router.register(
    r"models",
    VehicleModelViewSet,
    basename="vehicle-model",
)

router.register(
    r"variants",
    VehicleVariantViewSet,
    basename="vehicle-variant",
)

router.register(
    r"years",
    VehicleYearViewSet,
    basename="vehicle-year",
)



urlpatterns = router.urls