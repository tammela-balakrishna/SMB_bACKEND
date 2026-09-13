from django.conf import settings
from django.db import models

from common.models import TimeStampedModel


class Notification(TimeStampedModel):
    class NotificationType(models.TextChoices):
        ORDER_PLACED = "ORDER_PLACED", "Order Placed"
        ORDER_CONFIRMED = "ORDER_CONFIRMED", "Order Confirmed"
        ORDER_PROCESSING = "ORDER_PROCESSING", "Order Processing"
        ORDER_SHIPPED = "ORDER_SHIPPED", "Order Shipped"
        ORDER_DELIVERED = "ORDER_DELIVERED", "Order Delivered"
        ORDER_CANCELLED = "ORDER_CANCELLED", "Order Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    title = models.CharField(
        max_length=200,
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
    )

    is_read = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.order.order_number}"


class DeviceToken(TimeStampedModel):
    class Platform(models.TextChoices):
        ANDROID = "ANDROID", "Android"
        IOS = "IOS", "iOS"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="device_tokens",
    )

    token = models.TextField(
        unique=True,
    )

    platform = models.CharField(
        max_length=10,
        choices=Platform.choices,
        default=Platform.ANDROID,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        db_table = "device_tokens"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.platform}"