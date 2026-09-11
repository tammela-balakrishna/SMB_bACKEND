import hashlib
import logging
import secrets
from datetime import timedelta

import resend
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from ..models import OTPVerification

logger = logging.getLogger(__name__)


OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 5
OTP_MAX_ATTEMPTS = 5
OTP_RESEND_COOLDOWN_SECONDS = 60
OTP_IP_LIMIT = 10
OTP_IP_WINDOW_SECONDS = 3600


def generate_otp():
    """
    Generate a cryptographically secure 6-digit OTP.
    """
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp(otp: str) -> str:
    """
    Hash OTP before storing it in the database.
    """
    return hashlib.sha256(
        otp.encode("utf-8")
    ).hexdigest()


def send_otp(
    email: str,
    purpose: str = OTPVerification.Purpose.REGISTRATION,
    ip_address: str | None = None,
):
    """
    Generate, store and email a new OTP using Resend.
    """

    email = email.strip().lower()

    if ip_address:
        ip_key = f"otp-ip:{ip_address}"
        ip_requests = cache.get(ip_key, 0)

        if ip_requests >= OTP_IP_LIMIT:
            raise ValueError(
                "Too many OTP requests. Please try again later."
            )

        cache.set(
            ip_key,
            ip_requests + 1,
            timeout=OTP_IP_WINDOW_SECONDS,
        )

    now = timezone.now()

    # Prevent frequent OTP requests
    recent_otp = (
        OTPVerification.objects
        .filter(
            email=email,
            purpose=purpose,
            created_at__gte=now - timedelta(
                seconds=OTP_RESEND_COOLDOWN_SECONDS
            ),
            is_used=False,
        )
        .first()
    )

    if recent_otp:
        raise ValueError(
            "Please wait before requesting another OTP."
        )

    # Invalidate previous active OTPs
    OTPVerification.objects.filter(
        email=email,
        purpose=purpose,
        is_used=False,
    ).update(
        is_used=True,
    )

    otp = generate_otp()

    otp_record = OTPVerification.objects.create(
        email=email,
        otp_hash=hash_otp(otp),
        purpose=purpose,
        expires_at=now + timedelta(
            minutes=OTP_EXPIRY_MINUTES
        ),
    )

    logger.info(
        "OTP requested for user account",
        extra={
            "email": email,
            "purpose": purpose,
        },
    )

    try:
        resend.api_key = settings.RESEND_API_KEY

        resend.Emails.send(
            {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": [email],
                "subject": "SMB Auto Parts - Verification Code",
                "html": f"""
                    <div>
                        <h2>SMB Auto Parts</h2>

                        <p>Your verification code is:</p>

                        <h1>{otp}</h1>

                        <p>
                            This code will expire in
                            {OTP_EXPIRY_MINUTES} minutes.
                        </p>

                        <p>
                            If you did not request this code,
                            please ignore this email.
                        </p>
                    </div>
                """,
            }
        )

    except Exception:
        otp_record.is_used = True
        otp_record.save(
            update_fields=["is_used"]
        )

        logger.exception(
            "Resend email failed while sending OTP",
            extra={
                "email": email,
                "purpose": purpose,
            },
        )

        raise RuntimeError(
            "Unable to send verification email. "
            "Please try again later."
        )

    return otp_record


def verify_otp(
    email: str,
    otp: str,
    purpose: str,
):
    """
    Verify an OTP securely.
    """

    email = email.strip().lower()
    otp = otp.strip()

    otp_record = (
        OTPVerification.objects
        .filter(
            email=email,
            purpose=purpose,
            is_used=False,
        )
        .order_by("-created_at")
        .first()
    )

    if not otp_record:
        raise ValueError(
            "Invalid or expired OTP."
        )

    if otp_record.is_expired():
        otp_record.is_used = True
        otp_record.save(
            update_fields=["is_used"]
        )

        raise ValueError(
            "OTP has expired."
        )

    if otp_record.attempts >= OTP_MAX_ATTEMPTS:
        otp_record.is_used = True
        otp_record.save(
            update_fields=["is_used"]
        )

        raise ValueError(
            "Maximum OTP attempts exceeded."
        )

    otp_record.attempts += 1

    submitted_hash = hash_otp(otp)

    if not secrets.compare_digest(
        otp_record.otp_hash,
        submitted_hash,
    ):
        otp_record.save(
            update_fields=["attempts"]
        )

        raise ValueError(
            "Invalid OTP."
        )

    otp_record.is_used = True

    otp_record.save(
        update_fields=[
            "attempts",
            "is_used",
        ]
    )

    return True