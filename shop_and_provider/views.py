from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from shop_and_provider.models import Provider, Shop, ProductProvider, Order
from shop_and_provider.permissions import IsOwner, IsProvider, IsShop
from shop_and_provider import serializers


class ProviderViewSet(ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = serializers.ProviderSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Устанавливаем разрешения для методов.
        GET может использовать любой пользователь
        POST может использовать только авторизованный пользователь с типом Поставщик
        PATCH и DELETE может использовать только авторизованный пользователь, который создал постащика
        :return:
        """
        if self.request.method == 'GET':
            return []
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsProvider()]
        return [IsAuthenticated(), IsOwner()]


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = serializers.ShopSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Устанавливаем разрешения для методов.
        GET может использовать любой пользователь
        POST может использовать только авторизованный пользователь с типом Магазин
        PATCH и DELETE может использовать только авторизованный пользователь, который создал магазин
        :return:
        """
        if self.request.method == 'GET':
            return []
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsShop()]
        return [IsAuthenticated(), IsOwner()]


class ProductProviderViewSet(ModelViewSet):
    queryset = ProductProvider.objects.all()
    serializer_class = serializers.ProductProviderSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Устанавливаем разрешения для методов.
        GET может использовать любой пользователь
        POST может использовать только авторизованный пользователь с типом Поставщик
        PATCH и DELETE может использовать только авторизованный пользователь, который создал товар
        :return:
        """
        if self.request.method == 'GET':
            return []
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsProvider()]
        return [IsAuthenticated(), IsOwner()]
