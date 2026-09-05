from django.core.exceptions import ValidationError

from vehicles.models import (
    CategoryDiscount,
    CategoryDiscountProduct,
)


def validate_discount_scope(discount):
    mapping_count = CategoryDiscountProduct.objects.filter(
        category_discount=discount
    ).count()

    if (
        discount.application_scope
        == CategoryDiscount.ApplicationScope.ALL_PRODUCTS
    ):
        if mapping_count > 0:
            raise ValidationError(
                "ALL_PRODUCTS discount cannot have product mappings."
            )

    elif (
        discount.application_scope
        in (
            CategoryDiscount.ApplicationScope.SELECTED_PRODUCTS,
            CategoryDiscount.ApplicationScope.EXCLUDE_PRODUCTS,
        )
    ):
        if mapping_count == 0:
            raise ValidationError(
                "This discount scope requires at least one "
                "product mapping."
            )