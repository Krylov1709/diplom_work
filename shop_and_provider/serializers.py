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

    def update(self, instance, validated_data):
        """
        Устанавливаем ограничение на изменение поставщика в товаре и самого товара
        :param instance:
        :param validated_data:
        :return:
        """
        if 'provider' in validated_data or 'product' in validated_data:
            raise ValidationError('Provider and product change is not possible')
        return super().update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id', 'user', 'shop', 'status', 'products_provider']
        read_only = ['user', 'products_provider']

    def create(self, validated_data):
        """
        Проверяем может ли пользователь создавать заказ от имени магазина.
        id пользователя и id создателя магазина должны совпадать
        :param validated_data:
        :return:
        """
        shop = models.Shop.objects.get(id=validated_data['shop'].id)
        if shop.user.id != validated_data['user'].id:
            raise ValidationError('You cannot create a order on behalf of this shop')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Устанавливаем ограничение на изменение магазина в заказе
        :param instance:
        :param validated_data:
        :return:
        """
        if 'shop' in validated_data:
            raise ValidationError('Shop change is not possible')
        return super().update(instance, validated_data)


class OrderPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderPosition
        fields = ['id', 'order', 'product_provider', 'quantity']
        read_only = ['user']

    def create(self, validated_data):
        """
        Проверяем может ли пользователь добавлять товары в заказ.
        id пользователя и id создателя заказа должны совпадать
        :param validated_data:
        :return:
        """
        # Проверяем является пользователь создателем заказа
        order = models.Order.objects.get(id=validated_data['order'].id)
        if order.user.id != validated_data['user'].id:
            raise ValidationError('You can only add products to your own order')
        # Проверяем может ли поставщик товара принимать заказы
        product_provider = models.ProductProvider.objects.get(id=validated_data['product_provider'].id)
        if product_provider.provider.state is not True:
            raise ValidationError('The provider of this product does not accept orders')
        # Проверяем нет ли уже такого товара в заказе
        order_positions = models.OrderPosition.objects.filter(order=validated_data['order'].id)
        for position in order_positions:
            if validated_data['product_provider'] == position.product_provider:
                raise ValidationError(
                    f'The order already contains such a product in quantity {position.quantity}'
                )
        # удаляем пользователя что бы не вносить в БД
        del validated_data['user']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Устанавливаем ограничение на изменение колличества товара в заказе
        :param instance:
        :param validated_data:
        :return:
        """
        if instance.order.user.id != validated_data['user'].id:
            raise ValidationError('Quantity can only be changed by the owner of the order')
        del validated_data['user']
        if 'order' in validated_data or 'product_provider' in validated_data:
            raise ValidationError('Order and product change is not possible')
        return super().update(instance, validated_data)
