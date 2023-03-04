from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from shop_and_provider.models import Provider, Shop
from shop_and_provider.permissions import IsOwner
from shop_and_provider.serializers import ProviderSerializer, ShopSerializer


class ProviderViewSet(ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Устанавливаем разрешения для методов.
        GET может использовать любой пользователь
        POST может использовать только авторизованный пользователь
        PATCH и DELETE может использовать только авторизованный пользователь, который создал постащика
        :return:
        """
        if self.request.method == 'GET':
            return []
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOwner()]


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Устанавливаем разрешения для методов.
        GET может использовать любой пользователь
        POST может использовать только авторизованный пользователь
        PATCH и DELETE может использовать только авторизованный пользователь, который создал магазин
        :return:
        """
        if self.request.method == 'GET':
            return []
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOwner()]
