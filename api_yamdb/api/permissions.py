from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка доступа по роли admin."""

    def has_permission(self, request, view):
        return request.user.is_admin()


class CheckUser(permissions.BasePermission):
    """Проверка доступа по пользователю."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj
