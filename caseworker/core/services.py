from collections import defaultdict

from caseworker.users.services import get_gov_user
from core import client
from core.constants import CaseStatusEnum
from core.helpers import convert_value_to_query_param
from caseworker.cases.constants import CaseType
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
    case_sub_type = case["case_type"]["sub_type"]["key"]
    case_type = case["case_type"]["type"]["key"]

    if case_type == CaseType.APPLICATION.value:
        case_type_applicable_statuses = [
            status
            for status in statuses
            if status["key"]
            not in [
                CaseStatusEnum.APPLICANT_EDITING,
                CaseStatusEnum.CLOSED,
                CaseStatusEnum.FINALISED,
                CaseStatusEnum.REGISTERED,
                CaseStatusEnum.CLC,
                CaseStatusEnum.PV,
                CaseStatusEnum.SURRENDERED,
            ]
        ]
    elif case_type == CaseType.QUERY.value:
        if case_sub_type == CaseType.END_USER_ADVISORY.value:
            case_type_applicable_statuses = [
                status for status in statuses if status["key"] in CaseStatusEnum.base_query_statuses()
            ]
        else:
            # if the query is not an end user advisory, then check if CLC/PV statuses are required
            goods_query_status_keys = CaseStatusEnum.base_query_statuses().copy()

            if case.data["clc_responded"] is not None:
                goods_query_status_keys.insert(1, CaseStatusEnum.CLC)

            if case.data["pv_grading_responded"] is not None:
                # add PV status into the correct location
                if case.data["clc_responded"] is not None:
                    goods_query_status_keys.insert(2, CaseStatusEnum.PV)
                else:
                    goods_query_status_keys.insert(1, CaseStatusEnum.PV)

            case_type_applicable_statuses = [status for status in statuses if status["key"] in goods_query_status_keys]
    elif case_type == CaseType.COMPLIANCE.value:
        if case_sub_type == CaseType.COMPLIANCE_SITE.value:
            case_type_applicable_statuses = [
                status
                for status in statuses
                if status["key"]
                in [
                    CaseStatusEnum.OPEN,
                    CaseStatusEnum.CLOSED,
                ]
            ]
        elif case_sub_type == CaseType.COMPLIANCE_VISIT.value:
            case_type_applicable_statuses = [
                status
                for status in statuses
                if status["key"]
                in [
                    CaseStatusEnum.OPEN,
                    CaseStatusEnum.UNDER_INTERNAL_REVIEW,
                    CaseStatusEnum.RETURN_TO_INSPECTOR,
                    CaseStatusEnum.AWAITING_EXPORTER_RESPONSE,
                    CaseStatusEnum.CLOSED,
                ]
            ]
    elif case_type == CaseType.REGISTRATION.value:
        case_type_applicable_statuses = [
            status
            for status in statuses
            if status["key"]
            in [
                CaseStatusEnum.REGISTERED,
                CaseStatusEnum.UNDER_ECJU_REVIEW,
                CaseStatusEnum.REVOKED,
                CaseStatusEnum.SUSPENDED,
                CaseStatusEnum.SURRENDERED,
                CaseStatusEnum.DEREGISTERED,
            ]
        ]
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


# Control List Entries
def get_control_list_entries(request, convert_to_options=False, include_parent=False, clc_entries_cache=[]):  # noqa
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


def get_gov_pv_gradings(request, convert_to_options=False):
    pv_gradings = client.get(request, "/static/private-venture-gradings/gov/").json().get("pv_gradings")
    if convert_to_options:
        converted_units = []
        for pv_grading_entry in pv_gradings:
            for key in pv_grading_entry:
                converted_units.append(Option(key=key, value=pv_grading_entry[key]))
        return converted_units

    return pv_gradings


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
