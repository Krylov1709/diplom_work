from rest_framework.permissions import BasePermission
from shop_and_provider import models


class IsOwner(BasePermission):
    """
    Проверяяем является ли пользователь создателем
    """
    message = "Only the creator can change"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsProvider(BasePermission):
    """
    Проверяем является ли пользователь поставщиком
    """
    message = "Your type is not a PROVIDER"

    def has_permission(self, request, view):
        return request.user.type == 'PROVIDER'


class IsShop(BasePermission):
    """
    Проверяем является ли пользователь магазином
    """
    message = "Your type is not a SHOP"

    def has_permission(self, request, view):
        return request.user.type == 'SHOP'


class IsOwnerOrder(BasePermission):
    """
    Проверяяем является ли пользователь создателем заказа
    """
    message = "Only the creator order can change"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.order.user
