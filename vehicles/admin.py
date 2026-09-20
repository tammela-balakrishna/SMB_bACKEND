from django.contrib import admin

from .models import (
    VehicleBrand,
    VehicleModel,
    VehicleVariant,
    VehicleYear,
)


@admin.register(VehicleBrand)
class VehicleBrandAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "logo",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "vehicle_brand",
        "name",
        "image",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "vehicle_brand",
        "is_active",
    )

    search_fields = (
        "name",
        "vehicle_brand__name",
    )


@admin.register(VehicleVariant)
class VehicleVariantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "vehicle_model",
        "name",
        "engine_cc",
        "fuel_type",
        "transmission",
        "image",
        "is_active",
        "created_at",
    )

    list_filter = (
        "fuel_type",
        "transmission",
        "is_active",
    )

    search_fields = (
        "name",
        "vehicle_model__name",
        "vehicle_model__vehicle_brand__name",
    )


@admin.register(VehicleYear)
class VehicleYearAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "vehicle_variant",
        "year",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "year",
        "is_active",
    )

    search_fields = (
        "vehicle_variant__name",
        "vehicle_variant__vehicle_model__name",
        "vehicle_variant__vehicle_model__vehicle_brand__name",
    )

    ordering = (
        "-year",
    )