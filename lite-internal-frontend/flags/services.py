import functools

from conf.client import get, post, put, patch
from conf.constants import FLAGS_URL, FLAGGING_RULES
from core.helpers import convert_parameters_to_query_params
from flags.enums import FlagStatus
from lite_forms.components import Option
from users.services import get_gov_user


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
    data = get(request, FLAGS_URL + convert_parameters_to_query_params(locals()))
    return data.json()


def _get_team_flags(level, request, convert_to_options=False, include_deactivated=False):
    user, _ = get_gov_user(request)
    team_pk = user["user"]["team"]["id"]
    data = get(
        request,
        f"{FLAGS_URL}?level={level}&team={team_pk}&include_deactivated={include_deactivated}&disable_pagination=True",
    ).json()

    if convert_to_options:
        return [
            Option(
                key=flag["id"],
                value=flag["name"],
                classes=["app-flag", "app-flag--checkbox", "app-flag--" + flag["colour"]],
            )
            for flag in data
        ]

    return data


get_cases_flags = functools.partial(_get_team_flags, "Case", convert_to_options=True)
get_goods_flags = functools.partial(_get_team_flags, "Good", convert_to_options=True)
get_organisation_flags = functools.partial(_get_team_flags, "Organisation", convert_to_options=True)
get_destination_flags = functools.partial(_get_team_flags, "Destination", convert_to_options=True)


def post_flags(request, json):
    data = post(request, FLAGS_URL, json)
    return data.json(), data.status_code


def get_flag(request, pk):
    data = get(request, FLAGS_URL + pk)
    return data.json()


def update_flag(request, pk, json):
    data = patch(request, FLAGS_URL + pk + "/", json)
    return data.json(), data.status_code


def get_flagging_rules(request, params):
    data = get(request, FLAGGING_RULES + "?" + params)
    return data.json(), data.status_code


def post_flagging_rules(request, json):
    data = post(request, FLAGGING_RULES, json)
    return data.json(), data.status_code


def get_flagging_rule(request, pk):
    data = get(request, FLAGGING_RULES + str(pk))
    return data.json(), data.status_code


def put_flagging_rule(request, pk, json):
    data = json
    if json.get("form_name"):
        data["status"] = json.get("form_name")
    data = put(request, FLAGGING_RULES + str(pk), json)
    return data.json(), data.status_code
