from collections import defaultdict
from typing import List

from conf import decorators
from conf.constants import Permission
from core.services import get_user_permissions
from lite_forms.components import FiltersBar, Option, Select, DateInput


def convert_dict_to_query_params(dictionary):
    items = []
    for key, value in dictionary.items():
        if isinstance(value, list):
            for val in value:
                items.append(key + "=" + str(val))
        else:
            items.append(key + "=" + str(value))
    return "&".join(items)


def convert_parameters_to_query_params(dictionary: dict):
    """
    Given a dictionary of parameters, convert to a query param string
    Removes request object and deletes empty keys
    """
    if "request" in dictionary:
        del dictionary["request"]

    return "?" + convert_dict_to_query_params({key: value for key, value in dictionary.items() if value is not None})


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
    return has_permissions(request, [permission])


def has_permissions(request, permissions: List[Permission]):
    """
    Returns true if the user has the given permissions, else false
    """
    user_permissions = get_user_permissions(request)
    return_value = True
    for permission in permissions:
        if permission.value not in user_permissions:
            return_value = False
    return return_value


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


def group_control_list_entries_by_category(control_list_entries):
    dictionary = defaultdict(list)

    for control_list_entry in control_list_entries:
        dictionary[control_list_entry["category"]].append(control_list_entry)

    return dictionary


def generate_activity_filters(activity_filters, string_class):
    def make_options(values):
        return [Option(option["key"], option["value"]) for option in values]

    return FiltersBar(
        [
            Select(
                title=string_class.ActivityFilters.USER,
                name="user_id",
                options=make_options(activity_filters["users"]),
            ),
            Select(
                title=string_class.ActivityFilters.TEAM,
                name="team_id",
                options=make_options(activity_filters["teams"]),
            ),
            Select(
                title=string_class.ActivityFilters.USER_TYPE,
                name="user_type",
                options=make_options(activity_filters["user_types"]),
            ),
            Select(
                title=string_class.ActivityFilters.ACTIVITY_TYPE,
                name="activity_type",
                options=make_options(activity_filters["activity_types"]),
            ),
            DateInput(title=string_class.ActivityFilters.DATE_FROM, prefix="from_", inline_title=True),
            DateInput(title=string_class.ActivityFilters.DATE_TO, prefix="to_", inline_title=True),
        ]
    )
