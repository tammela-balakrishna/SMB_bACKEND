from rest_framework.routers import DefaultRouter

from .views import (
    ProductCategoryViewSet,
    ProductBrandViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ProductCompatibilityViewSet,
    CategoryDiscountViewSet,
)


router = DefaultRouter()


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

router.register(
    r"category-discounts",
    CategoryDiscountViewSet,
    basename="category-discount",
)


urlpatterns = router.urls