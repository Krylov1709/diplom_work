from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin
from shop_and_provider import models
from shop_and_provider.models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    model = User
    fieldsets = (("User", {"fields": ("type",)}),) + auth.admin.UserAdmin.fieldsets
    list_display = ['id', 'username', 'email', 'type', 'is_active']


@admin.register(models.Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'company', 'state']


@admin.register(models.Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class ParameterInfoInline(admin.TabularInline):
    model = models.ParameterInfo
    extra = 0


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category']
    inlines = [ParameterInfoInline]


@admin.register(models.ProductProvider)
class ProductProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'provider', 'price']


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'company']


class OrderPositionInline(admin.TabularInline):
    model = models.OrderPosition
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'shop', 'status', 'created_add', 'update_add']
    list_editable = ['status']
    inlines = [OrderPositionInline]
