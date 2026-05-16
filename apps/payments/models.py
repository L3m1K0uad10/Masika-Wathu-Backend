from django.db import models


class Subscription(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    )

    PLAN_CHOICES = (
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    )

    merchant = models.ForeignKey('merchants.MerchantProfile', on_delete = models.CASCADE, related_name = 'subscriptions')
    tx_ref = models.CharField(max_length = 255, unique = True) # transaction reference
    paychangu_reference = models.CharField(max_length = 255, blank = True, null = True)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    currency = models.CharField(max_length = 10, default = 'MWK')
    plan = models.CharField(max_length = 20,choices = PLAN_CHOICES, default = 'basic')
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default = 'pending')
    paid_at = models.DateTimeField(blank = True, null = True)
    expires_at = models.DateTimeField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.merchant.shop_name} - {self.status}"
    

class PaymentEvent(models.Model):
    EVENT_STATUS_CHOICES = (
        ('received', 'Received'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    )

    event_id = models.CharField(
        max_length = 255,
        unique = True,
        blank = True,
        null = True
    )

    event_type = models.CharField(max_length = 100)
    tx_ref = models.CharField(max_length = 255, blank = True, null = True)
    payload = models.JSONField()
    signature = models.CharField(max_length = 500)
    processing_status = models.CharField(
        max_length = 20,
        choices = EVENT_STATUS_CHOICES,
        default = 'received'
    )
    error_message = models.TextField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.event_type} - {self.processing_status}"