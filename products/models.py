from django.core.exceptions import ValidationError
from django.db import models

from common.models import TimeStampedModel
from vehicles.models import (
    VehicleBrand,
    VehicleModel,
    VehicleVariant,
    VehicleYear,
)
# Create your models here.
# ============================================================
# PRODUCT CATEGORY
# ============================================================

class ProductCategory(TimeStampedModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
        default="",
    )

    image = models.ImageField(
        upload_to="products/categories/",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "product_categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# PRODUCT BRAND
# ============================================================

class ProductBrand(TimeStampedModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    logo = models.ImageField(
        upload_to="products/brands/",
        null=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
        default="",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "product_brands"
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# PRODUCT
# ============================================================

class Product(TimeStampedModel):
    product_category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="products",
    )

    product_brand = models.ForeignKey(
        ProductBrand,
        on_delete=models.PROTECT,
        related_name="products",
    )

    name = models.CharField(
        max_length=200,
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
        default="",
    )

    mrp = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "products"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.sku})"


# ============================================================
# PRODUCT IMAGE
# ============================================================

class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="products/images/",
    )

    public_id = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    is_primary = models.BooleanField(
        default=False,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        db_table = "product_images"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"


# ============================================================
# PRODUCT COMPATIBILITY
# ============================================================

class ProductCompatibility(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="compatibilities",
    )

    vehicle_brand = models.ForeignKey(
        VehicleBrand,
        on_delete=models.CASCADE,
        related_name="product_compatibilities",
        null=True,
        blank=True,
    )

    vehicle_model = models.ForeignKey(
        VehicleModel,
        on_delete=models.CASCADE,
        related_name="product_compatibilities",
        null=True,
        blank=True,
    )

    vehicle_variant = models.ForeignKey(
        VehicleVariant,
        on_delete=models.CASCADE,
        related_name="product_compatibilities",
        null=True,
        blank=True,
    )

    vehicle_year = models.ForeignKey(
        VehicleYear,
        on_delete=models.CASCADE,
        related_name="product_compatibilities",
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
        default="",
    )

    class Meta:
        db_table = "product_compatibilities"
        ordering = [
            "vehicle_brand",
            "vehicle_model",
            "vehicle_variant",
            "vehicle_year",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["product", "vehicle_brand"],
                condition=models.Q(
                    vehicle_model__isnull=True,
                    vehicle_variant__isnull=True,
                    vehicle_year__isnull=True,
                ),
                name="unique_product_vehicle_brand",
            ),
            models.UniqueConstraint(
                fields=["product", "vehicle_model"],
                condition=models.Q(
                    vehicle_variant__isnull=True,
                    vehicle_year__isnull=True,
                ),
                name="unique_product_vehicle_model",
            ),
            models.UniqueConstraint(
                fields=["product", "vehicle_variant"],
                condition=models.Q(
                    vehicle_year__isnull=True,
                ),
                name="unique_product_vehicle_variant",
            ),
            models.UniqueConstraint(
                fields=["product", "vehicle_year"],
                condition=models.Q(
                    vehicle_year__isnull=False,
                ),
                name="unique_product_vehicle_year",
            ),
        ]

    def clean(self):
        super().clean()

        if not any([
            self.vehicle_brand_id,
            self.vehicle_model_id,
            self.vehicle_variant_id,
            self.vehicle_year_id,
        ]):
            raise ValidationError(
                "At least one vehicle compatibility level is required."
            )

        if self.vehicle_year_id:
            year = self.vehicle_year

            expected_variant_id = year.vehicle_variant_id
            expected_model_id = (
                year.vehicle_variant.vehicle_model_id
            )
            expected_brand_id = (
                year.vehicle_variant.vehicle_model.vehicle_brand_id
            )

            if (
                self.vehicle_variant_id
                and self.vehicle_variant_id != expected_variant_id
            ):
                raise ValidationError(
                    "Selected variant does not belong to the selected year."
                )

            if (
                self.vehicle_model_id
                and self.vehicle_model_id != expected_model_id
            ):
                raise ValidationError(
                    "Selected model does not belong to the selected year."
                )

            if (
                self.vehicle_brand_id
                and self.vehicle_brand_id != expected_brand_id
            ):
                raise ValidationError(
                    "Selected brand does not belong to the selected year."
                )

        if self.vehicle_variant_id:
            variant = self.vehicle_variant

            expected_model_id = variant.vehicle_model_id
            expected_brand_id = (
                variant.vehicle_model.vehicle_brand_id
            )

            if (
                self.vehicle_model_id
                and self.vehicle_model_id != expected_model_id
            ):
                raise ValidationError(
                    "Selected model does not belong to the selected variant."
                )

            if (
                self.vehicle_brand_id
                and self.vehicle_brand_id != expected_brand_id
            ):
                raise ValidationError(
                    "Selected brand does not belong to the selected variant."
                )

        if self.vehicle_model_id:
            expected_brand_id = (
                self.vehicle_model.vehicle_brand_id
            )

            if (
                self.vehicle_brand_id
                and self.vehicle_brand_id != expected_brand_id
            ):
                raise ValidationError(
                    "Selected brand does not belong to the selected model."
                )

    def save(self, *args, **kwargs):
        if self.vehicle_year_id:
            year = self.vehicle_year

            self.vehicle_variant_id = year.vehicle_variant_id
            self.vehicle_model_id = (
                year.vehicle_variant.vehicle_model_id
            )
            self.vehicle_brand_id = (
                year.vehicle_variant.vehicle_model.vehicle_brand_id
            )

        elif self.vehicle_variant_id:
            variant = self.vehicle_variant

            self.vehicle_model_id = variant.vehicle_model_id
            self.vehicle_brand_id = (
                variant.vehicle_model.vehicle_brand_id
            )

        elif self.vehicle_model_id:
            self.vehicle_brand_id = (
                self.vehicle_model.vehicle_brand_id
            )

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        target = []

        if self.vehicle_brand:
            target.append(self.vehicle_brand.name)

        if self.vehicle_model:
            target.append(self.vehicle_model.name)

        if self.vehicle_variant:
            target.append(self.vehicle_variant.name)

        if self.vehicle_year:
            target.append(str(self.vehicle_year.year))

        compatibility = " ? ".join(target)

        return f"{self.product} ? {compatibility}"


