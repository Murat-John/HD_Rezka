from rest_framework.permissions import BasePermission


class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user


class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
