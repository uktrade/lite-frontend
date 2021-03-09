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


def _get_team_flags(level, request, convert_to_options=False, include_deactivated=False):
    user, _ = get_gov_user(request)
    team_pk = user["user"]["team"]["id"]
    data = client.get(
        request,
        f"/flags/?level={level}&team={team_pk}&include_deactivated={include_deactivated}&disable_pagination=True",
    ).json()

    flags = [
        {
            "cannot_remove": (
                flag["removable_by"] != FlagPermissions.DEFAULT
                and FlagPermissions.PERMISSIONS_MAPPING[flag["removable_by"]].value
                not in user["user"]["role"]["permissions"]
            ),
            **flag,
        }
        for flag in data
    ]

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


def post_flags(request, json):
    data = client.post(request, "/flags/", json)
    return data.json(), data.status_code


def get_flag(request, pk):
    data = client.get(request, f"/flags/{pk}")
    return data.json()


def update_flag(request, pk, json):
    data = client.patch(request, f"/flags/{pk}/", json)
    return data.json(), data.status_code


def get_flagging_rules(request, params):
    data = client.get(request, f"/flags/rules/?{params}")
    return data.json(), data.status_code


def post_flagging_rules(request, json):
    data = client.post(request, "/flags/rules/", json)
    return data.json(), data.status_code


def get_flagging_rule(request, pk):
    data = client.get(request, f"/flags/rules/{pk}")
    return data.json(), data.status_code


def put_flagging_rule(request, pk, json):
    data = json
    if json.get("form_name"):
        data["status"] = json.get("form_name")
    data = client.put(request, f"/flags/rules/{pk}", json)
    return data.json(), data.status_code
