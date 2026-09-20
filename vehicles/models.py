from django.core.exceptions import ValidationError
from django.db import models

from common.models import TimeStampedModel


# ============================================================
# VEHICLE BRAND
# ============================================================

class VehicleBrand(TimeStampedModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    logo = models.ImageField(
        upload_to="vehicles/brands/",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "vehicle_brands"
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# VEHICLE MODEL
# ============================================================

class VehicleModel(TimeStampedModel):
    vehicle_brand = models.ForeignKey(
        VehicleBrand,
        on_delete=models.PROTECT,
        related_name="models",
    )

    name = models.CharField(
        max_length=100,
    )

    image = models.ImageField(
        upload_to="vehicles/models/",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "vehicle_models"
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["vehicle_brand", "name"],
                name="unique_vehicle_model_per_brand",
            ),
        ]

    def __str__(self):
        return f"{self.vehicle_brand.name} {self.name}"


# ============================================================
# VEHICLE VARIANT
# ============================================================

class VehicleVariant(TimeStampedModel):

    class FuelType(models.TextChoices):
        PETROL = "PETROL", "Petrol"
        ELECTRIC = "ELECTRIC", "Electric"
        CNG = "CNG", "CNG"

    class TransmissionType(models.TextChoices):
        MANUAL = "MANUAL", "Manual"
        AUTOMATIC = "AUTOMATIC", "Automatic"

    vehicle_model = models.ForeignKey(
        VehicleModel,
        on_delete=models.PROTECT,
        related_name="variants",
    )

    name = models.CharField(
        max_length=100,
    )

    engine_cc = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    fuel_type = models.CharField(
        max_length=20,
        choices=FuelType.choices,
        default=FuelType.PETROL,
    )

    transmission = models.CharField(
        max_length=20,
        choices=TransmissionType.choices,
        default=TransmissionType.MANUAL,
    )

    image = models.ImageField(
        upload_to="vehicles/variants/",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "vehicle_variants"
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["vehicle_model", "name"],
                name="unique_vehicle_variant_per_model",
            ),
        ]

    def __str__(self):
        return f"{self.vehicle_model} - {self.name}"


# ============================================================
# VEHICLE YEAR
# ============================================================

class VehicleYear(TimeStampedModel):
    vehicle_variant = models.ForeignKey(
        VehicleVariant,
        on_delete=models.PROTECT,
        related_name="years",
    )

    year = models.PositiveIntegerField()

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "vehicle_years"
        ordering = ["year"]

        constraints = [
            models.UniqueConstraint(
                fields=["vehicle_variant", "year"],
                name="unique_vehicle_year_per_variant",
            ),
        ]

    def __str__(self):
        return f"{self.vehicle_variant} - {self.year}"





