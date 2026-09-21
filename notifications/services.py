from django.contrib.auth import get_user_model

from .fcm import send_notification_to_user
from .models import Notification


User = get_user_model()


def create_order_notification(order):
    status_messages = {
        "PLACED": (
            "Order Placed",
            f"Your order {order.order_number} has been placed.",
        ),
        "CONFIRMED": (
            "Order Confirmed",
            f"Your order {order.order_number} has been confirmed.",
        ),
        "PROCESSING": (
            "Order Processing",
            f"Your order {order.order_number} is being prepared.",
        ),
        "SHIPPED": (
            "Order Shipped",
            f"Your order {order.order_number} has been shipped.",
        ),
        "DELIVERED": (
            "Order Delivered",
            f"Your order {order.order_number} has been delivered.",
        ),
        "CANCELLED": (
            "Order Cancelled",
            f"Your order {order.order_number} has been cancelled.",
        ),
    }

    notification_type_map = {
        "PLACED": Notification.NotificationType.ORDER_PLACED,
        "CONFIRMED": Notification.NotificationType.ORDER_CONFIRMED,
        "PROCESSING": Notification.NotificationType.ORDER_PROCESSING,
        "SHIPPED": Notification.NotificationType.ORDER_SHIPPED,
        "DELIVERED": Notification.NotificationType.ORDER_DELIVERED,
        "CANCELLED": Notification.NotificationType.ORDER_CANCELLED,
    }

    title, message = status_messages[order.status]
    notification_type = notification_type_map[order.status]

    # ---------------------------------------------------------
    # 1. Notify the customer
    # ---------------------------------------------------------
    customer_notification = Notification.objects.create(
        user=order.customer,
        order=order,
        title=title,
        message=message,
        notification_type=notification_type,
    )

    send_notification_to_user(
        user=order.customer,
        title=title,
        body=message,
        data={
            "type": "ORDER",
            "order_id": str(order.id),
            "order_number": order.order_number,
            "status": order.status,
            "notification_id": str(customer_notification.id),
        },
    )

    # ---------------------------------------------------------
    # 2. Notify Admin / Super Admin when a new order is placed
    # ---------------------------------------------------------
    if order.status == "PLACED":

        staff_users = User.objects.filter(
            account_type="STAFF",
            role__in=[
                "SUPER_ADMIN",
                "SALES_MANAGER",
            ],
            is_active=True,
        ).exclude(
            id=order.customer_id
        )

        staff_title = "New Order Received"
        staff_message = (
            f"New order {order.order_number} "
            f"has been placed by {order.customer_name}."
        )

        for staff_user in staff_users:

            staff_notification = Notification.objects.create(
                user=staff_user,
                order=order,
                title=staff_title,
                message=staff_message,
                notification_type=Notification.NotificationType.ORDER_PLACED,
            )

            send_notification_to_user(
                user=staff_user,
                title=staff_title,
                body=staff_message,
                data={
                    "type": "ORDER",
                    "order_id": str(order.id),
                    "order_number": order.order_number,
                    "status": order.status,
                    "notification_id": str(
                        staff_notification.id
                    ),
                },
            )

    return customer_notification