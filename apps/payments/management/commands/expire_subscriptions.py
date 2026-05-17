from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.payments.models import Subscription



class Command(BaseCommand):
    help = "Expire outdated subscriptions and deactivate merchants"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        expired_subscriptions = Subscription.objects.filter(
            status = "paid",
            expires_at__lt = now
        )

        expired_count = 0

        for subscription in expired_subscriptions:
            # marking subscription expired
            subscription.status = "expired"
            subscription.save()

            # deactivating merchant
            # checking if merchant still has another active subscription
            merchant_profile = subscription.merchant

            has_active_subscription = Subscription.objects.filter(
                merchant = merchant_profile,
                status = "paid",
                expires_at__gt = now
            ).exclude(id = subscription.id).exists()

            # deactivate only if no active subscription remains
            if not has_active_subscription:
                merchant_profile.is_active_subscription = False
                merchant_profile.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Expired subscription: {subscription.tx_ref}"
                )
            )