from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Создаем класс для проверки является ли пользователь собственником
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
