from django.db.models.signals import post_save

from django.dispatch import receiver

from django.conf import settings

from django.utils.text import slugify

from .models import MerchantProfile



@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_merchant_profile(sender, instance, created, **kwargs):

    if created and instance.is_merchant:
        shop_name = f"Shop_{instance.username}"

        MerchantProfile.objects.create(
            user = instance,
            shop_name = shop_name,
            slug = slugify(shop_name)
        )