from django.contrib import admin
from apps.users.models import User



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_merchant', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')