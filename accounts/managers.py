from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address is required.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise ValueError("Super Admin must have a password.")

        extra_fields.setdefault(
            "role",
            "SUPER_ADMIN",
        )
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Super Admin must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Super Admin must have is_superuser=True.")

        return self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )
def create_superuser(self, email, password=None, **extra_fields):

    if not password:
        raise ValueError(
            "Super Admin must have a password."
        )

    extra_fields.setdefault(
        "account_type",
        "STAFF",
    )

    extra_fields.setdefault(
        "role",
        "SUPER_ADMIN",
    )

    extra_fields.setdefault(
        "is_staff",
        True,
    )

    extra_fields.setdefault(
        "is_superuser",
        True,
    )

    extra_fields.setdefault(
        "is_active",
        True,
    )

    extra_fields.setdefault(
        "is_verified",
        True,
    )

    return self.create_user(
        email=email,
        password=password,
        **extra_fields,
    )