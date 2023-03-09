from rest_framework import serializers
from shop_and_provider import models


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Provider
        fields = ['id', 'title', 'company', 'created_add']
        read_only = ['user']


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Shop
        fields = ['id', 'title', 'company', 'created_add']
        read_only = ['user']


