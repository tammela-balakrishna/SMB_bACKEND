def is_product_eligible_for_discount(discount, product):
    if not discount.is_active:
        return False

    if discount.product_category_id != product.product_category_id:
        return False

    if discount.application_scope == (
        CategoryDiscount.ApplicationScope.ALL_PRODUCTS
    ):
        return True

    mapped = CategoryDiscountProduct.objects.filter(
        category_discount=discount,
        product=product,
    ).exists()

    if discount.application_scope == (
        CategoryDiscount.ApplicationScope.SELECTED_PRODUCTS
    ):
        return mapped

    if discount.application_scope == (
        CategoryDiscount.ApplicationScope.EXCLUDE_PRODUCTS
    ):
        return not mapped

    return False
from decimal import Decimal


def calculate_discount_amount(discount, price):
    price = Decimal(price)

    if price <= 0:
        return Decimal("0.00")

    if discount.discount_type == (
        CategoryDiscount.DiscountType.PERCENTAGE
    ):
        discount_amount = (
            price * discount.discount_value / Decimal("100")
        )

        if discount.max_discount_amount is not None:
            discount_amount = min(
                discount_amount,
                discount.max_discount_amount,
            )

    else:
        discount_amount = min(
            discount.discount_value,
            price,
        )

    return discount_amount.quantize(Decimal("0.01"))