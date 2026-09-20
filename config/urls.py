from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "privacy-policy/",
        TemplateView.as_view(template_name="privacy_policy.html"),
        name="privacy_policy",
    ),

    # Authentication
    path(
        "api/v1/auth/",
        include("accounts.urls"),
    ),

    # Vehicles
    path(
        "api/v1/vehicles/",
        include("vehicles.urls"),
    ),

    # Products
    path(
        "api/v1/products/",
        include("products.urls"),
    ),

    # Orders
    path(
        "api/v1/orders/",
        include("orders.urls"),
    ),

    # Addresses
    path(
        "api/v1/addresses/",
        include("addresses.urls"),
    ),

    # Notifications
    path(
        "api/v1/notifications/",
        include("notifications.urls"),
    ),
]