import firebase_admin
from firebase_admin import credentials
from django.conf import settings


def initialize_firebase():
    if firebase_admin._apps:
        return firebase_admin.get_app()

    if not all(
        [
            settings.FIREBASE_PROJECT_ID,
            settings.FIREBASE_PRIVATE_KEY,
            settings.FIREBASE_CLIENT_EMAIL,
        ]
    ):
        raise RuntimeError(
            "Firebase credentials are not configured correctly."
        )

    credential = credentials.Certificate(
        {
            "type": "service_account",
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key": settings.FIREBASE_PRIVATE_KEY,
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    )

    return firebase_admin.initialize_app(credential)