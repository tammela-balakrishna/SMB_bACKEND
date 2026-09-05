import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from ..models import OTPVerification


OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 5
OTP_MAX_ATTEMPTS = 5
OTP_RESEND_COOLDOWN_SECONDS = 60


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
):
    """
    Generate, store and email a new OTP.
    """

    email = email.strip().lower()

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

    send_mail(
        subject="SMB Auto Parts - Verification Code",
        message=(
            f"Your verification code is: {otp}\n\n"
            f"This code will expire in "
            f"{OTP_EXPIRY_MINUTES} minutes.\n\n"
            "If you did not request this code, "
            "please ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
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