from rest_framework import serializers

from apps.marketplace.serializers import CategorySerializer
from .models import (
    MerchantProfile,
    ShopImage
)



class ShopImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopImage

        fields = [
            'id', 
            'image', 
            'order'
        ]


class ShopImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopImage
        fields = [
            'id',
            'image',
            'order'
        ]

    def validate_order(self, value):
        """Ensure order is 1, 2, or 3"""
        if value not in [1, 2, 3]:
            raise serializers.ValidationError("Order must be 1, 2, or 3.")
        
        return value
    

class VerificationUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantProfile
        fields = [
            'identity_document'
        ]


class MerchantProfileSerializer(serializers.ModelSerializer):
    images = ShopImageSerializer(many = True, read_only = True)
    categories = CategorySerializer(many = True, read_only = True)
    
    class Meta:
        model = MerchantProfile

        fields = [
            'id', 
            'shop_name', 
            'slug', 
            'description', 
            'phone_number', 
            'location_name', 
            'categories',
            'district', 
            'images', 
            'verification_status',
            'is_active_subscription'
        ]
        read_only_fields = [
            'verification_status', 
            'is_active_subscription',
            'slug'
        ]
