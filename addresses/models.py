from django.conf import settings
from django.db import models


class CustomerAddress(models.Model):
    class AddressType(models.TextChoices):
        HOME = "HOME", "Home"
        WORK = "WORK", "Work"
        OTHER = "OTHER", "Other"

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    address_type = models.CharField(
        max_length=10,
        choices=AddressType.choices,
        default=AddressType.HOME,
    )

    full_name = models.CharField(
        max_length=150,
    )

    mobile_number = models.CharField(
        max_length=15,
    )

    delivery_address = models.TextField()

    area = models.CharField(
        max_length=150,
    )

    city = models.CharField(
        max_length=100,
    )

    state = models.CharField(
        max_length=100,
    )

    pincode = models.CharField(
        max_length=10,
    )

    is_default = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-is_default", "-created_at"]
        indexes = [
            models.Index(
                fields=["customer", "is_default"],
            ),
        ]

    def __str__(self):
        return (
            f"{self.full_name} - "
            f"{self.city} - "
            f"{self.pincode}"
        )