import logging
from django.utils.functional import wraps

from caseworker.core.constants import Permission
from caseworker.core import helpers


logger = logging.getLogger(__name__)


def has_permission(permission: Permission):
    """
    Decorator for views that checks that the user has a given permission
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if helpers.has_permission(request, permission):
                return view_func(request, *args, **kwargs)

            logger.warning(
                "You don't have the permission '%s' to view this, "
                "check urlpatterns or the function decorator if you want to change "
                "this functionality.",
                permission.value,
            )
            return

        return _wrapped_view

    return decorator
