from rest_framework import permissions


class IsAuthbrokerAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.authbroker_client.authorized
