from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "admin" and request.user.is_authenticated:
            return True
        return False