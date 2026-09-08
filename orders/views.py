import uuid
from decimal import Decimal

from django.db import transaction
from django.db.models import Prefetch

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsOrderManager
from vehicles.models import Product

from .models import Order, OrderItem
from .serializers import (
    OrderAddressUpdateSerializer,
    OrderCreateSerializer,
    OrderSerializer,
    OrderStatusUpdateSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Order.objects.prefetch_related(
            Prefetch(
                "items",
                queryset=OrderItem.objects.select_related(
                    "product"
                ),
            )
        ).select_related("customer")

        if (
            user.account_type == "STAFF"
            and user.role in {
                "SALES_MANAGER",
                "SUPER_ADMIN",
            }
        ):
            return queryset

        return queryset.filter(customer=user)

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        items_data = validated_data.pop("items")

        product_ids = [
            item["product"]
            for item in items_data
        ]

        with transaction.atomic():
            products = Product.objects.select_for_update().filter(
                id__in=product_ids,
                is_active=True,
            )

            products_by_id = {
                product.id: product
                for product in products
            }

            if len(products_by_id) != len(
                set(product_ids)
            ):
                missing_ids = sorted(
                    set(product_ids)
                    - set(products_by_id.keys())
                )

                return Response(
                    {
                        "detail": (
                            "One or more products are unavailable."
                        ),
                        "product_ids": missing_ids,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subtotal = Decimal("0.00")

            order_items = []

            for item_data in items_data:
                product = products_by_id[
                    item_data["product"]
                ]

                quantity = item_data["quantity"]

                unit_price = product.mrp

                total_price = (
                    unit_price * quantity
                )

                subtotal += total_price

                order_items.append(
                    {
                        "product": product,
                        "product_name": product.name,
                        "sku": product.sku,
                        "unit_price": unit_price,
                        "quantity": quantity,
                        "total_price": total_price,
                    }
                )

            delivery_charge = Decimal("0.00")

            total_amount = (
                subtotal + delivery_charge
            )

            order = Order.objects.create(
                customer=request.user,
                order_number=self._generate_order_number(),
                status=Order.OrderStatus.PLACED,
                payment_method=Order.PaymentMethod.COD,
                payment_status=Order.PaymentStatus.PENDING,
                customer_name=validated_data[
                    "customer_name"
                ],
                mobile_number=validated_data[
                    "mobile_number"
                ],
                delivery_address=validated_data[
                    "delivery_address"
                ],
                area=validated_data["area"],
                city=validated_data["city"],
                state=validated_data["state"],
                pincode=validated_data["pincode"],
                subtotal=subtotal,
                delivery_charge=delivery_charge,
                total_amount=total_amount,
            )

            OrderItem.objects.bulk_create(
                [
                    OrderItem(
                        order=order,
                        **item,
                    )
                    for item in order_items
                ]
            )

        response_serializer = OrderSerializer(
            order,
            context={"request": request},
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsOrderManager],
        url_path="status",
    )
    def update_status(self, request, *args, **kwargs):
        order = self.get_object()

        serializer = OrderStatusUpdateSerializer(
            order,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            OrderSerializer(
                order,
                context={"request": request},
            ).data,
        )

def update_status(self, request, *args, **kwargs):
    order = self.get_object()

    serializer = OrderStatusUpdateSerializer(
        order,
        data=request.data,
        partial=True,
    )

    serializer.is_valid(raise_exception=True)

    with transaction.atomic():
        order = serializer.save()

        if (
            order.status == Order.OrderStatus.DELIVERED
            and order.payment_method == Order.PaymentMethod.COD
            and order.payment_status == Order.PaymentStatus.PENDING
        ):
            order.payment_status = Order.PaymentStatus.PAID
            order.save(
                update_fields=[
                    "payment_status",
                    "updated_at",
                ]
            )

    return Response(
        OrderSerializer(
            order,
            context={"request": request},
        ).data,
    )

    @staticmethod
    def _generate_order_number():
        return (
            f"SMB-{uuid.uuid4().hex[:12].upper()}"
        )