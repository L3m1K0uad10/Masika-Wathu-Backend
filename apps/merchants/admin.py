from django.contrib import admin
from apps.merchants.models import MerchantProfile, ShopImage



class ShopImageInline(admin.TabularInline):
    """Inline admin interface for managing shop images directly from the merchant profile page."""
    model = ShopImage 
    extra = 0

@admin.register(MerchantProfile)
class MerchantProfileAdmin(admin.ModelAdmin):
    list_display = (
        'shop_name', 
        'user', 
        'verification_status', 
        'is_active_subscription'
    )

    search_fields = (
        'shop_name', 
        'user__username', 
        'user__email'
    )

    list_filter = (
        'verification_status', 
        'is_active_subscription'
    )

    inlines = [ShopImageInline]

    filter_horizontal = ('categories',) # gives a better interface for managing many-to-many relationships with categories

@admin.register(ShopImage)
class ShopImageAdmin(admin.ModelAdmin):
    list_display = (
        'merchant', 
        'order'
    )

    list_filter = ('merchant',)