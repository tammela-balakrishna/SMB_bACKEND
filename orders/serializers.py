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
            "subtotal",
            "delivery_charge",
            "total_amount",
            "items",
            "created_at",
            "updated_at",
        ]