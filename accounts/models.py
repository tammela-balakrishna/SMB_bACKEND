from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    class AccountType(models.TextChoices):
        STAFF = "STAFF", "Staff"
        CUSTOMER = "CUSTOMER", "Customer"

    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        INVENTORY_MANAGER = "INVENTORY_MANAGER", "Inventory Manager"
        SALES_MANAGER = "SALES_MANAGER", "Sales Manager"

    email = models.EmailField(
        unique=True,
        db_index=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
    )

    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.CUSTOMER,
    )

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        return self.email  

class OTPVerification(models.Model):

    class Purpose(models.TextChoices):
        REGISTRATION = "REGISTRATION", "Registration"
        LOGIN = "LOGIN", "Login"
        PASSWORD_RESET = "PASSWORD_RESET", "Password Reset"
        EMAIL_VERIFY = "EMAIL_VERIFY", "Email Verification"

    email = models.EmailField(
        db_index=True,
    )

    otp_hash = models.CharField(
        max_length=128,
    )

    purpose = models.CharField(
        max_length=30,
        choices=Purpose.choices,
    )

    expires_at = models.DateTimeField()

    attempts = models.PositiveSmallIntegerField(
        default=0,
    )

    is_used = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["email", "purpose", "created_at"],
            ),
        ]

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"{self.email} - {self.purpose}"