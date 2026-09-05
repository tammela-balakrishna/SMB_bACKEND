from django.contrib import admin

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
    CategoryDiscount,
    CategoryDiscountProduct,

)


@admin.register(VehicleBrand)
class VehicleBrandAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = ("is_active",)

    search_fields = ("name",)


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "vehicle_brand",
        "name",
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
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
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

    ordering = (
        "name",
    )
@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
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

    ordering = (
        "name",
    )
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "sku",
        "product_category",
        "product_brand",
        "mrp",
        "is_active",
        "created_at",
    )

    list_filter = (
        "product_category",
        "product_brand",
        "is_active",
    )

    search_fields = (
        "name",
        "sku",
        "product_category__name",
        "product_brand__name",
    )
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "is_primary",
        "sort_order",
        "created_at",
    )

    list_filter = (
        "is_primary",
    )

    search_fields = (
        "product__name",
        "product__sku",
    )

    ordering = (
        "product",
        "sort_order",
    )
@admin.register(ProductCompatibility)
class ProductCompatibilityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "vehicle_year",
        "created_at",
    )

    list_filter = (
        "vehicle_year__vehicle_variant__vehicle_model__vehicle_brand",
    )

    search_fields = (
        "product__name",
        "product__sku",
        "vehicle_year__vehicle_variant__name",
        "vehicle_year__vehicle_variant__vehicle_model__name",
        "vehicle_year__vehicle_variant__vehicle_model__vehicle_brand__name",
    )
@admin.register(CategoryDiscount)
class CategoryDiscountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_category",
        "application_scope",
        "discount_type",
        "discount_value",
        "min_order_amount",
        "start_at",
        "end_at",
        "priority",
        "is_active",
    )

    list_filter = (
        "application_scope",
        "discount_type",
        "is_active",
        "product_category",
    )

    search_fields = (
        "product_category__name",
    )

    ordering = (
        "priority",
        "-created_at",
    )
@admin.register(CategoryDiscountProduct)
class CategoryDiscountProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category_discount",
        "product",
        "created_at",
    )

    list_filter = (
        "category_discount__product_category",
        "category_discount__application_scope",
        "category_discount__discount_type",
    )

    search_fields = (
        "product__name",
        "product__sku",
        "category_discount__product_category__name",
    )