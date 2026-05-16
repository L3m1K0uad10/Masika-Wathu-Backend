from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import (
    Category,
    Lead 
)
from apps.merchants.models import MerchantProfile
from .serializers import CategorySerializer



class CategoryListView(generics.ListAPIView):
    """Endpoint to list all categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ContactClickView(generics.CreateAPIView):
    """Endpoint to create a lead when contact button is clicked on merchant profile"""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """overide post method to create a lead when contact button is clicked on merchant profile"""
        merchant_id = kwargs.get('id')
        try:
            merchant = MerchantProfile.objects.get(id = merchant_id)
        except MerchantProfile.DoesNotExist:
            return Response({"error": "Merchant not found"}, status = status.HTTP_404_NOT_FOUND)

        Lead.objects.create(
            merchant = merchant,
            buyer_name = request.data.get('buyer_name', '')
        )

        return Response({"message": "Lead recorded"}, status = status.HTTP_201_CREATED)