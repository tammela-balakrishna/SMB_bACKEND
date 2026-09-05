from rest_framework import serializers

from .models import OTPVerification
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()
class CustomerRegisterSerializer(serializers.Serializer):

    email = serializers.EmailField()

    first_name = serializers.CharField(
        max_length=100
    )

    last_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )

    def validate_email(self, value):
        return value.strip().lower()

class StaffCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )
    role = serializers.ChoiceField(
        choices=[
            (
                User.Role.INVENTORY_MANAGER,
                "Inventory Manager",
            ),
            (
                User.Role.SALES_MANAGER,
                "Sales Manager",
            ),
        ]
    )

    def validate_email(self, value):
        return value.strip().lower()

    def validate_role(self, value):
        if value == User.Role.SUPER_ADMIN:
            raise serializers.ValidationError(
                "Super Admin accounts cannot be created through this endpoint."
            )

        return value

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {
                    "email": "A user with this email already exists."
                }
            )

        return attrs
class StaffLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate_email(self, value):
        return value.strip().lower()
class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    purpose = serializers.ChoiceField(
        choices=OTPVerification.Purpose.choices,
        default=OTPVerification.Purpose.REGISTRATION,
    )

    def validate_email(self, value):
        return value.strip().lower()
class StaffActivateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(
        min_length=6,
        max_length=6,
        trim_whitespace=True,
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        trim_whitespace=False,
    )
    password_confirm = serializers.CharField(
        min_length=8,
        write_only=True,
        trim_whitespace=False,
    )

    def validate_email(self, value):
        return value.strip().lower()

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "OTP must contain only digits."
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {
                    "password_confirm": "Passwords do not match."
                }
            )

        return attrs
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(
        min_length=6,
        max_length=6,
        trim_whitespace=True,
    )
    purpose = serializers.ChoiceField(
        choices=OTPVerification.Purpose.choices,
        default=OTPVerification.Purpose.REGISTRATION,
    )

    def validate_email(self, value):
        return value.strip().lower()

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "OTP must contain only digits."
            )

        return value