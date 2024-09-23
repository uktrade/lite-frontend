import functools

from core import client
from core.helpers import convert_parameters_to_query_params

from caseworker.flags.enums import FlagStatus, FlagPermissions
from caseworker.users.services import get_gov_user

from lite_forms.components import Option


def get_flags(
    request,
    page=1,
    name=None,
    level=None,
    priority=None,
    status=FlagStatus.ACTIVE.value,
    team=None,
    disable_pagination=False,
):
    data = client.get(request, "/flags/" + convert_parameters_to_query_params(locals()))
    return data.json()


def _add_flag_permissions(data, permissions):
    return [
        {
            "cannot_remove": (
                flag["removable_by"] != FlagPermissions.DEFAULT
                and FlagPermissions.PERMISSIONS_MAPPING[flag["removable_by"]].value not in permissions
            ),
            **flag,
        }
        for flag in data
    ]


def _get_team_flags(level, request, convert_to_options=False, include_deactivated=False):
    user, _ = get_gov_user(request)
    team_pk = user["user"]["team"]["id"]
    data = client.get(
        request,
        f"/flags/?level={level}&team={team_pk}&include_deactivated={include_deactivated}&disable_pagination=True",
    ).json()

    flags = _add_flag_permissions(data, user["user"]["role"]["permissions"])

    if convert_to_options:
        return [
            Option(
                key=flag["id"],
                value=flag["name"],
                classes=["app-flag", "app-flag--checkbox", "app-flag--" + flag["colour"]],
                cannot_remove=flag["cannot_remove"],
                data_attribute="cannot-remove" if flag["cannot_remove"] else "",
            )
            for flag in flags
        ]

    return flags


get_cases_flags = functools.partial(_get_team_flags, "Case", convert_to_options=True)
get_goods_flags = functools.partial(_get_team_flags, "Good", convert_to_options=True)
get_organisation_flags = functools.partial(_get_team_flags, "Organisation", convert_to_options=True)
get_destination_flags = functools.partial(_get_team_flags, "Destination", convert_to_options=True)
