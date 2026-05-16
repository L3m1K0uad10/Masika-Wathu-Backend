from django.contrib import admin

from .models import (
    Subscription,
    PaymentEvent
)



@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'merchant',
        'plan',
        'amount',
        'status',
        'paid_at',
        'expires_at',
    )

    list_filter = (
        'status',
        'plan',
    )

    search_fields = (
        'merchant__shop_name',
        'tx_ref',
    )


@admin.register(PaymentEvent)
class PaymentEventAdmin(admin.ModelAdmin):
    list_display = (
        'event_type',
        'tx_ref',
        'processing_status',
        'created_at',
    )

    list_filter = (
        'processing_status',
        'event_type',
    )

    search_fields = (
        'tx_ref',
    )

    readonly_fields = (
        'payload',
        'signature',
        'created_at',
    )