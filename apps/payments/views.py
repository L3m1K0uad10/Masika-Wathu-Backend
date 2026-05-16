import json
import hmac
import hashlib
import logging

from decimal import Decimal

from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Subscription,
    PaymentEvent
)
from .services import (
    initialize_paychangu_payment, 
    verify_paychangu_transaction,
    calculate_subscription_expiry
)



logger = logging.getLogger(__name__)

class InitializePaymentView(APIView):
    """Endpoint for merchants to initialize a PayChangu payment for their subscription."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        merchant_profile = request.user.profile
        plan = request.data.get('plan', 'basic')
        amount = Decimal("10000.00") # using decimal for money values
        paychangu_response, tx_ref = initialize_paychangu_payment(
            request.user,
            amount,
            plan
        )

        # Only create subscription if initialization succeeded
        if paychangu_response.get("status") != "success":
            return Response(
                {
                    "error": "Payment initialization failed",
                    "paychangu_response": paychangu_response
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Creating pending subscription
        subscription = Subscription.objects.create(
            merchant = merchant_profile,
            tx_ref = tx_ref,
            amount = amount,
            plan = plan,
            status = "pending"
        )

        logger.info(
            f"Subscription created with tx_ref: {tx_ref}"
        )

        return Response({
            "subscription_id": subscription.id,
            "payment_data": paychangu_response,
        }, status = status.HTTP_201_CREATED)
    

@method_decorator(csrf_exempt, name='dispatch')
class PayChanguWebhookView(APIView):
    """Endpoint to receive PayChangu webhook notifications about payment events."""
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        raw_body = request.body.decode('utf-8')
        
        # getting signature
        signature = request.headers.get('Signature') or request.headers.get('paychangu-signature')
        if not signature:
            logger.warning("Missing webhook signature")
            return Response({"error": "Missing signature"}, status = status.HTTP_400_BAD_REQUEST)

        # verifying signature
        computed_signature = hmac.new(
            key = settings.PAYCHANGU_WEBHOOK_SECRET.encode('utf-8'),
            msg = request.body,
            digestmod = hashlib.sha256
        ).hexdigest()

        # comparing signatures securely
        if not hmac.compare_digest(signature, computed_signature):
            logger.warning("Invalid webhook signature")

            PaymentEvent.objects.create(
                event_type="invalid_signature",
                payload={"raw_body": raw_body},
                signature=signature,
                processing_status="failed",
                error_message="Invalid webhook signature"
            )
            return Response({"error": "Invalid signature"}, status = status.HTTP_403_FORBIDDEN)
        
        logger.info("SIGNATURE VERIFIED SUCCESSFULLY")
        
        # parsing payload
        try:
            payload = json.loads(raw_body)
            event_type = payload.get("event", "unknown")
            event_id = payload.get("reference") or tx_ref # generating a reliable idempotency key

            existing_event = PaymentEvent.objects.filter(
                event_id = event_id,
                processing_status = 'processed'
            ).exists()

            if existing_event:
                return Response({"message": "Duplicate webhook ignored"}, status = 200)

            payment_event = PaymentEvent.objects.create(
                event_type = event_type,
                tx_ref = payload.get("tx_ref") or payload.get("data", {}).get("tx_ref"),
                payload = payload,
                signature = signature,
                processing_status = 'received'
            )
        except json.JSONDecodeError:
            logger.error("Invalid JSON payload")
            return Response({"error": "Invalid JSON"}, status = status.HTTP_400_BAD_REQUEST)

        logger.info(f"Webhook Payload: {payload}")

        tx_ref = payload.get("tx_ref") or payload.get("data", {}).get("tx_ref")
        
        if not tx_ref:
            logger.warning("Missing tx_ref in payload")
            return Response({"error": "Missing tx_ref"}, status = status.HTTP_400_BAD_REQUEST)
        
        logger.info(f"Webhook received for tx_ref: {tx_ref}")

        # verification logic (Handling Dashboard Test vs Real Payment)
        is_test_mode = payload.get("mode") == "test"

        payment_status = None
        paychangu_reference = None
        
        # REAL PAYMENT FLOW
        if not is_test_mode:
            logger.info(
                f"Verifying payment with PayChangu for tx_ref: {tx_ref}"
            )

            # only call verify_paychangu_transaction for REAL payments
            verification_response = verify_paychangu_transaction(tx_ref)
            verification_data = verification_response.get("data", {})
            payment_status = verification_data.get("status")
            paychangu_reference = verification_data.get("reference")
        
        # DASHBOARD TEST FLOW
        else:
            logger.info(
                "Dashboard Test detected: "
                "Skipping external API verification."
            )

            payment_status = payload.get("status")
            paychangu_reference = payload.get("reference")

        # Only process successful payments
        # database update logic
        if payment_status == "success":
            try:
                subscription = Subscription.objects.get(tx_ref = tx_ref)
            except Subscription.DoesNotExist:
                logger.error(
                    f"Subscription not found for tx_ref: {tx_ref}"
                )

                payment_event.processing_status = "failed"
                payment_event.error_message = "Subscription not found"
                payment_event.save()

                return Response({"error": "Subscription not found"}, status = status.HTTP_404_NOT_FOUND)

                
            # Idempotent Protection: Only update if not already marked as paid to prevent duplicate processing: VERY IMPORTANT IN PAYMENT SYSTEM
            if subscription.status == "paid":
                logger.info(
                    f"Subscription already processed for tx_ref: {tx_ref}"
                )

                payment_event.processing_status = "processed"
                payment_event.error_message = "Duplicate webhook ignored"
                payment_event.save()

                return Response({"message": "Already processed"}, status = status.HTTP_200_OK)
                                
            # Updating subscription
            subscription.status = "paid"
            subscription.paychangu_reference = paychangu_reference
            subscription.paid_at = timezone.now()
            subscription.expires_at = calculate_subscription_expiry(
                current_expiry = subscription.expires_at,
                duration_days = 30
            )
            subscription.save()

            logger.info(
                f"Subscription updated to PAID for tx_ref: {tx_ref}"
            )

            # Activating merchant subscription
            merchant_profile = subscription.merchant
            merchant_profile.is_active_subscription = True
            merchant_profile.save()

            payment_event.processing_status = "processed"
            payment_event.save()

            logger.info(
                f"Merchant subscription activated "
                f"for merchant ID: {merchant_profile.id}"
            )

            return Response({"message": "Webhook processed successfully"}, status = status.HTTP_200_OK)

        logger.warning(
            f"Payment status is not successful. "
            f"Status received: {payment_status}"
        )

        return Response(
            {
                "message": (
                    f"Payment status is {payment_status}"
                )
            },
            status=status.HTTP_200_OK
        )