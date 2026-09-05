from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperAdmin
from .models import OTPVerification
from .serializers import (
    SendOTPSerializer,
    VerifyOTPSerializer,
    CustomerRegisterSerializer,
    StaffCreateSerializer,
    StaffLoginSerializer,
    StaffActivateSerializer,
)
from .services.otp_service import (
    send_otp,
    verify_otp,
)

User = get_user_model()
class CustomerRegisterView(APIView):
    """
    Create a customer account.

    Registration itself does not mark the customer
    as verified. Email OTP verification does that.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = CustomerRegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]

        if User.objects.filter(
            email=email
        ).exists():

            return Response(
                {
                    "success": False,
                    "message": "An account with this email already exists.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            email=email,
            first_name=serializer.validated_data[
                "first_name"
            ],
            last_name=serializer.validated_data.get(
                "last_name",
                "",
            ),
            account_type=User.AccountType.CUSTOMER,
            role=None,
            is_staff=False,
            is_superuser=False,
            is_verified=False,
        )

        return Response(
            {
                "success": True,
                "message": "Customer registered successfully. Please verify your email.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "account_type": user.account_type,
                    "is_verified": user.is_verified,
                },
            },
            status=status.HTTP_201_CREATED,
        )

class StaffCreateView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin,
    ]

    def post(self, request):
        serializer = StaffCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            email=serializer.validated_data["email"],
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data.get(
                "last_name",
                "",
            ),
            account_type=User.AccountType.STAFF,
            role=serializer.validated_data["role"],
            is_staff=False,
            is_superuser=False,
            is_verified=False,
        )

        return Response(
            {
                "success": True,
                "message": "Staff account created successfully.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "account_type": user.account_type,
                    "role": user.role,
                    "is_verified": user.is_verified,
                },
            },
            status=status.HTTP_201_CREATED,
        )
class SendOTPView(APIView):
    """
    Send OTP to an email address.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = SendOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]
        purpose = serializer.validated_data["purpose"]

        try:
            send_otp(
                email=email,
                purpose=purpose,
            )

        except ValueError as exc:
            return Response(
                {
                    "success": False,
                    "message": str(exc),
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        return Response(
            {
                "success": True,
                "message": "OTP sent successfully.",
            },
            status=status.HTTP_200_OK,
        )
class StaffLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = StaffLoginSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(
            request=request,
            email=email,
            password=password,
        )

        if user is None:
            return Response(
                {
                    "success": False,
                    "message": "Invalid email or password.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if user.account_type != User.AccountType.STAFF:
            return Response(
                {
                    "success": False,
                    "message": "Staff login is only available for staff accounts.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if not user.is_active:
            return Response(
                {
                    "success": False,
                    "message": "This staff account is inactive.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if not user.is_verified:
            return Response(
                {
                    "success": False,
                    "message": "Staff email is not verified.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "success": True,
                "message": "Staff login successful.",
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "account_type": user.account_type,
                    "role": user.role,
                    "is_verified": user.is_verified,
                },
            },
            status=status.HTTP_200_OK,
        ) 
class VerifyOTPView(APIView):
    """
    Verify customer registration OTP and issue JWT tokens.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = VerifyOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        purpose = serializer.validated_data["purpose"]

        try:
            verify_otp(
                email=email,
                otp=otp,
                purpose=purpose,
            )

        except ValueError as exc:
            return Response(
                {
                    "success": False,
                    "message": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Registration OTP
        if purpose == "REGISTRATION":

            try:
                user = User.objects.get(
                    email=email,
                    account_type=User.AccountType.CUSTOMER,
                )
            except User.DoesNotExist:
                return Response(
                    {
                        "success": False,
                        "message": "Customer registration not found.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            user.is_verified = True
            user.is_active = True

            user.save(
                update_fields=[
                    "is_verified",
                    "is_active",
                    "updated_at",
                ]
            )

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "success": True,
                    "message": "Email verified successfully.",
                    "tokens": {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    },
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "account_type": user.account_type,
                        "role": user.role,
                        "is_verified": user.is_verified,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "success": True,
                "message": "OTP verified successfully.",
            },
            status=status.HTTP_200_OK,
        )
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response(
            {
                "success": True,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "account_type": user.account_type,
                    "role": user.role,
                    "is_verified": user.is_verified,
                },
            },
            status=status.HTTP_200_OK,
        )
class StaffActivateView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = StaffActivateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(
                email=email,
                account_type=User.AccountType.STAFF,
            )
        except User.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Staff account not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.is_verified:
            return Response(
                {
                    "success": False,
                    "message": "Staff account is already activated.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            verify_otp(
                email=email,
                otp=otp,
                purpose=OTPVerification.Purpose.EMAIL_VERIFY,
            )
        except ValueError as exc:
            return Response(
                {
                    "success": False,
                    "message": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(password)
        user.is_verified = True
        user.is_active = True

        user.save(
            update_fields=[
                "password",
                "is_verified",
                "is_active",
                "updated_at",
            ]
        )

        return Response(
            {
                "success": True,
                "message": "Staff account activated successfully.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "account_type": user.account_type,
                    "role": user.role,
                    "is_verified": user.is_verified,
                },
            },
            status=status.HTTP_200_OK,
        )
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {
                    "success": False,
                    "message": "Refresh token is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except Exception:
            return Response(
                {
                    "success": False,
                    "message": "Invalid or already blacklisted refresh token.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "message": "Logged out successfully.",
            },
            status=status.HTTP_200_OK,
        )