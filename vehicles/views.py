from rest_framework import viewsets

from accounts.permissions import IsInventoryManagerOrReadOnly

from .models import (
    VehicleBrand,
    VehicleModel,
    VehicleVariant,
    VehicleYear,
    ProductCategory,
    ProductBrand,
    Product,
    ProductImage,
    ProductCompatibility,
)

from .serializers import (
    VehicleBrandSerializer,
    VehicleModelSerializer,
    VehicleVariantSerializer,
    VehicleYearSerializer,
    ProductCategorySerializer,
    ProductBrandSerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductCompatibilitySerializer,
)


# ============================================================
# VEHICLE BRAND
# ============================================================

class VehicleBrandViewSet(viewsets.ModelViewSet):
    queryset = VehicleBrand.objects.all()
    serializer_class = VehicleBrandSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        is_active = self.request.query_params.get("is_active")

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        return queryset


# ============================================================
# VEHICLE MODEL
# ============================================================

class VehicleModelViewSet(viewsets.ModelViewSet):
    queryset = VehicleModel.objects.select_related(
        "vehicle_brand",
    ).all()
    serializer_class = VehicleModelSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        brand_id = self.request.query_params.get(
            "vehicle_brand"
        )

        is_active = self.request.query_params.get(
            "is_active"
        )

        if brand_id:
            queryset = queryset.filter(
                vehicle_brand_id=brand_id
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        return queryset


# ============================================================
# VEHICLE VARIANT
# ============================================================

class VehicleVariantViewSet(viewsets.ModelViewSet):
    queryset = VehicleVariant.objects.select_related(
        "vehicle_model",
        "vehicle_model__vehicle_brand",
    ).all()
    serializer_class = VehicleVariantSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        model_id = self.request.query_params.get(
            "vehicle_model"
        )

        is_active = self.request.query_params.get(
            "is_active"
        )

        if model_id:
            queryset = queryset.filter(
                vehicle_model_id=model_id
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        return queryset


# ============================================================
# VEHICLE YEAR
# ============================================================

class VehicleYearViewSet(viewsets.ModelViewSet):
    queryset = VehicleYear.objects.select_related(
        "vehicle_variant",
        "vehicle_variant__vehicle_model",
        "vehicle_variant__vehicle_model__vehicle_brand",
    ).all()
    serializer_class = VehicleYearSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        variant_id = self.request.query_params.get(
            "vehicle_variant"
        )

        is_active = self.request.query_params.get(
            "is_active"
        )

        if variant_id:
            queryset = queryset.filter(
                vehicle_variant_id=variant_id
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        return queryset


# ============================================================
# PRODUCT CATEGORY
# ============================================================

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

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

        category_id = self.request.query_params.get(
            "product_category"
        )

        brand_id = self.request.query_params.get(
            "product_brand"
        )

        is_active = self.request.query_params.get(
            "is_active"
        )

        if category_id:
            queryset = queryset.filter(
                product_category_id=category_id
            )

        if brand_id:
            queryset = queryset.filter(
                product_brand_id=brand_id
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == "true"
            )

        return queryset.order_by("name")


# ============================================================
# PRODUCT IMAGE
# ============================================================

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.select_related(
        "product",
    ).all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

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

        vehicle_year_id = self.request.query_params.get(
            "vehicle_year"
        )

        if product_id:
            queryset = queryset.filter(
                product_id=product_id
            )

        if vehicle_year_id:
            queryset = queryset.filter(
                vehicle_year_id=vehicle_year_id
            )

        return queryset