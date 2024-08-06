from collections import defaultdict

from caseworker.advice.services import LICENSING_UNIT_TEAM
from caseworker.cases.constants import CaseType
from caseworker.users.services import get_gov_user
from core import client
from core.constants import CaseStatusEnum
from core.helpers import convert_value_to_query_param
from lite_forms.components import Option


def get_denial_reasons(request, convert_to_options=False, group=False):
    data = client.get(request, "/static/denial-reasons/").json()["denial_reasons"]

    if convert_to_options:
        options = [Option(denial_reason["id"], denial_reason["id"]) for denial_reason in data]

        if group:
            return_dict = defaultdict(list)
            for item in options:
                return_dict[item.key[0]].append(item)
            return dict(return_dict)

        return options

    return data


def group_denial_reasons(denial_reasons):
    grouped = defaultdict(list)
    for item in denial_reasons:
        # skip the ones that are not active anymore
        if item["deprecated"]:
            continue
        grouped[item["id"][0]].append((item["id"], item.get("display_value") or item["id"]))
    return grouped.items()


def get_countries(request, convert_to_options=False, exclude: list = None):
    """
    Returns a list of GOV.UK countries and territories
    param exclude: Takes a list of country codes and excludes them
    """
    data = client.get(request, "/static/countries/?" + convert_value_to_query_param("exclude", exclude))

    if convert_to_options:
        converted_units = []

        for country in data.json().get("countries"):
            converted_units.append(Option(country.get("id"), country.get("name")))

        return converted_units

    return data.json(), data.status_code


# CaseStatuesEnum
def get_statuses(request, convert_to_options=False):
    """Get static list of case statuses."""
    data = client.get(request, "/static/statuses/")
    if convert_to_options:
        return [Option(key=item["id"], value=item["value"]) for item in data.json().get("statuses")]

    return data.json()["statuses"], data.status_code


def get_permissible_statuses(request, case):
    """Get a list of case statuses permissible for the user's role."""

    user, _ = get_gov_user(request, str(request.session["lite_api_user_id"]))
    user_permissible_statuses = user["user"]["role"]["statuses"]
    statuses, _ = get_statuses(request)
    case_type = case["case_type"]["type"]["key"]
    case_type_applicable_statuses = []

    if case_type == CaseType.APPLICATION.value:
        case_type_applicable_statuses = [
            status
            for status in statuses
            if status["key"]
            not in [
                CaseStatusEnum.APPLICANT_EDITING,
                CaseStatusEnum.FINALISED,
                CaseStatusEnum.REGISTERED,
                CaseStatusEnum.CLC,
                CaseStatusEnum.PV,
                CaseStatusEnum.SURRENDERED,
            ]
        ]

        user_team_alias = user["user"]["team"].get("alias")
        # Allow LU users to set Finalised status as required for Appeals
        if user_team_alias and user_team_alias == LICENSING_UNIT_TEAM:
            finalised_status = [status for status in statuses if status["key"] == CaseStatusEnum.FINALISED]
            case_type_applicable_statuses.extend(finalised_status)

    return [status for status in case_type_applicable_statuses if status in user_permissible_statuses]


def get_permissible_license_statuses(request, case):
    """Get a list of case statuses permissible for the user's role."""

    user, _ = get_gov_user(request, str(request.session["lite_api_user_id"]))
    # user_permissible_statuses = user["user"]["role"]["statuses"]

    statuses, _ = get_statuses(request)
    case_type = case["case_type"]["type"]["key"]
    case_type_applicable_statuses = []

    if case_type == CaseType.APPLICATION.value:
        case_type_applicable_statuses = [
            status
            for status in statuses
            if status["key"]
            not in [
                CaseStatusEnum.APPLICANT_EDITING,
                CaseStatusEnum.FINALISED,
                CaseStatusEnum.REGISTERED,
                CaseStatusEnum.CLC,
                CaseStatusEnum.PV,
                CaseStatusEnum.SURRENDERED,
            ]
        ]

        user_team_alias = user["user"]["team"].get("alias")
        # Allow LU users to set Finalised status as required for Appeals
        if user_team_alias and user_team_alias == LICENSING_UNIT_TEAM:
            finalised_status = [status for status in statuses if status["key"] == CaseStatusEnum.FINALISED]
            case_type_applicable_statuses.extend(finalised_status)

    return [status for status in case_type_applicable_statuses if status in user_permissible_statuses]


def get_status_properties(request, status):
    data = client.get(request, f"/static/statuses/properties/{status}")
    return data.json(), data.status_code


# Permissions
def get_user_permissions(request, with_team=False):
    user, _ = get_gov_user(request)
    if with_team:
        return user["user"]["role"]["permissions"], user["user"]["team"]
    return user["user"]["role"]["permissions"]


def get_user_role_name(request):
    user, _ = get_gov_user(request)
    return user["user"]["role"]["name"]


CLC_ENTRIES_CACHE = []


# Control List Entries
def get_control_list_entries(  # noqa
    request, convert_to_options=False, include_parent=False, clc_entries_cache=CLC_ENTRIES_CACHE  # noqa
):  # noqa
    """
    Preliminary caching mechanism, requires service restart to repopulate control list entries
    """
    if convert_to_options:
        if clc_entries_cache:
            return clc_entries_cache
        else:
            data = client.get(request, "/static/control-list-entries/")

        for control_list_entry in data.json().get("control_list_entries"):
            clc_entries_cache.append(
                Option(
                    key=control_list_entry["rating"],
                    value=control_list_entry["rating"],
                    description=control_list_entry["text"],
                )
            )

        return clc_entries_cache

    if include_parent:
        response = client.get(request, "/static/control-list-entries/?include_parent=True")
    else:
        response = client.get(request, "/static/control-list-entries/?group=True")

    response.raise_for_status()
    return response.json().get("control_list_entries")


# Regime Entries
def get_regime_entries(request):
    data = client.get(request, "/static/regimes/entries/")
    return [{"id": regime["pk"], "name": regime["name"]} for regime in sorted(data.json(), key=lambda r: r["name"])]


def get_pv_gradings(request, convert_to_options=False):
    pv_gradings = client.get(request, "/static/private-venture-gradings/").json().get("pv_gradings")

    if convert_to_options:
        converted_units = []
        for pv_grading_entry in pv_gradings:
            for key in pv_grading_entry:
                converted_units.append(Option(key=key, value=pv_grading_entry[key]))
        return converted_units

    return pv_gradings


def get_menu_notifications(request):
    if not hasattr(request, "cached_get_menu_notifications"):
        request.cached_get_menu_notifications = client.get(request, "/gov-users/notifications/")
    response = request.cached_get_menu_notifications
    return response.json()


def get_mentions(request):
    if not hasattr(request, "cached_mentions"):
        request.cached_mentions = client.get(request, "/cases/user-case-note-mentions/")
    response = request.cached_mentions
    return response.json(), response.status_code


def get_new_mention_count(request):
    if not hasattr(request, "cached_new_mention_count"):
        request.cached_new_mention_count = client.get(request, "/cases/user-case-note-mentions-new-count/")
    response = request.cached_new_mention_count
    response.raise_for_status()
    return response.json(), response.status_code
