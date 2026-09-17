from rest_framework import serializers

from .models import (
    ProductCategory,
    ProductBrand,
    Product,
    ProductImage,
    ProductCompatibility,
    CategoryDiscountProduct,
    CategoryDiscount,
    VehicleBrand,
    VehicleModel,
    VehicleVariant,
    VehicleYear,
)


# ============================================================
# PRODUCT CATEGORY
# ============================================================

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


# ============================================================
# PRODUCT BRAND
# ============================================================

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


# ============================================================
# PRODUCT
# ============================================================

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
            "is_featured",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# PRODUCT IMAGE
# ============================================================

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
            "public_id",
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
            "vehicle_brand",
            "vehicle_model",
            "vehicle_variant",
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
# CATEGORY DISCOUNT
# ============================================================
# ============================================================
# CATEGORY DISCOUNT
# ============================================================

class CategoryDiscountSerializer(serializers.ModelSerializer):
    product_ids = serializers.PrimaryKeyRelatedField(
        source="product_mappings",
        many=True,
        queryset=Product.objects.all(),
        required=False,
        write_only=True,
    )

    products = serializers.SerializerMethodField(
        read_only=True,
    )

    product_category_name = serializers.CharField(
        source="product_category.name",
        read_only=True,
    )

    class Meta:
        model = CategoryDiscount
        fields = [
            "id",
            "product_category",
            "product_category_name",
            "application_scope",
            "discount_type",
            "discount_value",
            "max_discount_amount",
            "min_order_amount",
            "start_at",
            "end_at",
            "priority",
            "is_active",
            "product_ids",
            "products",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "product_category_name",
            "products",
            "created_at",
            "updated_at",
        ]

    def get_products(self, obj):
        return [
            {
                "id": mapping.product.id,
                "name": mapping.product.name,
                "sku": mapping.product.sku,
                "product_category": mapping.product.product_category_id,
            }
            for mapping in obj.product_mappings.select_related(
                "product",
                "product__product_category",
            ).all()
        ]

    def validate(self, attrs):
        application_scope = attrs.get(
            "application_scope",
            getattr(
                self.instance,
                "application_scope",
                None,
            ),
        )

        discount_type = attrs.get(
            "discount_type",
            getattr(
                self.instance,
                "discount_type",
                None,
            ),
        )

        discount_value = attrs.get(
            "discount_value",
            getattr(
                self.instance,
                "discount_value",
                None,
            ),
        )

        max_discount_amount = attrs.get(
            "max_discount_amount",
            getattr(
                self.instance,
                "max_discount_amount",
                None,
            ),
        )

        min_order_amount = attrs.get(
            "min_order_amount",
            getattr(
                self.instance,
                "min_order_amount",
                None,
            ),
        )

        start_at = attrs.get(
            "start_at",
            getattr(
                self.instance,
                "start_at",
                None,
            ),
        )

        end_at = attrs.get(
            "end_at",
            getattr(
                self.instance,
                "end_at",
                None,
            ),
        )

        product_category = attrs.get(
            "product_category",
            getattr(
                self.instance,
                "product_category",
                None,
            ),
        )

        product_ids = attrs.get(
            "product_mappings",
            None,
        )

        errors = {}

        # --------------------------------------------------------
        # Discount value
        # --------------------------------------------------------

        if discount_value is not None and discount_value <= 0:
            errors["discount_value"] = (
                "Discount value must be greater than 0."
            )

        # --------------------------------------------------------
        # Percentage validation
        # --------------------------------------------------------

        if (
            discount_type
            == CategoryDiscount.DiscountType.PERCENTAGE
            and discount_value is not None
            and discount_value > 100
        ):
            errors["discount_value"] = (
                "Percentage discount cannot exceed 100%."
            )

        # --------------------------------------------------------
        # Maximum discount
        # --------------------------------------------------------

        if (
            max_discount_amount is not None
            and max_discount_amount < 0
        ):
            errors["max_discount_amount"] = (
                "Maximum discount amount cannot be negative."
            )

        if (
            discount_type
            == CategoryDiscount.DiscountType.FIXED_AMOUNT
            and max_discount_amount is not None
        ):
            errors["max_discount_amount"] = (
                "Maximum discount amount should only be used "
                "with percentage discounts."
            )

        # --------------------------------------------------------
        # Minimum order amount
        # --------------------------------------------------------

        if (
            min_order_amount is not None
            and min_order_amount < 0
        ):
            errors["min_order_amount"] = (
                "Minimum order amount cannot be negative."
            )

        # --------------------------------------------------------
        # Date validation
        # --------------------------------------------------------

        if start_at and end_at and start_at >= end_at:
            errors["end_at"] = (
                "End date/time must be after start date/time."
            )

        # --------------------------------------------------------
        # Product mapping validation
        # --------------------------------------------------------

        if (
            application_scope
            in [
                CategoryDiscount.ApplicationScope.SELECTED_PRODUCTS,
                CategoryDiscount.ApplicationScope.EXCLUDE_PRODUCTS,
            ]
        ):
            if self.instance is None and product_ids is None:
                errors["product_ids"] = (
                    "Product IDs are required for "
                    "selected/excluded product discounts."
                )

        # --------------------------------------------------------
        # ALL_PRODUCTS should not receive mappings
        # --------------------------------------------------------

        if (
            application_scope
            == CategoryDiscount.ApplicationScope.ALL_PRODUCTS
            and product_ids
        ):
            errors["product_ids"] = (
                "Product IDs cannot be provided when the "
                "discount applies to all products."
            )

        # --------------------------------------------------------
        # Product category validation
        # --------------------------------------------------------

        if (
            product_category is not None
            and product_ids
        ):
            invalid_products = [
                product.id
                for product in product_ids
                if product.product_category_id
                != product_category.id
            ]

            if invalid_products:
                errors["product_ids"] = (
                    "All selected products must belong to "
                    "the selected product category."
                )

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        products = validated_data.pop(
            "product_mappings",
            [],
        )

        discount = CategoryDiscount.objects.create(
            **validated_data
        )

        self._sync_product_mappings(
            discount,
            products,
        )

        return discount

    def update(self, instance, validated_data):
        products = validated_data.pop(
            "product_mappings",
            None,
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.full_clean()
        instance.save()

        if products is not None:
            self._sync_product_mappings(
                instance,
                products,
            )

        return instance

    def _sync_product_mappings(
        self,
        discount,
        products,
    ):
        discount.product_mappings.all().delete()

        if (
            discount.application_scope
            == CategoryDiscount.ApplicationScope.ALL_PRODUCTS
        ):
            return

        CategoryDiscountProduct.objects.bulk_create(
            [
                CategoryDiscountProduct(
                    category_discount=discount,
                    product=product,
                )
                for product in products
            ]
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
