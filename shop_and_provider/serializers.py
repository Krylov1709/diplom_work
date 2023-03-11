from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shop_and_provider import models


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Provider
        fields = ['id', 'user', 'title', 'company', 'state']
        read_only = ['user']


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Shop
        fields = ['id', 'user', 'title', 'company']
        read_only = ['user']


class ProductProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductProvider
        fields = ['id', 'provider', 'product', 'price']
        read_only = ['user']

    def create(self, validated_data):
        """
        Проверяем может ли пользователь создавать товар от имени поставщика.
        id пользователя и id создателя поставщика должны совпадать
        :param validated_data:
        :return:
        """
        provider = models.Provider.objects.get(id=validated_data['provider'].id)
        if provider.user.id != validated_data['user'].id:
            raise ValidationError('You cannot create a product on behalf of this provider')
        return super().create(validated_data)
