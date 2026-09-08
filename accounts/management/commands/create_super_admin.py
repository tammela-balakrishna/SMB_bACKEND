from getpass import getpass

from django.core.management.base import BaseCommand, CommandError

from accounts.models import User


class Command(BaseCommand):
    help = "Create a custom SMB Super Admin user."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "\n=== SMB Super Admin Creation ===\n"
            )
        )

        email = input("Email address: ").strip().lower()

        if not email:
            raise CommandError("Email address is required.")

        if User.objects.filter(email=email).exists():
            raise CommandError(
                f"A user with email '{email}' already exists."
            )

        first_name = input("First name: ").strip()

        if not first_name:
            raise CommandError("First name is required.")

        last_name = input("Last name (optional): ").strip()

        password = getpass("Password: ")
        password_confirm = getpass("Password (again): ")

        if not password:
            raise CommandError("Password is required.")

        if password != password_confirm:
            raise CommandError("Passwords do not match.")

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            account_type=User.AccountType.STAFF,
            role=User.Role.SUPER_ADMIN,
            is_active=True,
            is_staff=True,
            is_verified=True,
            is_superuser=True,
        )

        user.set_password(password)
        user.save()

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Super Admin created successfully!"
            )
        )
        self.stdout.write(f"Email: {user.email}")
        self.stdout.write(f"Role: {user.role}")
        self.stdout.write(f"Account Type: {user.account_type}")
        self.stdout.write("")