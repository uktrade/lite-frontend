from conf import decorators
from conf.constants import Permission
from core.services import get_user_permissions


def convert_dict_to_query_params(dictionary):
    items = []
    for key, value in dictionary.items():
        if isinstance(value, list):
            for val in value:
                items.append(key + "=" + str(val))
        else:
            items.append(key + "=" + str(value))
    return "&".join(items)


def has_permission(request, permission: Permission):
    """
    Returns true if the user has a given permission, else false
    """
    user_permissions = get_user_permissions(request)
    return permission.value in user_permissions


def decorate_patterns_with_permission(patterns, permission: Permission):
    def _wrap_with_permission(_permission: Permission, view_func=None):
        actual_decorator = decorators.has_permission(_permission)

        if view_func:
            return actual_decorator(view_func)
        return actual_decorator

    decorated_patterns = []
    for pattern in patterns:
        callback = pattern.callback
        pattern.callback = _wrap_with_permission(permission, callback)
        pattern._callback = _wrap_with_permission(permission, callback)
        decorated_patterns.append(pattern)
    return decorated_patterns
