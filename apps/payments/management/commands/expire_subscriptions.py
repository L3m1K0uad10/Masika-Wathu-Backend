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
            merchant_profile = subscription.merchant
            merchant_profile.is_active_subscription = False
            merchant_profile.save()

            expired_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Expired subscription: {subscription.tx_ref}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total expired subscriptions: {expired_count}"
            )
        )