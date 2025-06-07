from rest_framework import permissions

class IsSuperuserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superusers to edit objects.
    Read-only access is allowed for any request (authenticated or not).
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the superuser.
        return request.user and request.user.is_authenticated and request.user.is_superuser 