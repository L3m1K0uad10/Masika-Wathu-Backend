from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from .models import (
    MerchantProfile,
    ShopImage
)
from apps.marketplace.models import Lead
from .serializers import (
    MerchantProfileSerializer,
    ShopImageUploadSerializer,
    VerificationUploadSerializer
)
from apps.payments.permissions import HasActiveSubscription



class DirectoryListView(generics.ListAPIView):
    """Endpoint to list all verified merchants with active subscriptions, with optional filtering by district."""
    serializer_class = MerchantProfileSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['district']

    def get_queryset(self):
        return MerchantProfile.objects.filter(
            verification_status = 'Verified',
            is_active_subscription = True
        )


class DirectoryDetailView(generics.RetrieveAPIView):
    """Endpoint to retrieve details of a specific merchant by slug, only if they are verified and have an active subscription."""
    serializer_class = MerchantProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    queryset = MerchantProfile.objects.filter(
        verification_status = 'Verified',
        is_active_subscription = True
    )


class MerchantProfileView(generics.RetrieveUpdateAPIView):
    """Endpoint for merchants to view and update their own profile. Only accessible to authenticated users."""
    serializer_class = MerchantProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    

class MerchantImageUploadView(generics.CreateAPIView):
    """
        Endpoint for merchants to upload images for their shop. 
        Enforces a maximum of 3 images per merchant and validates the order field.
        This is a premium/public feature. so added HasActiveSubscription
    """
    serializer_class = ShopImageUploadSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscription]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(merchant = self.request.user.profile)


class VerificationUploadView(generics.UpdateAPIView):
    """
        Endpoint for merchants to upload identity documents for verification. 
        Only accessible to authenticated users 
        This does not require payment, verification is before monetization
    """
    serializer_class = VerificationUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user.profile
    

class MerchantStatsView(generics.GenericAPIView):
    """
        Endpoint for merchants to view statistics about their profile, 
        such as total leads. Only accessible to authenticated users.
        This is a premium/public feature, so added HasActiveSubscription
    """
    permission_classes = [IsAuthenticated, HasActiveSubscription]

    def get(self, request):
        """override get method to retrieve statistics about the merchant profile, such as total leads"""
        profile = request.user.profile
        total_leads = Lead.objects.filter(merchant = profile).count()

        return Response({
            "shop_name": profile.shop_name,
            "total_leads": total_leads
        })