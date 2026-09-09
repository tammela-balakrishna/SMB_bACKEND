from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase
from rest_framework import serializers

from .models import OTPVerification, User
from .serializers import StaffManagementSerializer
from .services.otp_service import (
	OTP_IP_LIMIT,
	send_otp,
)


class StaffManagementSerializerTests(TestCase):
	def test_valid_staff_role_uses_user_role_choices(self):
		serializer = StaffManagementSerializer()

		self.assertEqual(
			serializer.validate_role(User.Role.SALES_MANAGER),
			User.Role.SALES_MANAGER,
		)

	def test_invalid_staff_role_is_rejected(self):
		serializer = StaffManagementSerializer()

		with self.assertRaises(serializers.ValidationError):
			serializer.validate_role("NOT_A_ROLE")


class OTPThrottleTests(TestCase):
	def setUp(self):
		cache.clear()

	def tearDown(self):
		cache.clear()

	@patch("accounts.services.otp_service.send_mail")
	def test_otp_requests_are_limited_per_ip(self, send_mail):
		for request_number in range(OTP_IP_LIMIT):
			send_otp(
				email=f"user{request_number}@example.com",
				purpose=OTPVerification.Purpose.REGISTRATION,
				ip_address="192.0.2.10",
			)

		with self.assertRaisesMessage(
			ValueError,
			"Too many OTP requests",
		):
			send_otp(
				email="another@example.com",
				purpose=OTPVerification.Purpose.REGISTRATION,
				ip_address="192.0.2.10",
			)

		self.assertEqual(send_mail.call_count, OTP_IP_LIMIT)

	@patch("accounts.services.otp_service.send_mail")
	def test_otp_send_failure_raises_clear_error(self, send_mail):
		send_mail.side_effect = RuntimeError("SMTP authentication failed")

		with self.assertRaisesRegex(RuntimeError, "SMTP send failed"):
			send_otp(
				email="user@example.com",
				purpose=OTPVerification.Purpose.PASSWORD_RESET,
			)
