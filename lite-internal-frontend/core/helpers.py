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


def get_params_if_exist(request, keys, json=None):
    params = json if json else dict()
    for key in keys:
        value = request.GET.get(key, False)
        if value:
            params[key] = value
    return params


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


def convert_value_to_query_param(key: str, value):
    """
    Convert key/value pairs to a string suitable for query parameters
    eg {'type': 'organisation'} becomes type=organisation
    eg {'type': ['organisation', 'organisation']} becomes type=organisation&type=organisation
    """
    if value is None:
        return ""

    if isinstance(value, list):
        return_value = ""
        for item in value:
            if not return_value:
                return_value = return_value + key + "=" + item
            else:
                return_value = return_value + "&" + key + "=" + item
        return return_value

    return key + "=" + str(value)
