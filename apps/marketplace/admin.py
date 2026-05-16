from django.contrib import admin

from .models import (
    Category,
    Lead
)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

    prepopulated_fields = {
        'slug': ('name',)
    }

    search_fields = ('name',)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('merchant', 'buyer_name', 'timestamp')

    search_fields = ('merchant__shop_name', 'buyer_name')

    list_filter = ('timestamp',)