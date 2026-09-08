from rest_framework import serializers

from .models import (
    ProductCategory,
    VehicleBrand,
    VehicleModel,
    VehicleVariant,
    VehicleYear,
    ProductCompatibility,
    ProductCategory,
    ProductBrand,
    Product,
    ProductImage,
    ProductCompatibility,
);


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = [
            "id",
            "name",
            "description",
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


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = [
            "id",
            "name",
            "logo",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "product_category",
            "product_brand",
            "name",
            "sku",
            "description",
            "mrp",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "product",
            "image",
            "public_id",
            "is_primary",
            "sort_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ProductCompatibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCompatibility
        fields = [
            "id",
            "product",
            "vehicle_year",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

# ============================================================
# VEHICLE BRAND
# ============================================================

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


# ============================================================
# PRODUCT COMPATIBILITY
# ============================================================

class ProductCompatibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCompatibility

        fields = [
            "id",
            "product",
            "vehicle_year",
            "notes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]