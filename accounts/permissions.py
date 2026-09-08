from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    message = "Staff access is required."

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and user.account_type == "STAFF"
            and user.is_active
            and user.is_verified
        )


class IsSuperAdmin(BasePermission):
    message = "Only Super Admin can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and user.account_type == "STAFF"
            and user.role == "SUPER_ADMIN"
            and user.is_active
            and user.is_verified
        )


class IsInventoryManager(BasePermission):
    message = "Only Inventory Manager can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and user.account_type == "STAFF"
            and user.role == "INVENTORY_MANAGER"
            and user.is_active
            and user.is_verified
        )


class IsSalesManager(BasePermission):
    message = "Only Sales Manager can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and user.account_type == "STAFF"
            and user.role == "SALES_MANAGER"
            and user.is_active
            and user.is_verified
        )


class IsOrderManager(BasePermission):
    message = "Only Sales Manager or Super Admin can manage orders."

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and user.account_type == "STAFF"
            and user.role in {
                "SALES_MANAGER",
                "SUPER_ADMIN",
            }
            and user.is_active
            and user.is_verified
        )


class IsInventoryManagerOrReadOnly(BasePermission):
    message = "Only Inventory Manager or Super Admin can change inventory."

    def has_permission(self, request, view):
        user = request.user

        if not (
            user
            and user.is_authenticated
            and user.is_active
            and user.is_verified
        ):
            return False

        if request.method in {
            "GET",
            "HEAD",
            "OPTIONS",
        }:
            return True

        return (
            user.account_type == "STAFF"
            and user.role in {
                "INVENTORY_MANAGER",
                "SUPER_ADMIN",
            }
        )