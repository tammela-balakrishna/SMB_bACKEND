from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    SendOTPView,
    VerifyOTPView,
    CustomerRegisterView,
    MeView,
    LogoutView,
    StaffCreateView,
    StaffLoginView,
    StaffActivateView,
)

app_name = "accounts"

urlpatterns = [
    path(
        "register/",
        CustomerRegisterView.as_view(),
        name="register",
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
    path(
        "me/",
        MeView.as_view(),
        name="me",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),path(
    "logout/",
    LogoutView.as_view(),
    name="logout",
),
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
]