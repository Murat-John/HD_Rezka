from rest_framework.permissions import BasePermission


class IsUserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.email == request.user.email
