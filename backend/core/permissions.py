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
