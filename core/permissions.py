from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.request import Request


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff and request.user.is_superuser)


class IsAdminOrWriteOnly(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method == 'POST':
            return True
        return bool(request.user.is_staff)


class IsAdminWriteOrIsAuthenticatedRead(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method == 'GET':
            return bool(request.user)
        return bool(request.user and request.user.is_staff)
