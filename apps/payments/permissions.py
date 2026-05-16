from rest_framework.permissions import BasePermission



class HasActiveSubscription(BasePermission):
    """
    Allowing access only to merchants
    with active subscriptions.
    """

    message = "An active subscription is required."

    def has_permission(self, request, view):
        user = request.user

        # must be authenticated
        if not user or not user.is_authenticated:
            return False

        # must have merchant profile
        if not hasattr(user, "profile"):
            return False

        merchant_profile = user.profile

        return merchant_profile.is_active_subscription