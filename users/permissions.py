from rest_framework.permissions import BasePermission
from users.models import User


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )


class CanApproveProduct(BasePermission):
    """
    Allows admins and approvers to approve products.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in {
                User.Role.ADMIN,
                User.Role.APPROVER,
            }
        )


class CanEditProduct(BasePermission):
    """
    Allows admins and editors to create or edit products.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in {
                User.Role.ADMIN,
                User.Role.EDITOR,
            }
        )
