from rest_framework import permissions


class IsAuthbrokerAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.authbroker_client.token:
            return False

        return not request.authbroker_client.token.is_expired()
