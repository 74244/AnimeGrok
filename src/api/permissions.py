from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffAdminOrReadOnly(BasePermission):
    """CRUD доступно стаффу, чтение доступно всем """

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or 
            request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
                obj.user.is_authenticated and request.user.is_staff and request.user == obj.user)
    
