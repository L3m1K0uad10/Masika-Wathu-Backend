from rest_framework import serializers

from .models import Subscription



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'id',
            'tx_ref',
            'amount',
            'currency',
            'plan',
            'status',
            'created_at',
        ]

        read_only_fields = [
            'tx_ref',
            'status',
        ]