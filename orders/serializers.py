from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "sku",
            "unit_price",
            "quantity",
            "total_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "product_name",
            "sku",
            "unit_price",
            "total_price",
            "created_at",
            "updated_at",
        ]


class OrderCreateItemSerializer(serializers.Serializer):
    product = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField(
        max_length=150,
    )

    mobile_number = serializers.CharField(
        max_length=15,
    )

    delivery_address = serializers.CharField()

    area = serializers.CharField(
        max_length=150,
    )

    city = serializers.CharField(
        max_length=100,
    )

    state = serializers.CharField(
        max_length=100,
    )

    pincode = serializers.CharField(
        max_length=10,
    )

    items = OrderCreateItemSerializer(
        many=True,
    )

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError(
                "Order must contain at least one item."
            )

        return value


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]

    def validate_status(self, value):
        current_status = self.instance.status

        if current_status == value:
            raise serializers.ValidationError(
                f"Order is already {value}."
            )

        allowed_transitions = {
            Order.OrderStatus.PLACED: {
                Order.OrderStatus.CONFIRMED,
                Order.OrderStatus.CANCELLED,
            },
            Order.OrderStatus.CONFIRMED: {
                Order.OrderStatus.PROCESSING,
                Order.OrderStatus.CANCELLED,
            },
            Order.OrderStatus.PROCESSING: {
                Order.OrderStatus.SHIPPED,
                Order.OrderStatus.CANCELLED,
            },
            Order.OrderStatus.SHIPPED: {
                Order.OrderStatus.DELIVERED,
            },
            Order.OrderStatus.DELIVERED: set(),
            Order.OrderStatus.CANCELLED: set(),
        }

        allowed_statuses = allowed_transitions.get(
            current_status,
            set(),
        )

        if value not in allowed_statuses:
            current_label = self._format_status(
                current_status
            )
            requested_label = self._format_status(
                value
            )

            if current_status in {
                Order.OrderStatus.SHIPPED,
                Order.OrderStatus.DELIVERED,
                Order.OrderStatus.CANCELLED,
            }:
                raise serializers.ValidationError(
                    f"Order cannot be changed from "
                    f"{current_label} to {requested_label}."
                )

            raise serializers.ValidationError(
                f"Invalid order status transition: "
                f"{current_label} to {requested_label}."
            )

        return value

    @staticmethod
    def _format_status(value):
        return value.replace("_", " ").title()


class OrderAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "customer_name",
            "mobile_number",
            "delivery_address",
            "area",
            "city",
            "state",
            "pincode",
        ]

    def validate_customer_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Customer name is required."
            )

        return value

    def validate_mobile_number(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Mobile number is required."
            )

        if not value.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain only digits."
            )

        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError(
                "Mobile number must contain 10 to 15 digits."
            )

        return value

    def validate_delivery_address(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Delivery address is required."
            )

        return value

    def validate_area(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Area is required."
            )

        return value

    def validate_city(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "City is required."
            )

        return value

    def validate_state(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "State is required."
            )

        return value

    def validate_pincode(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Pincode is required."
            )

        if not value.isdigit():
            raise serializers.ValidationError(
                "Pincode must contain only digits."
            )

        if len(value) < 4 or len(value) > 10:
            raise serializers.ValidationError(
                "Pincode must contain 4 to 10 digits."
            )

        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "customer",
            "status",
            "payment_method",
            "payment_status",
            "customer_name",
            "mobile_number",
            "delivery_address",
            "area",
            "city",
            "state",
            "pincode",
            "subtotal",
            "delivery_charge",
            "total_amount",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "order_number",
            "customer",
            "status",
            "payment_method",
            "payment_status",
            "customer_name",
            "mobile_number",
            "delivery_address",
            "area",
            "city",
            "state",
            "pincode",
            "subtotal",
            "delivery_charge",
            "total_amount",
            "items",
            "created_at",
            "updated_at",
        ]