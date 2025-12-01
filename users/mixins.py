from rest_framework import permissions
from .permissions import IsAdmin

class ReadOnlyOrIsAdminMixin:
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsAdmin()]