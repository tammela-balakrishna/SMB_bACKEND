from django.core.management.base import BaseCommand

from accounts.models import User
from addresses.models import CustomerAddress


class Command(BaseCommand):
    help = "Seed test customer accounts and customer addresses"

    def handle(self, *args, **options):
        customers = [
            {
                "email": "customer1@smb.test",
                "first_name": "Ravi",
                "last_name": "Kumar",
                "mobile": "9876543210",
            },
            {
                "email": "customer2@smb.test",
                "first_name": "Suresh",
                "last_name": "Reddy",
                "mobile": "9876543211",
            },
            {
                "email": "customer3@smb.test",
                "first_name": "Arun",
                "last_name": "Kumar",
                "mobile": "9876543212",
            },
        ]

        created_customers = 0
        existing_customers = 0

        for data in customers:
            user, created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "account_type": User.AccountType.CUSTOMER,
                    "is_active": True,
                    "is_verified": True,
                    "is_staff": False,
                    "is_superuser": False,
                },
            )

            if created:
                user.set_unusable_password()
                user.save(update_fields=["password"])
                created_customers += 1
            else:
                existing_customers += 1

            address_exists = CustomerAddress.objects.filter(
                customer=user
            ).exists()

            if not address_exists:
                CustomerAddress.objects.create(
                    customer=user,
                    address_type=CustomerAddress.AddressType.HOME,
                    full_name=f"{data['first_name']} {data['last_name']}",
                    mobile_number=data["mobile"],
                    delivery_address="12 Main Road",
                    area="Rayachoti",
                    city="Rayachoti",
                    state="Andhra Pradesh",
                    pincode="516269",
                    is_default=True,
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Customers created: {created_customers}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Customers already existing: {existing_customers}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total customers: "
                f"{User.objects.filter(account_type=User.AccountType.CUSTOMER).count()}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total customer addresses: "
                f"{CustomerAddress.objects.count()}"
            )
        )