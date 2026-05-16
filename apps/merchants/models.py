from django.db import models
from django.conf import settings

from django.core.exceptions import ValidationError

from django.utils.text import slugify

from apps.marketplace.models import Category



class MerchantProfile(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'), 
        ('Verified', 'Verified'), 
        ('Rejected', 'Rejected')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'profile')
    shop_name = models.CharField(max_length = 255)
    slug = models.SlugField(unique = True)
    description = models.TextField(blank = True)
    phone_number = models.CharField(max_length = 20, blank = True)
    location_name = models.CharField(max_length = 255, blank = True)
    categories = models.ManyToManyField(Category, related_name = 'merchants', blank = True)
    district = models.CharField(max_length = 255, blank = True)
    
    # Security, status
    identity_document = models.FileField(upload_to = 'private/ids/', null = True, blank = True) 
    verification_status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'Pending')
    is_active_subscription = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.shop_name)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.shop_name


class ShopImage(models.Model):
    merchant = models.ForeignKey(MerchantProfile, on_delete = models.CASCADE, related_name = 'images')
    image = models.ImageField(upload_to = 'shops/')
    order = models.PositiveSmallIntegerField(default = 1) # 1, 2, or 3

    def save(self, *args, **kwargs):
        if not self.pk and self.merchant.images.count() >= 3:
            raise ValidationError("Maximum of 3 images allowed")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.merchant.shop_name} - Image {self.order}"
    