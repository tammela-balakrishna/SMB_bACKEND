from decimal import Decimal

from django.core.management.base import BaseCommand

from vehicles.models import Product, ProductBrand, ProductCategory


class Command(BaseCommand):
    help = "Seed sample two-wheeler spare products"

    def handle(self, *args, **options):
        products = [
            {
                "category": "Engine Parts",
                "brand": "Honda Genuine",
                "name": "Honda Activa Engine Oil Filter",
                "sku": "HON-ENG-FLT-001",
                "description": "Genuine engine oil filter for compatible Honda two-wheelers.",
                "mrp": Decimal("180.00"),
            },
            {
                "category": "Brake Parts",
                "brand": "Honda Genuine",
                "name": "Honda Activa Front Brake Pad",
                "sku": "HON-BRK-PAD-001",
                "description": "Front disc brake pad for compatible Honda scooters.",
                "mrp": Decimal("450.00"),
            },
            {
                "category": "Brake Parts",
                "brand": "Hero Genuine",
                "name": "Hero Splendor Front Brake Shoe",
                "sku": "HER-BRK-SHO-001",
                "description": "Front brake shoe for compatible Hero motorcycles.",
                "mrp": Decimal("320.00"),
            },
            {
                "category": "Clutch Parts",
                "brand": "TVS Genuine",
                "name": "TVS Apache Clutch Plate Set",
                "sku": "TVS-CLU-PLT-001",
                "description": "Clutch plate set for compatible TVS motorcycles.",
                "mrp": Decimal("850.00"),
            },
            {
                "category": "Electrical Parts",
                "brand": "Bosch",
                "name": "Two Wheeler Spark Plug",
                "sku": "BOS-SPK-001",
                "description": "Bosch spark plug for compatible two-wheelers.",
                "mrp": Decimal("160.00"),
            },
            {
                "category": "Electrical Parts",
                "brand": "NGK",
                "name": "NGK Spark Plug",
                "sku": "NGK-SPK-001",
                "description": "NGK spark plug for compatible motorcycles and scooters.",
                "mrp": Decimal("175.00"),
            },
            {
                "category": "Filters",
                "brand": "Hero Genuine",
                "name": "Hero Splendor Air Filter",
                "sku": "HER-AIR-FLT-001",
                "description": "Air filter for compatible Hero motorcycles.",
                "mrp": Decimal("220.00"),
            },
            {
                "category": "Filters",
                "brand": "Honda Genuine",
                "name": "Honda Activa Air Filter",
                "sku": "HON-AIR-FLT-001",
                "description": "Air filter for compatible Honda scooters.",
                "mrp": Decimal("250.00"),
            },
            {
                "category": "Suspension Parts",
                "brand": "TVS Genuine",
                "name": "TVS Jupiter Front Fork Seal",
                "sku": "TVS-SUS-SEAL-001",
                "description": "Front fork oil seal for compatible TVS scooters.",
                "mrp": Decimal("190.00"),
            },
            {
                "category": "Transmission Parts",
                "brand": "Bajaj Genuine",
                "name": "Bajaj Pulsar Gear Lever",
                "sku": "BAJ-TRN-GLV-001",
                "description": "Gear lever for compatible Bajaj motorcycles.",
                "mrp": Decimal("280.00"),
            },
            {
                "category": "Body Parts",
                "brand": "Yamaha Genuine",
                "name": "Yamaha FZ Side Panel",
                "sku": "YAM-BDY-SP-001",
                "description": "Side body panel for compatible Yamaha FZ models.",
                "mrp": Decimal("950.00"),
            },
            {
                "category": "Cables",
                "brand": "Suzuki Genuine",
                "name": "Suzuki Access Throttle Cable",
                "sku": "SUZ-CAB-THR-001",
                "description": "Throttle cable for compatible Suzuki scooters.",
                "mrp": Decimal("240.00"),
            },
            {
                "category": "Tyres & Tubes",
                "brand": "MRF",
                "name": "MRF Two Wheeler Tyre",
                "sku": "MRF-TYR-001",
                "description": "Two-wheeler tyre for compatible motorcycles.",
                "mrp": Decimal("1850.00"),
            },
            {
                "category": "Tyres & Tubes",
                "brand": "CEAT",
                "name": "CEAT Two Wheeler Tyre",
                "sku": "CEAT-TYR-001",
                "description": "Two-wheeler tyre for compatible motorcycles.",
                "mrp": Decimal("1750.00"),
            },
            {
                "category": "Lights & Indicators",
                "brand": "Honda Genuine",
                "name": "Honda Activa Front Indicator",
                "sku": "HON-LGT-IND-001",
                "description": "Front indicator lamp for compatible Honda scooters.",
                "mrp": Decimal("300.00"),
            },
            {
                "category": "Batteries",
                "brand": "Exide",
                "name": "Exide Two Wheeler Battery",
                "sku": "EXI-BAT-001",
                "description": "Two-wheeler battery for compatible motorcycles and scooters.",
                "mrp": Decimal("1450.00"),
            },
        ]

        created_count = 0
        existing_count = 0

        for data in products:
            category = ProductCategory.objects.get(
                name=data["category"]
            )

            brand = ProductBrand.objects.get(
                name=data["brand"]
            )

            _, created = Product.objects.get_or_create(
                sku=data["sku"],
                defaults={
                    "product_category": category,
                    "product_brand": brand,
                    "name": data["name"],
                    "description": data["description"],
                    "mrp": data["mrp"],
                    "is_active": True,
                },
            )

            if created:
                created_count += 1
            else:
                existing_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Products created: {created_count}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Products already existing: {existing_count}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total products: {Product.objects.count()}"
            )
        )