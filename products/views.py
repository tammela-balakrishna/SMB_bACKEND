from django.db.models import Q
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from accounts.permissions import IsInventoryManagerOrReadOnly
from vehicles.models import (
    VehicleBrand,
    VehicleModel,
    VehicleVariant,
    VehicleYear,
)

from vehicles.serializers import (
    VehicleBrandSerializer,
    VehicleModelSerializer,
    VehicleVariantSerializer,
    VehicleYearSerializer,
)

from .models import (
    Product,
    ProductCategory,
    ProductBrand,
    ProductImage,
    ProductCompatibility,
    CategoryDiscount,
    CategoryDiscountProduct,
)

from .serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    ProductBrandSerializer,
    ProductImageSerializer,
    ProductCompatibilitySerializer,
    CategoryDiscountSerializer,
    CategoryDiscountProductSerializer,
)

# ============================================================
# PRODUCT CATEGORY
# ============================================================

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        is_active = self.request.query_params.get("is_active")

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        return queryset.order_by("name")


# ============================================================
# PRODUCT BRAND
# ============================================================

class ProductBrandViewSet(viewsets.ModelViewSet):
    queryset = ProductBrand.objects.all()
    serializer_class = ProductBrandSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

    parser_classes = [
        MultiPartParser,
        FormParser,
        JSONParser,
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        is_active = self.request.query_params.get("is_active")

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        return queryset.order_by("name")

# ============================================================
# PRODUCT
# ============================================================

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related(
        "product_category",
        "product_brand",
    ).all()
    serializer_class = ProductSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        category_id = self.request.query_params.get("product_category")
        brand_id = self.request.query_params.get("product_brand")
        is_active = self.request.query_params.get("is_active")
        is_featured = self.request.query_params.get("is_featured")

        if category_id:
            queryset = queryset.filter(product_category_id=category_id)

        if brand_id:
            queryset = queryset.filter(product_brand_id=brand_id)

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        if is_featured is not None:
            queryset = queryset.filter(
                is_featured=is_featured.lower() == "true"
            )

        return queryset
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.select_related(
        "product",
    ).all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        product_id = self.request.query_params.get(
            "product"
        )

        if product_id:
            queryset = queryset.filter(
                product_id=product_id
            )

        return queryset.order_by(
            "sort_order",
            "id",
        )


# ============================================================
# PRODUCT COMPATIBILITY
# ============================================================

class ProductCompatibilityViewSet(viewsets.ModelViewSet):
    queryset = ProductCompatibility.objects.select_related(
        "product",
        "vehicle_brand",
        "vehicle_model",
        "vehicle_variant",
        "vehicle_year",
        "vehicle_year__vehicle_variant",
        "vehicle_year__vehicle_variant__vehicle_model",
        "vehicle_year__vehicle_variant__vehicle_model__vehicle_brand",
    ).all()

    serializer_class = ProductCompatibilitySerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        product_id = self.request.query_params.get(
            "product"
        )

        vehicle_brand_id = self.request.query_params.get(
            "vehicle_brand"
        )

        vehicle_model_id = self.request.query_params.get(
            "vehicle_model"
        )

        vehicle_variant_id = self.request.query_params.get(
            "vehicle_variant"
        )

        vehicle_year_id = self.request.query_params.get(
            "vehicle_year"
        )

        # --------------------------------------------------------
        # PRODUCT FILTER
        # --------------------------------------------------------

        if product_id:
            queryset = queryset.filter(
                product_id=product_id
            )

        # --------------------------------------------------------
        # HIERARCHICAL VEHICLE COMPATIBILITY FILTER
        #
        # Selected:
        # Brand -> Model -> Variant -> Year
        #
        # Matches:
        # 1. Brand only
        # 2. Brand + Model
        # 3. Brand + Model + Variant
        # 4. Exact Year compatibility
        # --------------------------------------------------------

        if vehicle_brand_id:
            compatibility_filter = Q(
                vehicle_brand_id=vehicle_brand_id,
                vehicle_model__isnull=True,
                vehicle_variant__isnull=True,
                vehicle_year__isnull=True,
            )

            if vehicle_model_id:
                compatibility_filter |= Q(
                    vehicle_brand_id=vehicle_brand_id,
                    vehicle_model_id=vehicle_model_id,
                    vehicle_variant__isnull=True,
                    vehicle_year__isnull=True,
                )

            if vehicle_model_id and vehicle_variant_id:
                compatibility_filter |= Q(
                    vehicle_brand_id=vehicle_brand_id,
                    vehicle_model_id=vehicle_model_id,
                    vehicle_variant_id=vehicle_variant_id,
                    vehicle_year__isnull=True,
                )

            if vehicle_year_id:
                compatibility_filter |= Q(
                    vehicle_year_id=vehicle_year_id
                )

            queryset = queryset.filter(
                compatibility_filter
            )

        return queryset
# ============================================================
# CATEGORY DISCOUNT
# ============================================================

# ============================================================
# CATEGORY DISCOUNT
# ============================================================

class CategoryDiscountViewSet(viewsets.ModelViewSet):
    queryset = CategoryDiscount.objects.select_related(
        "product_category",
    ).prefetch_related(
        "product_mappings__product",
    ).all()

    serializer_class = CategoryDiscountSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        category_id = self.request.query_params.get(
            "product_category"
        )

        is_active = self.request.query_params.get(
            "is_active"
        )

        application_scope = self.request.query_params.get(
            "application_scope"
        )

        if category_id:
            queryset = queryset.filter(
                product_category_id=category_id
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        if application_scope:
            queryset = queryset.filter(
                application_scope=application_scope
            )

        return queryset.order_by(
            "priority",
            "-created_at",
        )