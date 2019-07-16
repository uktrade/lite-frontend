from django.http import Http404
from django.utils.functional import wraps

from core.services import get_user_permissions


def has_permission(permission: str):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            permissions = get_user_permissions(args[0])

            if permission in permissions:
                return func(request, *args, **kwargs)
            else:
                pass

            raise Http404()

        return wraps(func)(inner_decorator)

    return decorator
