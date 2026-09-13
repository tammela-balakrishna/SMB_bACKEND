from rest_framework import serializers

from .models import DeviceToken, Notification


class NotificationSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(
        source="order.order_number",
        read_only=True,
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "order",
            "order_number",
            "title",
            "message",
            "notification_type",
            "is_read",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = [
            "id",
            "token",
            "platform",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_token(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "FCM token is required."
            )

        return value