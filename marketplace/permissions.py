from rest_framework.permissions import BasePermission


class CanApproveProduct(BasePermission):
    """
    Only admins and approvers are allowed
    to approve products.
    """

    def has_permission(self, request, view):
        return request.user.role in ['admin', 'approver']