# ============================================================
# CATEGORY DISCOUNT
# ============================================================

class CategoryDiscount(TimeStampedModel):

    class ApplicationScope(models.TextChoices):
        ALL_PRODUCTS = "ALL_PRODUCTS", "All Products"
        SELECTED_PRODUCTS = "SELECTED_PRODUCTS", "Selected Products"
        EXCLUDE_PRODUCTS = "EXCLUDE_PRODUCTS", "Exclude Products"

    class DiscountType(models.TextChoices):
        PERCENTAGE = "PERCENTAGE", "Percentage"
        FIXED_AMOUNT = "FIXED_AMOUNT", "Fixed Amount"

    product_category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="discounts",
    )

    application_scope = models.CharField(
        max_length=30,
        choices=ApplicationScope.choices,
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    start_at = models.DateTimeField()

    end_at = models.DateTimeField()

    priority = models.PositiveIntegerField(
        default=1,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "category_discounts"
        ordering = ["priority", "-created_at"]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    discount_value__gt=0
                ),
                name="discount_value_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    min_order_amount__gte=0
                ),
                name="min_order_amount_non_negative",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(max_discount_amount__isnull=True)
                    | models.Q(max_discount_amount__gte=0)
                ),
                name="max_discount_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    start_at__lt=models.F("end_at")
                ),
                name="discount_start_before_end",
            ),
        ]

    def clean(self):
        super().clean()

        errors = {}

        # --------------------------------------------------------
        # Discount value
        # --------------------------------------------------------

        if self.discount_value is not None:
            if self.discount_value <= 0:
                errors["discount_value"] = (
                    "Discount value must be greater than 0."
                )

        # --------------------------------------------------------
        # Percentage validation
        # --------------------------------------------------------

        if (
            self.discount_type == self.DiscountType.PERCENTAGE
            and self.discount_value is not None
            and self.discount_value > 100
        ):
            errors["discount_value"] = (
                "Percentage discount cannot exceed 100%."
            )

        # --------------------------------------------------------
        # Maximum discount validation
        # --------------------------------------------------------

        if (
            self.max_discount_amount is not None
            and self.max_discount_amount < 0
        ):
            errors["max_discount_amount"] = (
                "Maximum discount amount cannot be negative."
            )

        # Maximum discount only applies to percentage discounts.
        if (
            self.discount_type == self.DiscountType.FIXED_AMOUNT
            and self.max_discount_amount is not None
        ):
            errors["max_discount_amount"] = (
                "Maximum discount amount should only be used "
                "with percentage discounts."
            )

        # --------------------------------------------------------
        # Minimum order amount
        # --------------------------------------------------------

        if (
            self.min_order_amount is not None
            and self.min_order_amount < 0
        ):
            errors["min_order_amount"] = (
                "Minimum order amount cannot be negative."
            )

        # --------------------------------------------------------
        # Date validation
        # --------------------------------------------------------

        if self.start_at and self.end_at:
            if self.start_at >= self.end_at:
                errors["end_at"] = (
                    "End date/time must be after start date/time."
                )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return (
            f"{self.product_category.name} - "
            f"{self.discount_value} "
            f"{self.discount_type}"
        )


# ============================================================
# CATEGORY DISCOUNT PRODUCT MAPPING
# ============================================================

class CategoryDiscountProduct(TimeStampedModel):


    category_discount = models.ForeignKey(
        CategoryDiscount,
        on_delete=models.CASCADE,
        related_name="product_mappings",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="discount_mappings",
    )

    class Meta:
        db_table = "category_discount_products"
        ordering = ["id"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "category_discount",
                    "product",
                ],
                name="unique_category_discount_product",
            ),
        ]

    def clean(self):
        super().clean()

        errors = {}

        # --------------------------------------------------------
        # Ensure mapped product belongs to discount category
        # --------------------------------------------------------

        if (
            self.category_discount_id
            and self.product_id
        ):
            if (
                self.category_discount.product_category_id
                != self.product.product_category_id
            ):
                errors["product"] = (
                    "Selected product must belong to the "
                    "same category as the discount."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.category_discount} → "
            f"{self.product.name}"
        )