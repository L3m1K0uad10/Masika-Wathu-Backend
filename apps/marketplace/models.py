from django.db import models


class Category(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.name


class Lead(models.Model):
    merchant = models.ForeignKey('merchants.MerchantProfile', on_delete = models.CASCADE, related_name='leads')
    buyer_name = models.CharField(max_length = 255, blank = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Lead for {self.merchant.shop_name}"