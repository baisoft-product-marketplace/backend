from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Business, Product, MarketplaceProfile

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'status', 'created_by', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'business__name')

@admin.register(MarketplaceProfile)
class MarketplaceProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business')
    search_fields = ('user__username', 'business__name')

