"""
Custom permissions for accounts and subscription tiers.
"""
from rest_framework.permissions import BasePermission
from django.utils import timezone


class IsProUser(BasePermission):
    """
    Allows access only to authenticated users with active Pro subscriptions.
    """
    message = "Pro subscription required to access this feature."

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff or request.user.is_superuser:
            return True

        if not request.user.is_pro:
            return False

        if request.user.pro_expires_at and request.user.pro_expires_at < timezone.now():
            return False

        return True
