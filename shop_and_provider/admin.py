from django.contrib import admin
from shop_and_provider import models


@admin.register(models.Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


@admin.register(models.Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


class ParameterInfoInline(admin.TabularInline):
    model = models.ParameterInfo
    extra = 0


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_add']
    inlines = [ParameterInfoInline]


@admin.register(models.ProductProvider)
class ProductProviderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'provider',
        'price',
        'status',
        'created_add'
    ]


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'shop']


class OrderPositionInline(admin.TabularInline):
    model = models.OrderPosition
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'manager', 'status', 'created_add']
    list_editable = ['status']
    inlines = [OrderPositionInline]
