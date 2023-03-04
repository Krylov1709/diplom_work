from rest_framework import serializers
from shop_and_provider.models import Provider, Shop


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ['id', 'title', 'company', 'email', 'created_add']
        read_only = ['user']


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ['id', 'title', 'company', 'email', 'created_add']
        read_only = ['user']

