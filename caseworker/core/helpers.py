from collections import defaultdict
from typing import List

from caseworker.core import decorators
from caseworker.core.constants import Permission
from caseworker.core.services import get_user_permissions
from lite_forms.components import FiltersBar, Option, Select, DateInput


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


def format_date(data, date_field):
    year = data.get(date_field + "year", "")
    month = data.get(date_field + "month", "")
    if len(month) == 1:
        month = "0" + month
    day = data.get(date_field + "day", "")
    if len(day) == 1:
        day = "0" + day
    return f"{year}-{month}-{day}" if year or month or day else None
