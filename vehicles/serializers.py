from rest_framework import serializers

from .models import (

    VehicleBrand,
    VehicleModel,
    VehicleVariant,
    VehicleYear,
)


class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = [
            "id",
            "name",
            "logo",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# VEHICLE MODEL
# ============================================================

class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = [
            "id",
            "vehicle_brand",
            "name",
            "image",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# VEHICLE VARIANT
# ============================================================

class VehicleVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleVariant
        fields = [
            "id",
            "vehicle_model",
            "name",
            "engine_cc",
            "fuel_type",
            "transmission",
            "image",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# VEHICLE YEAR
# ============================================================

class VehicleYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleYear
        fields = [
            "id",
            "vehicle_variant",
            "year",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
