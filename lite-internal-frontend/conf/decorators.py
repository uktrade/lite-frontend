from django.utils.functional import wraps

from conf.constants import Permission
from conf.exceptions import PermissionDeniedError
from core import helpers


def has_permission(permission: Permission):
    """
    Decorator for views that checks that the user has a given permission
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if helpers.has_permission(request, permission):
                return view_func(request, *args, **kwargs)

            raise PermissionDeniedError(
                f"You don't have the permission '{permission.value}' to view this, "
                "check urlpatterns or the function decorator if you want to change "
                "this functionality."
            )

        return _wrapped_view

    return decorator
