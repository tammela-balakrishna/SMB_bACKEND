from django.db.models import Q
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.permissions import IsInventoryManagerOrReadOnly

from .models import (
    VehicleBrand,
    VehicleModel,
    VehicleVariant,
    VehicleYear,
    
)

from .serializers import (
    VehicleBrandSerializer,
    VehicleModelSerializer,
    VehicleVariantSerializer,
    VehicleYearSerializer,
    
)


# ============================================================
# VEHICLE BRAND
# ============================================================

class VehicleBrandViewSet(viewsets.ModelViewSet):
    queryset = VehicleBrand.objects.all()
    serializer_class = VehicleBrandSerializer
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

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

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

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

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


