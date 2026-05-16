import uuid
import requests
from datetime import timedelta

from django.conf import settings
from django.utils import timezone



def initialize_paychangu_payment(user, amount, plan):
    tx_ref = str(uuid.uuid4())

    url = f"{settings.PAYCHANGU_BASE_URL}/payment"

    headers = {
        "Authorization": f"Bearer {settings.PAYCHANGU_SECRET_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "amount": str(amount),
        "currency": "MWK",
        "tx_ref": tx_ref,
        "email": user.email,
        "first_name": user.username,

        # IMPORTANT for callback and return URLs - should replace later with actual URLs in production, actual ones are for testing purposes
        "callback_url": (
            f"{settings.BACKEND_BASE_URL}"
            "/api/directory/"
        ),

        "return_url": (
            f"{settings.BACKEND_BASE_URL}"
            "/api/directory/"
        ),

        # IMPORTANT for receiving webhook - should replace with actual URL in production
        "webhook_url": (
            f"{settings.BACKEND_BASE_URL}"
            "/api/payments/webhook/"
        ),

        "customization": {
            "title": "Masika Wathu Subscription",
            "description": f"{plan} subscription"
        }
    }

    try:
        response = requests.post(
            url,
            json = payload,
            headers = headers,
            timeout = 30
        )

        response.raise_for_status()

        return response.json(), tx_ref

    except requests.RequestException as e:
        return {"status": "error", "message": str(e)}, tx_ref


def verify_paychangu_transaction(tx_ref):
    url = f"{settings.PAYCHANGU_BASE_URL}/verify-payment/{tx_ref}"

    headers = {
        "Authorization": f"Bearer {settings.PAYCHANGU_SECRET_KEY}",
        "Accept": "application/json",
    }

    try:
        response = requests.get(
            url,
            headers = headers,
            timeout = 30
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
def calculate_subscription_expiry(current_expiry = None, duration_days = 30):
    """
    Calculate the next subscription expiry date.

    If current subscription is still active:
        extend from current expiry.

    Otherwise:
        start from now.
    """

    now = timezone.now()

    if current_expiry and current_expiry > now:
        return current_expiry + timedelta(days = duration_days)

    return now + timedelta(days = duration_days)