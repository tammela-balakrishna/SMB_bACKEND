from rest_framework import serializers

from .models import CustomerAddress


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = [
            "id",
            "address_type",
            "full_name",
            "mobile_number",
            "delivery_address",
            "area",
            "city",
            "state",
            "pincode",
            "is_default",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_full_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Full name is required."
            )

        return value

    def validate_mobile_number(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Mobile number is required."
            )

        if not value.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain only digits."
            )

        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError(
                "Mobile number must contain 10 to 15 digits."
            )

        return value

    def validate_delivery_address(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Delivery address is required."
            )

        return value

    def validate_area(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Area is required."
            )

        return value

    def validate_city(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "City is required."
            )

        return value

    def validate_state(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "State is required."
            )

        return value

    def validate_pincode(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Pincode is required."
            )

        if not value.isdigit():
            raise serializers.ValidationError(
                "Pincode must contain only digits."
            )

        if len(value) < 4 or len(value) > 10:
            raise serializers.ValidationError(
                "Pincode must contain 4 to 10 digits."
            )

        return value