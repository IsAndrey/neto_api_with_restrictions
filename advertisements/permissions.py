from rest_framework.permissions import BasePermission, IsAdminUser


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        for attr in ['creator', 'user']:
            if hasattr(obj, attr) and request.user == getattr(obj, attr):
                return True
        return False


class IsAdminOROwner(IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return IsOwnerPermission.has_object_permission(self, request, view, obj)