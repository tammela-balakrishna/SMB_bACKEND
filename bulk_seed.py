from decimal import Decimal
from django.apps import apps
from django.db import transaction


# ============================================================
# LOAD MODELS SAFELY
# ============================================================

VehicleBrand = apps.get_model("vehicles", "VehicleBrand")
VehicleModel = apps.get_model("vehicles", "VehicleModel")
VehicleVariant = apps.get_model("vehicles", "VehicleVariant")
VehicleYear = apps.get_model("vehicles", "VehicleYear")

ProductCategory = apps.get_model("vehicles", "ProductCategory")
ProductBrand = apps.get_model("vehicles", "ProductBrand")
Product = apps.get_model("vehicles", "Product")
ProductCompatibility = apps.get_model("vehicles", "ProductCompatibility")


# ============================================================
# SEED DATA
# ============================================================

@transaction.atomic
def seed_database():

    print("")
    print("======================================")
    print("      SMU BULK DATA SEED START")
    print("======================================")

    # ========================================================
    # 1. VEHICLE BRANDS
    # ========================================================

    vehicle_brands_data = [
        "Honda",
        "Hero",
        "Bajaj",
        "TVS",
        "Yamaha",
        "Suzuki",
        "Royal Enfield",
        "KTM",
        "Mahindra",
        "Kawasaki",
    ]

    vehicle_brands = {}

    for name in vehicle_brands_data:
        obj, created = VehicleBrand.objects.get_or_create(
            name=name,
            defaults={"is_active": True},
        )

        if not obj.is_active:
            obj.is_active = True
            obj.save(update_fields=["is_active"])

        vehicle_brands[name] = obj

    print("Vehicle Brands:", VehicleBrand.objects.count())


    # ========================================================
    # 2. VEHICLE MODELS
    # ========================================================

    vehicle_models_data = {
        "Honda": [
            "Activa 5G",
            "Activa 6G",
            "Shine",
            "SP 125",
            "Unicorn",
        ],
        "Hero": [
            "Splendor Plus",
            "HF Deluxe",
            "Passion Pro",
            "Glamour",
            "Xtreme 125R",
        ],
        "Bajaj": [
            "Pulsar 125",
            "Pulsar 150",
            "Pulsar NS200",
            "Platina 100",
            "CT 100",
        ],
        "TVS": [
            "Apache RTR 160",
            "Apache RTR 200",
            "Jupiter",
            "NTORQ 125",
            "Raider 125",
        ],
        "Yamaha": [
            "FZ-S",
            "MT-15",
            "R15 V4",
            "Fascino 125",
            "RayZR 125",
        ],
        "Suzuki": [
            "Access 125",
            "Burgman Street",
            "Gixxer",
            "Avenis 125",
        ],
        "Royal Enfield": [
            "Classic 350",
            "Bullet 350",
            "Hunter 350",
            "Meteor 350",
        ],
        "KTM": [
            "Duke 125",
            "Duke 200",
            "RC 200",
        ],
        "Mahindra": [
            "Centuro",
            "Gusto",
        ],
        "Kawasaki": [
            "Ninja 300",
            "Ninja 400",
        ],
    }

    vehicle_models = {}

    for brand_name, model_names in vehicle_models_data.items():

        brand = vehicle_brands[brand_name]

        for model_name in model_names:
            obj, created = VehicleModel.objects.get_or_create(
                vehicle_brand=brand,
                name=model_name,
                defaults={"is_active": True},
            )

            if not obj.is_active:
                obj.is_active = True
                obj.save(update_fields=["is_active"])

            vehicle_models[model_name] = obj

    print("Vehicle Models:", VehicleModel.objects.count())


    # ========================================================
    # 3. VEHICLE VARIANTS
    # ========================================================

    variants_data = {
        "Activa 5G": [
            ("110cc", 110, "PETROL", "AUTOMATIC"),
        ],
        "Activa 6G": [
            ("110cc", 110, "PETROL", "AUTOMATIC"),
        ],
        "Shine": [
            ("125cc", 125, "PETROL", "MANUAL"),
        ],
        "SP 125": [
            ("125cc", 125, "PETROL", "MANUAL"),
        ],
        "Unicorn": [
            ("160cc", 160, "PETROL", "MANUAL"),
        ],

        "Splendor Plus": [
            ("100cc", 100, "PETROL", "MANUAL"),
        ],
        "HF Deluxe": [
            ("100cc", 100, "PETROL", "MANUAL"),
        ],
        "Passion Pro": [
            ("110cc", 110, "PETROL", "MANUAL"),
        ],
        "Glamour": [
            ("125cc", 125, "PETROL", "MANUAL"),
        ],
        "Xtreme 125R": [
            ("125cc", 125, "PETROL", "MANUAL"),
        ],

        "Pulsar 125": [
            ("125cc", 125, "PETROL", "MANUAL"),
        ],
        "Pulsar 150": [
            ("150cc", 150, "PETROL", "MANUAL"),
        ],
        "Pulsar NS200": [
            ("200cc", 200, "PETROL", "MANUAL"),
        ],
        "Platina 100": [
            ("100cc", 100, "PETROL", "MANUAL"),
        ],
        "CT 100": [
            ("100cc", 100, "PETROL", "MANUAL"),
        ],

        "Apache RTR 160": [
            ("160cc", 160, "PETROL", "MANUAL"),
        ],
        "Apache RTR 200": [
            ("200cc", 200, "PETROL", "MANUAL"),
        ],
        "Jupiter": [
            ("110cc", 110, "PETROL", "AUTOMATIC"),
        ],
        "NTORQ 125": [
            ("125cc", 125, "PETROL", "AUTOMATIC"),
        ],
        "Raider 125": [
            ("125cc", 125, "PETROL", "MANUAL"),
        ],

        "FZ-S": [
            ("150cc", 150, "PETROL", "MANUAL"),
        ],
        "MT-15": [
            ("155cc", 155, "PETROL", "MANUAL"),
        ],
        "R15 V4": [
            ("155cc", 155, "PETROL", "MANUAL"),
        ],
        "Fascino 125": [
            ("125cc", 125, "PETROL", "AUTOMATIC"),
        ],
        "RayZR 125": [
            ("125cc", 125, "PETROL", "AUTOMATIC"),
        ],

        "Access 125": [
            ("125cc", 125, "PETROL", "AUTOMATIC"),
        ],
        "Burgman Street": [
            ("125cc", 125, "PETROL", "AUTOMATIC"),
        ],
        "Gixxer": [
            ("155cc", 155, "PETROL", "MANUAL"),
        ],
        "Avenis 125": [
            ("125cc", 125, "PETROL", "AUTOMATIC"),
        ],

        "Classic 350": [
            ("350cc", 349, "PETROL", "MANUAL"),
        ],
        "Bullet 350": [
            ("350cc", 349, "PETROL", "MANUAL"),
        ],
        "Hunter 350": [
            ("350cc", 349, "PETROL", "MANUAL"),
        ],
        "Meteor 350": [
            ("350cc", 349, "PETROL", "MANUAL"),
        ],

        "Duke 125": [
            ("125cc", 125, "PETROL", "MANUAL"),
        ],
        "Duke 200": [
            ("200cc", 199, "PETROL", "MANUAL"),
        ],
        "RC 200": [
            ("200cc", 199, "PETROL", "MANUAL"),
        ],

        "Centuro": [
            ("110cc", 106, "PETROL", "MANUAL"),
        ],
        "Gusto": [
            ("110cc", 110, "PETROL", "AUTOMATIC"),
        ],

        "Ninja 300": [
            ("300cc", 296, "PETROL", "MANUAL"),
        ],
        "Ninja 400": [
            ("400cc", 399, "PETROL", "MANUAL"),
        ],
    }

    vehicle_variants = {}

    for model_name, variants in variants_data.items():

        model = vehicle_models[model_name]

        for variant_name, engine_cc, fuel_type, transmission in variants:

            obj, created = VehicleVariant.objects.get_or_create(
                vehicle_model=model,
                name=variant_name,
                defaults={
                    "engine_cc": engine_cc,
                    "fuel_type": fuel_type,
                    "transmission": transmission,
                    "is_active": True,
                },
            )

            vehicle_variants[(model_name, variant_name)] = obj

    print("Vehicle Variants:", VehicleVariant.objects.count())


    # ========================================================
    # 4. VEHICLE YEARS
    # ========================================================

    years = [2020, 2021, 2022, 2023, 2024, 2025]

    for variant in VehicleVariant.objects.all():

        for year in years:

            VehicleYear.objects.get_or_create(
                vehicle_variant=variant,
                year=year,
                defaults={"is_active": True},
            )

    print("Vehicle Years:", VehicleYear.objects.count())


    # ========================================================
    # 5. PRODUCT CATEGORIES
    # ========================================================

    categories_data = [
        ("Engine Parts", "Engine related spare parts"),
        ("Brake System", "Brake pads, shoes and related parts"),
        ("Clutch Parts", "Clutch plates and clutch components"),
        ("Electrical", "Electrical and ignition components"),
        ("Filters", "Air, oil and fuel filters"),
        ("Lights", "Headlights, indicators and bulbs"),
        ("Cables", "Clutch, brake and accelerator cables"),
        ("Suspension", "Shock absorbers and suspension parts"),
        ("Body Parts", "Body and exterior spare parts"),
        ("Service Parts", "Regular maintenance and service parts"),
    ]

    categories = {}

    for name, description in categories_data:

        obj, created = ProductCategory.objects.get_or_create(
            name=name,
            defaults={
                "description": description,
                "is_active": True,
            },
        )

        if not obj.is_active:
            obj.is_active = True
            obj.save(update_fields=["is_active"])

        categories[name] = obj

    print("Product Categories:", ProductCategory.objects.count())


    # ========================================================
    # 6. PRODUCT BRANDS
    # ========================================================

    product_brands_data = [
        "Bosch",
        "NGK",
        "SKF",
        "Exide",
        "Uno Minda",
        "Endurance",
        "Gabriel",
        "Rolon",
        "Lumax",
        "TVS",
    ]

    product_brands = {}

    for name in product_brands_data:

        obj, created = ProductBrand.objects.get_or_create(
            name=name,
            defaults={
                "description": f"{name} motorcycle spare parts",
                "is_active": True,
            },
        )

        if not obj.is_active:
            obj.is_active = True
            obj.save(update_fields=["is_active"])

        product_brands[name] = obj

    print("Product Brands:", ProductBrand.objects.count())


    # ========================================================
    # 7. 50 PRODUCTS
    # ========================================================

    products_data = [

        ("Engine Oil 10W40 1L", "Engine Parts", "Bosch", "SMU-ENG-001", 650),
        ("Engine Oil 20W50 1L", "Engine Parts", "TVS", "SMU-ENG-002", 580),
        ("Spark Plug Standard", "Engine Parts", "NGK", "SMU-ENG-003", 180),
        ("Spark Plug Iridium", "Engine Parts", "NGK", "SMU-ENG-004", 550),
        ("Cam Chain", "Engine Parts", "Rolon", "SMU-ENG-005", 450),

        ("Front Disc Brake Pad", "Brake System", "Bosch", "SMU-BRK-001", 420),
        ("Rear Brake Shoe", "Brake System", "Endurance", "SMU-BRK-002", 380),
        ("Front Brake Shoe", "Brake System", "TVS", "SMU-BRK-003", 350),
        ("Disc Brake Pad Premium", "Brake System", "Uno Minda", "SMU-BRK-004", 520),
        ("Brake Shoe Set", "Brake System", "Endurance", "SMU-BRK-005", 400),

        ("Clutch Plate Set", "Clutch Parts", "Endurance", "SMU-CLU-001", 1250),
        ("Clutch Cable", "Clutch Parts", "Uno Minda", "SMU-CLU-002", 260),
        ("Clutch Spring Set", "Clutch Parts", "TVS", "SMU-CLU-003", 320),
        ("Clutch Friction Plate", "Clutch Parts", "Endurance", "SMU-CLU-004", 850),
        ("Clutch Assembly", "Clutch Parts", "Endurance", "SMU-CLU-005", 1800),

        ("12V Horn", "Electrical", "Uno Minda", "SMU-ELC-001", 280),
        ("Ignition Coil", "Electrical", "Bosch", "SMU-ELC-002", 650),
        ("Rectifier Regulator", "Electrical", "Uno Minda", "SMU-ELC-003", 780),
        ("Battery 12V", "Electrical", "Exide", "SMU-ELC-004", 1450),
        ("Starter Relay", "Electrical", "Uno Minda", "SMU-ELC-005", 350),

        ("Air Filter", "Filters", "Bosch", "SMU-FLT-001", 320),
        ("Oil Filter", "Filters", "Bosch", "SMU-FLT-002", 220),
        ("Fuel Filter", "Filters", "TVS", "SMU-FLT-003", 180),
        ("Air Filter Premium", "Filters", "Uno Minda", "SMU-FLT-004", 450),
        ("Oil Filter Premium", "Filters", "Bosch", "SMU-FLT-005", 300),

        ("LED Headlight Bulb", "Lights", "Lumax", "SMU-LGT-001", 650),
        ("Halogen Headlight Bulb", "Lights", "Lumax", "SMU-LGT-002", 250),
        ("Front Indicator Set", "Lights", "Lumax", "SMU-LGT-003", 450),
        ("Rear Indicator Set", "Lights", "Uno Minda", "SMU-LGT-004", 480),
        ("Tail Light Assembly", "Lights", "Lumax", "SMU-LGT-005", 720),

        ("Clutch Cable Standard", "Cables", "Uno Minda", "SMU-CBL-001", 220),
        ("Front Brake Cable", "Cables", "Uno Minda", "SMU-CBL-002", 200),
        ("Rear Brake Cable", "Cables", "TVS", "SMU-CBL-003", 220),
        ("Accelerator Cable", "Cables", "Uno Minda", "SMU-CBL-004", 240),
        ("Speedometer Cable", "Cables", "TVS", "SMU-CBL-005", 260),

        ("Front Shock Absorber", "Suspension", "Gabriel", "SMU-SUS-001", 1850),
        ("Rear Shock Absorber", "Suspension", "Gabriel", "SMU-SUS-002", 2200),
        ("Fork Seal Set", "Suspension", "SKF", "SMU-SUS-003", 380),
        ("Steering Cone Set", "Suspension", "SKF", "SMU-SUS-004", 650),
        ("Rear Suspension Bush", "Suspension", "Endurance", "SMU-SUS-005", 320),

        ("Side Stand", "Body Parts", "Endurance", "SMU-BDY-001", 480),
        ("Main Stand", "Body Parts", "Endurance", "SMU-BDY-002", 750),
        ("Rear View Mirror Set", "Body Parts", "Uno Minda", "SMU-BDY-003", 550),
        ("Number Plate Frame", "Body Parts", "TVS", "SMU-BDY-004", 180),
        ("Foot Rest Set", "Body Parts", "Endurance", "SMU-BDY-005", 620),

        ("Chain Sprocket Kit", "Service Parts", "Rolon", "SMU-SRV-001", 1450),
        ("Drive Chain", "Service Parts", "Rolon", "SMU-SRV-002", 850),
        ("Wheel Bearing Set", "Service Parts", "SKF", "SMU-SRV-003", 550),
        ("Brake Fluid 500ml", "Service Parts", "Bosch", "SMU-SRV-004", 320),
        ("Grease 100g", "Service Parts", "TVS", "SMU-SRV-005", 150),
    ]


    # ========================================================
    # CREATE PRODUCTS
    # ========================================================

    products = []

    for name, category_name, brand_name, sku, mrp in products_data:

        category = categories[category_name]
        brand = product_brands[brand_name]

        product, created = Product.objects.get_or_create(
            sku=sku,
            defaults={
                "product_category": category,
                "product_brand": brand,
                "name": name,
                "description": f"{name} - genuine quality motorcycle spare part.",
                "mrp": Decimal(str(mrp)),
                "is_active": True,
                "is_featured": False,
            },
        )

        if not created:
            product.product_category = category
            product.product_brand = brand
            product.name = name
            product.description = (
                f"{name} - genuine quality motorcycle spare part."
            )
            product.mrp = Decimal(str(mrp))
            product.is_active = True
            product.save()

        products.append(product)

    print("Products:", Product.objects.count())


    # ========================================================
    # 8. PRODUCT COMPATIBILITY
    # ========================================================

    all_variants = list(VehicleVariant.objects.all())

    compatibility_count = 0

    for index, product in enumerate(products):

        # Give every product compatibility with 2 different variants.
        variant1 = all_variants[index % len(all_variants)]
        variant2 = all_variants[(index + 7) % len(all_variants)]

        for variant in [variant1, variant2]:

            model = variant.vehicle_model
            vehicle_brand = model.vehicle_brand

            years_for_variant = VehicleYear.objects.filter(
                vehicle_variant=variant,
                is_active=True,
            ).order_by("year")

            # Use the latest available year.
            vehicle_year = years_for_variant.last()

            if not vehicle_year:
                continue

            obj, created = ProductCompatibility.objects.get_or_create(
                product=product,
                vehicle_brand=vehicle_brand,
                vehicle_model=model,
                vehicle_variant=variant,
                vehicle_year=vehicle_year,
                defaults={
                    "notes": f"Compatible with {vehicle_brand.name} {model.name}."
                },
            )

            if created:
                compatibility_count += 1

    print("Compatibility records created:", compatibility_count)


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print("")
    print("======================================")
    print("       BULK DATA SEED COMPLETE")
    print("======================================")

    print("Vehicle Brands:", VehicleBrand.objects.count())
    print("Vehicle Models:", VehicleModel.objects.count())
    print("Vehicle Variants:", VehicleVariant.objects.count())
    print("Vehicle Years:", VehicleYear.objects.count())
    print("Product Categories:", ProductCategory.objects.count())
    print("Product Brands:", ProductBrand.objects.count())
    print("Products:", Product.objects.count())
    print("Compatibility:", ProductCompatibility.objects.count())

    print("======================================")



seed_database()