from cacheops import cached
from collections import defaultdict
from django.conf import settings

from caseworker.advice.constants import LICENSING_UNIT_TEAM, MOD_ECJU
from caseworker.cases.constants import CaseType
from caseworker.core.constants import CONTROL_LIST_ENTRIES_CACHE_TIMEOUT
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


def get_caseworker_operable_case_statuses(request):
    """
    Get list of case statuses which are operable - that is cases which can be
    assigned/worked upon by caseworkers.
    """
    response = client.get(request, "/static/statuses/")
    response.raise_for_status()
    operable_statuses = [status["status"] for status in response.json()["statuses"] if status["is_caseworker_operable"]]

    return operable_statuses


def get_permissible_statuses(request, case):
    """Get a list of case statuses permissible for the user's role."""
    user, _ = get_gov_user(request, str(request.session["lite_api_user_id"]))
    user_permissible_statuses = user["user"]["role"]["statuses"]
    user_team_alias = user["user"]["team"]["id"]
    permissible_statuses = []

    # TODO: Make this list of dis-allowed caseworker-settable statuses driven by the API
    if case.type == CaseType.SECURITY_CLEARANCE.value:
        permissible_statuses = [
            CaseStatusEnum.SUBMITTED,
            CaseStatusEnum.OGD_ADVICE,
            CaseStatusEnum.UNDER_FINAL_REVIEW,
            CaseStatusEnum.WITHDRAWN,
            CaseStatusEnum.REOPENED_FOR_CHANGES,
        ]
        if user_team_alias == MOD_ECJU:
            permissible_statuses.append(CaseStatusEnum.FINALISED)

    elif case.type == CaseType.APPLICATION.value:
        statuses, _ = get_statuses(request)
        permissible_statuses = [
            status["key"]
            for status in statuses
            if status["key"]
            not in [
                CaseStatusEnum.APPLICANT_EDITING,
                CaseStatusEnum.FINALISED,
                CaseStatusEnum.SUPERSEDED_BY_EXPORTER_EDIT,
                CaseStatusEnum.REGISTERED,
                CaseStatusEnum.CLC,
                CaseStatusEnum.PV,
                CaseStatusEnum.SURRENDERED,
                CaseStatusEnum.REVOKED,
                CaseStatusEnum.SUSPENDED,
            ]
        ]

        if user_team_alias == LICENSING_UNIT_TEAM:
            permissible_statuses.append(CaseStatusEnum.FINALISED)
    filtered_statuses = [
        status_dict for status_dict in user_permissible_statuses if status_dict["key"] in permissible_statuses
    ]
    return sorted(filtered_statuses, key=lambda status: status["priority"])


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


# Vary the cache by GIT_COMMIT sha - to invalidate the cache on release
@cached(timeout=CONTROL_LIST_ENTRIES_CACHE_TIMEOUT, extra=settings.GIT_COMMIT)
def get_control_list_entries(request, include_non_selectable_for_assessment=False):
    url = "/caseworker/static/control-list-entries/"
    if include_non_selectable_for_assessment:
        url = f"{url}?include_non_selectable_for_assessment=True"

    response = client.get(request, url)
    response.raise_for_status()
    return response.json()


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
