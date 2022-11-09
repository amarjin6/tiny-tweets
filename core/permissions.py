from rest_framework.permissions import BasePermission

from core.enums import Role


class IsUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return Role.USER.value in user.role


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return Role.MODERATOR.value in user.role


class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            return Role.MODERATOR.value in user.role or Role.ADMIN.value in user.role
        except Exception as e:
            return False
