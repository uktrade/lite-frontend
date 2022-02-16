import logging
from django.utils.functional import wraps

from exporter.core import helpers


logger = logging.getLogger(__name__)


def has_permission(permission):
    """
    Decorator for views that checks that the user has a given permission
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            has_permission_bool, permissions = helpers.has_permission(request, permission)
            if has_permission_bool:
                return view_func(request, *args, **kwargs, permissions=permissions)

            logger.warning(
                "You don't have the permission '%s' to view this, "
                "check urlpatterns or the function decorator if you want to change "
                "this functionality.",
                permission,
            )
            return

        return _wrapped_view

    return decorator
