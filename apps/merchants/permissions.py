from rest_framework import permissions



class IsVerifiedAndSubscribed(permissions.BasePermission):
    """allowing only merchants with verified profiles and active subscriptions to access certain views"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated: 
            return False
        profile = getattr(request.user, 'profile', None)
        
        return bool(profile and profile.verification_status == 'Verified' and profile.is_active_subscription)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """making sure that merchants can only edit their own profile, but anyone can read"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: 
            return True
        
        return obj.user == request.user