from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Создаем класс для проверки является ли пользователь собственником
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsProvider(BasePermission):
    """
    Создаем класс для проверки является ли пользователь поставщиком
    """
    message = "Your type is not a PROVIDER"

    def has_permission(self, request, view):
        return request.user.type == 'PROVIDER'


class IsShop(BasePermission):
    """
    Создаем класс для проверки является ли пользователь магазином
    """
    message = "Your type is not a SHOP"

    def has_permission(self, request, view):
        return request.user.type == 'SHOP'