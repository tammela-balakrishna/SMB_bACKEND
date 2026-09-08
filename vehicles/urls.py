from rest_framework.routers import DefaultRouter

from .views import (
    VehicleBrandViewSet,
    VehicleModelViewSet,
    VehicleVariantViewSet,
    VehicleYearViewSet,
    ProductCompatibilityViewSet,
    ProductCategoryViewSet,
    ProductBrandViewSet,
    ProductViewSet,
    ProductImageViewSet,
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

# Products
router.register(
    r"product-categories",
    ProductCategoryViewSet,
    basename="product-category",
)

router.register(
    r"product-brands",
    ProductBrandViewSet,
    basename="product-brand",
)

router.register(
    r"products",
    ProductViewSet,
    basename="product",
)

router.register(
    r"product-images",
    ProductImageViewSet,
    basename="product-image",
)

router.register(
    r"compatibilities",
    ProductCompatibilityViewSet,
    basename="product-compatibility",
)


urlpatterns = router.urls