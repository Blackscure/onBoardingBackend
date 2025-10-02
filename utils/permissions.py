from rest_framework import permissions

class IsAuthenticatedUser(permissions.BasePermission):
    """
    Custom permission to allow access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated