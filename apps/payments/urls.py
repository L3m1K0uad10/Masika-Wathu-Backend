from django.urls import path

from .views import (
    InitializePaymentView,
    PayChanguWebhookView
)



urlpatterns = [
    path('payments/initialize/', InitializePaymentView.as_view(), name = 'initialize-payment'),
    path('payments/webhook/', PayChanguWebhookView.as_view(), name = 'paychangu-webhook'),
]