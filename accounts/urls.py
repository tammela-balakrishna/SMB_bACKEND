from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    SendOTPView,
    VerifyOTPView,
    CustomerRegisterView,
    CustomerLoginView,
    MeView,
    LogoutView,
    StaffCreateView,
    StaffLoginView,
    StaffActivateView,
    StaffDetailView,
    ForgotPasswordView,
    ResetPasswordView,
)

app_name = "accounts"

urlpatterns = [
    # ============================================================
    # CUSTOMER AUTHENTICATION
    # ============================================================

    path(
        "register/",
        CustomerRegisterView.as_view(),
        name="register",
    ),

    path(
        "customer/login/",
        CustomerLoginView.as_view(),
        name="customer-login",
    ),

    path(
        "send-otp/",
        SendOTPView.as_view(),
        name="send-otp",
    ),

    path(
        "verify-otp/",
        VerifyOTPView.as_view(),
        name="verify-otp",
    ),

    # ============================================================
    # CURRENT USER
    # ============================================================

    path(
        "me/",
        MeView.as_view(),
        name="me",
    ),

    # ============================================================
    # TOKEN
    # ============================================================

    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
    path(
    "forgot-password/",
    ForgotPasswordView.as_view(),
    name="forgot-password",
),

    path(
        "reset-password/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),

    # ============================================================
    # LOGOUT
    # ============================================================

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # ============================================================
    # STAFF
    # ============================================================

    path(
        "staff/",
        StaffCreateView.as_view(),
        name="staff-create",
    ),

    path(
        "staff/login/",
        StaffLoginView.as_view(),
        name="staff-login",
    ),

    path(
        "staff/activate/",
        StaffActivateView.as_view(),
        name="staff-activate",
    ),

    path(
        "staff/<int:pk>/",
        StaffDetailView.as_view(),
        name="staff-detail",
    ),
]