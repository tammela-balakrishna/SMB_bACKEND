from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from vehicles.models import CategoryDiscount, ProductCategory


class Command(BaseCommand):
    help = "Seed product category discounts"

    def handle(self, *args, **options):
        now = timezone.now()

        discounts = [
            {
                "category": "Engine Parts",
                "application_scope": "CATEGORY",
                "discount_type": "PERCENTAGE",
                "discount_value": Decimal("10.00"),
                "max_discount_amount": Decimal("500.00"),
                "min_order_amount": Decimal("500.00"),
                "priority": 1,
            },
            {
                "category": "Brake Parts",
                "application_scope": "CATEGORY",
                "discount_type": "PERCENTAGE",
                "discount_value": Decimal("15.00"),
                "max_discount_amount": Decimal("750.00"),
                "min_order_amount": Decimal("500.00"),
                "priority": 1,
            },
            {
                "category": "Clutch Parts",
                "application_scope": "CATEGORY",
                "discount_type": "PERCENTAGE",
                "discount_value": Decimal("10.00"),
                "max_discount_amount": Decimal("600.00"),
                "min_order_amount": Decimal("500.00"),
                "priority": 1,
            },
            {
                "category": "Electrical Parts",
                "application_scope": "CATEGORY",
                "discount_type": "PERCENTAGE",
                "discount_value": Decimal("8.00"),
                "max_discount_amount": Decimal("400.00"),
                "min_order_amount": Decimal("300.00"),
                "priority": 1,
            },
            {
                "category": "Filters",
                "application_scope": "CATEGORY",
                "discount_type": "PERCENTAGE",
                "discount_value": Decimal("12.00"),
                "max_discount_amount": Decimal("300.00"),
                "min_order_amount": Decimal("300.00"),
                "priority": 1,
            },
            {
                "category": "Suspension Parts",
                "application_scope": "CATEGORY",
                "discount_type": "PERCENTAGE",
                "discount_value": Decimal("10.00"),
                "max_discount_amount": Decimal("500.00"),
                "min_order_amount": Decimal("500.00"),
                "priority": 1,
            },
            {
                "category": "Transmission Parts",
                "application_scope": "CATEGORY",
                "discount_type": "PERCENTAGE",
                "discount_value": Decimal("10.00"),
                "max_discount_amount": Decimal("500.00"),
                "min_order_amount": Decimal("500.00"),
                "priority": 1,
            },
            {
                "category": "Body Parts",
                "application_scope": "CATEGORY",
                "discount_type": "PERCENTAGE",
                "discount_value": Decimal("5.00"),
                "max_discount_amount": Decimal("300.00"),
                "min_order_amount": Decimal("500.00"),
                "priority": 1,
            },
            {
                "category": "Cables",
                "application_scope": "CATEGORY",
                "discount_type": "PERCENTAGE",
                "discount_value": Decimal("8.00"),
                "max_discount_amount": Decimal("250.00"),
                "min_order_amount": Decimal("300.00"),
                "priority": 1,
            },
            {
                "category": "Tyres & Tubes",
                "application_scope": "CATEGORY",
                "discount_type": "PERCENTAGE",
                "discount_value": Decimal("7.00"),
                "max_discount_amount": Decimal("500.00"),
                "min_order_amount": Decimal("1000.00"),
                "priority": 1,
            },
            {
                "category": "Lights & Indicators",
                "application_scope": "CATEGORY",
                "discount_type": "PERCENTAGE",
                "discount_value": Decimal("10.00"),
                "max_discount_amount": Decimal("300.00"),
                "min_order_amount": Decimal("300.00"),
                "priority": 1,
            },
            {
                "category": "Batteries",
                "application_scope": "CATEGORY",
                "discount_type": "PERCENTAGE",
                "discount_value": Decimal("5.00"),
                "max_discount_amount": Decimal("250.00"),
                "min_order_amount": Decimal("1000.00"),
                "priority": 1,
            },
        ]

        created_count = 0
        existing_count = 0

        for data in discounts:
            try:
                category = ProductCategory.objects.get(
                    name=data["category"]
                )
            except ProductCategory.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Category not found: {data['category']}"
                    )
                )
                continue

            _, created = CategoryDiscount.objects.get_or_create(
                product_category=category,
                application_scope=data["application_scope"],
                discount_type=data["discount_type"],
                discount_value=data["discount_value"],
                defaults={
                    "max_discount_amount": data["max_discount_amount"],
                    "min_order_amount": data["min_order_amount"],
                    "start_at": now,
                    "end_at": now + timedelta(days=365),
                    "priority": data["priority"],
                    "is_active": True,
                },
            )

            if created:
                created_count += 1
            else:
                existing_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Discounts created: {created_count}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Discounts already existing: {existing_count}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total category discounts: "
                f"{CategoryDiscount.objects.count()}"
            )
        )