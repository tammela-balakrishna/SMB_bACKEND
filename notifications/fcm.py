from firebase_admin import messaging

from .firebase import initialize_firebase
from .models import DeviceToken


def send_push_notification(device_token, title, body, data=None):
    initialize_firebase()

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        token=device_token,
    )

    return messaging.send(message)


def send_notification_to_user(user, title, body, data=None):
    device_tokens = DeviceToken.objects.filter(
        user=user,
        is_active=True,
    )

    results = []

    for device_token in device_tokens:
        try:
            message_id = send_push_notification(
                device_token=device_token.token,
                title=title,
                body=body,
                data=data,
            )

            results.append({
                "token_id": device_token.id,
                "success": True,
                "message_id": message_id,
            })

        except Exception as exc:
            results.append({
                "token_id": device_token.id,
                "success": False,
                "error": str(exc),
            })

    return results