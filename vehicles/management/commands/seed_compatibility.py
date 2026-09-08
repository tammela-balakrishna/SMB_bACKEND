from django.core.management.base import BaseCommand

from vehicles.models import Product, ProductCompatibility, VehicleYear


class Command(BaseCommand):
    help = "Seed product and vehicle compatibility data"

    def handle(self, *args, **options):
        compatibility_data = {
            "HON-ENG-FLT-001": [
                ("Honda", "Activa", "Activa 6G Standard"),
                ("Honda", "Activa", "Activa 6G Deluxe"),
            ],
            "HON-BRK-PAD-001": [
                ("Honda", "Activa", "Activa 6G Standard"),
                ("Honda", "Activa", "Activa 6G Deluxe"),
            ],
            "HER-BRK-SHO-001": [
                ("Hero", "Splendor Plus", "Splendor Plus Standard"),
                ("Hero", "Splendor Plus", "Splendor Plus XTEC"),
            ],
            "TVS-CLU-PLT-001": [
                ("TVS", "Apache RTR 160", "Apache RTR 160 2V"),
                ("TVS", "Apache RTR 160", "Apache RTR 160 4V"),
            ],
            "BOS-SPK-001": [
                ("Honda", "Activa", "Activa 6G Standard"),
                ("Honda", "Activa", "Activa 6G Deluxe"),
            ],
            "NGK-SPK-001": [
                ("Yamaha", "FZ-S", "FZ-S FI"),
                ("Yamaha", "FZ-S", "FZ-S Deluxe"),
            ],
            "HER-AIR-FLT-001": [
                ("Hero", "Splendor Plus", "Splendor Plus Standard"),
                ("Hero", "Splendor Plus", "Splendor Plus XTEC"),
            ],
            "HON-AIR-FLT-001": [
                ("Honda", "Activa", "Activa 6G Standard"),
                ("Honda", "Activa", "Activa 6G Deluxe"),
            ],
            "TVS-SUS-SEAL-001": [
                ("TVS", "Jupiter", None),
            ],
            "BAJ-TRN-GLV-001": [
                ("Bajaj", "Pulsar 150", "Pulsar 150 Neon"),
                ("Bajaj", "Pulsar 150", "Pulsar 150 Twin Disc"),
            ],
            "YAM-BDY-SP-001": [
                ("Yamaha", "FZ-S", "FZ-S FI"),
                ("Yamaha", "FZ-S", "FZ-S Deluxe"),
            ],
            "SUZ-CAB-THR-001": [
                ("Suzuki", "Access 125", "Access 125 Standard"),
                ("Suzuki", "Access 125", "Access 125 Special Edition"),
            ],
        }

        created_count = 0
        existing_count = 0

        for sku, vehicle_list in compatibility_data.items():

            try:
                product = Product.objects.get(sku=sku)
            except Product.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Product not found: {sku}"
                    )
                )
                continue

            for brand_name, model_name, variant_name in vehicle_list:

                filters = {
                    "vehicle_variant__vehicle_model__vehicle_brand__name": brand_name,
                    "vehicle_variant__vehicle_model__name": model_name,
                }

                if variant_name:
                    filters["vehicle_variant__name"] = variant_name

                vehicle_years = VehicleYear.objects.filter(**filters)

                for vehicle_year in vehicle_years:

                    _, created = ProductCompatibility.objects.get_or_create(
                        product=product,
                        vehicle_year=vehicle_year,
                        defaults={
                            "notes": (
                                f"Compatible with {brand_name} "
                                f"{model_name}"
                            )
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        existing_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Compatibility records created: {created_count}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Compatibility records already existing: "
                f"{existing_count}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total compatibility records: "
                f"{ProductCompatibility.objects.count()}"
            )
        )