from .fcm import send_notification_to_user
from .models import Notification


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

    notification = Notification.objects.create(
        user=order.customer,
        order=order,
        title=title,
        message=message,
        notification_type=notification_type_map[order.status],
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
            "notification_id": str(notification.id),
        },
    )

    return notification