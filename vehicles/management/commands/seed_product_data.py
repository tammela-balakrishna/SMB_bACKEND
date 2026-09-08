from django.core.management.base import BaseCommand

from vehicles.models import ProductBrand, ProductCategory


class Command(BaseCommand):
    help = "Seed product categories and product brands"

    def handle(self, *args, **options):
        categories = [
            (
                "Engine Parts",
                "Engine components and spare parts",
            ),
            (
                "Brake Parts",
                "Brake pads, shoes, discs and related parts",
            ),
            (
                "Clutch Parts",
                "Clutch plates, cables and related parts",
            ),
            (
                "Electrical Parts",
                "Electrical and ignition components",
            ),
            (
                "Filters",
                "Air, oil and fuel filters",
            ),
            (
                "Suspension Parts",
                "Front and rear suspension components",
            ),
            (
                "Transmission Parts",
                "Gearbox and transmission components",
            ),
            (
                "Body Parts",
                "Body panels and exterior spare parts",
            ),
            (
                "Cables",
                "Clutch, brake, accelerator and other cables",
            ),
            (
                "Tyres & Tubes",
                "Two-wheeler tyres and tubes",
            ),
            (
                "Lights & Indicators",
                "Headlights, indicators and lighting components",
            ),
            (
                "Batteries",
                "Two-wheeler batteries",
            ),
        ]

        brands = [
            "Honda Genuine",
            "Hero Genuine",
            "TVS Genuine",
            "Bajaj Genuine",
            "Yamaha Genuine",
            "Suzuki Genuine",
            "Bosch",
            "NGK",
            "SKF",
            "Exide",
            "MRF",
            "CEAT",
        ]

        category_count = 0
        brand_count = 0

        for name, description in categories:
            _, created = ProductCategory.objects.get_or_create(
                name=name,
                defaults={
                    "description": description,
                    "is_active": True,
                },
            )

            if created:
                category_count += 1

        for name in brands:
            _, created = ProductBrand.objects.get_or_create(
                name=name,
                defaults={
                    "description": f"{name} spare parts and components",
                    "is_active": True,
                },
            )

            if created:
                brand_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Product categories created: {category_count}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Product brands created: {brand_count}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total categories: {ProductCategory.objects.count()}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Total brands: {ProductBrand.objects.count()}"
            )
        )