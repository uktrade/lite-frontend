from caseworker.cases.objects import Case
from core import client

from caseworker.flags.enums import FlagStatus
from core.helpers import convert_parameters_to_query_params


# Case types
def get_case_types(request, type_only=True):
    data = client.get(request, f"/static/case-types/?type_only={type_only}")
    return data.json()["case_types"]


# Case
def get_case(request, pk):
    response = client.get(request, f"/cases/{pk}")
    response.raise_for_status()
    parsed = response.json()
    return Case(parsed["case"])


def get_case_basic_details(request, pk):
    response = client.get(request, f"/cases/{pk}/basic")
    response.raise_for_status()
    return response.json()


def patch_case(request, pk, json):
    response = client.patch(request, f"/cases/{pk}", json)
    return response.json(), response.status_code


# Case Queues
def put_case_queues(request, pk, json):
    data = client.put(request, f"/cases/{pk}/queues/", json)
    return data.json(), data.status_code


# Queue assignment actions
def get_user_case_queues(request, pk):
    data = client.get(request, f"/cases/{pk}/assigned-queues/")
    return data.json()["queues"], data.status_code


def put_unassign_queues(request, pk, json):
    data = client.put(request, f"/cases/{pk}/assigned-queues/", json)
    return data.json(), data.status_code


def delete_case_assignment(request, case_id, assignment_id):
    response = client.delete(request, f"/cases/{case_id}/case-assignments/{assignment_id}")
    return response


# Applications
def put_application_status(request, pk, json):
    response = client.put(request, f"/applications/{pk}/status/", json)
    response.raise_for_status()
    return response.json(), response.status_code


def get_finalise_application_goods(request, pk):
    data = client.get(request, f"/applications/{pk}/final-decision/")
    return data.json(), data.status_code


def finalise_application(request, pk, json):
    return client.put(request, f"/applications/{pk}/final-decision/", json)


def get_application_default_duration(request, pk):
    return int(client.get(request, f"/applications/{pk}/duration/").json()["licence_duration"])


# Case Notes
def get_case_notes(request, pk):
    data = client.get(request, f"/cases/{pk}/case-notes/")
    return data.json(), data.status_code


def post_case_notes(request, pk, json):
    data = client.post(request, f"/cases/{pk}/case-notes/", json)
    return data.json(), data.status_code


# Activity
def get_activity(request, pk, activity_filters=None):
    url = f"/cases/{pk}/activity/"
    if activity_filters:
        params = convert_parameters_to_query_params(activity_filters)
        url = url + params
    data = client.get(request, url)
    return data.json()["activity"]


def get_mentions(request, pk):
    url = f"/cases/{pk}/case-note-mentions/"
    data = client.get(request, url)
    return data.json()


def update_mentions(request, json):
    request = client.put(request, "/cases/case-note-mentions/", json)
    request.raise_for_status()
    return request.json()


def get_activity_filters(request, pk):
    data = client.get(request, f"/cases/{pk}/activity/filters/")
    return data.json()["filters"]


# Case Documents
def get_case_document(request, pk, document_metadata_id):
    data = client.get(request, f"/cases/{pk}/documents/{document_metadata_id}")
    return data.json(), data.status_code


def get_case_documents(request, pk):
    data = client.get(request, f"/cases/{pk}/documents/")
    return data.json(), data.status_code


def post_case_documents(request, pk, json):
    data = client.post(request, f"/cases/{pk}/documents/", json)
    return data.json(), data.status_code


def delete_case_document(request, pk, s3_key):
    data = client.delete(request, f"/cases/{pk}/documents/{s3_key}")
    return data.json(), data.status_code


# Advice
def get_user_case_advice(request, case_pk):
    data = client.get(request, f"/cases/{case_pk}/user-advice/")
    return data.json(), data.status_code


def get_team_case_advice(request, case_pk, team_pk):
    data = client.get(request, f"/cases/{case_pk}/view-team-advice/{team_pk}")
    return data.json(), data.status_code


def coalesce_user_advice(request, case_pk):
    data = client.get(request, f"/cases/{case_pk}/team-advice/")
    return data.json(), data.status_code


def clear_team_advice(request, case_pk):
    data = client.delete(request, f"/cases/{case_pk}/team-advice/")
    return data.json(), data.status_code


def get_final_decision_documents(request, case_pk):
    data = client.get(request, f"/cases/{case_pk}/final-advice-documents/")
    return data.json(), data.status_code


def grant_licence(request, case_pk, json):
    response = client.put(request, f"/cases/{case_pk}/finalise/", json)
    return response.json(), response.status_code


def get_licence(request, case_pk):
    data = client.get(request, f"/cases/{case_pk}/licences/")
    return data.json(), data.status_code


def coalesce_team_advice(request, case_pk):
    data = client.get(request, f"/cases/{case_pk}/final-advice/")
    return data.json(), data.status_code


def clear_final_advice(request, case_pk):
    data = client.delete(request, f"/cases/{case_pk}/final-advice/")
    return data.json(), data.status_code


def get_good_countries_decisions(request, case_pk):
    data = client.get(request, f"/cases/{case_pk}/goods-countries-decisions/")
    return data.json()


def post_good_countries_decisions(request, pk, json):
    response = client.post(request, f"/cases/{pk}/goods-countries-decisions/", json)
    return response.json(), response.status_code


def get_open_licence_decision(request, case_pk):
    data = client.get(request, f"/cases/{case_pk}/open-licence-decision/")
    return data.json()["decision"]


def post_user_case_advice(request, pk, json):
    response = client.post(request, f"/cases/{pk}/user-advice/", json)
    return response.json(), response.status_code


def post_team_case_advice(request, pk, json):
    response = client.post(request, f"/cases/{pk}/team-advice/", json)
    return response.json(), response.status_code


def post_final_case_advice(request, pk, json):
    response = client.post(request, f"/cases/{pk}/final-advice/", json)
    return response.json(), response.status_code


def get_document(request, pk):
    data = client.get(request, f"/documents/{pk}")
    return data.json(), data.status_code


# ECJU Queries
def get_ecju_queries(request, pk):
    data = client.get(request, f"/cases/{pk}/ecju-queries/")
    return data.json(), data.status_code


def get_ecju_queries_open_count(request, pk):
    response = client.get(request, f"/cases/{pk}/ecju-queries-open-count/")
    response.raise_for_status()
    return response.json()


def post_ecju_query(request, pk, json):
    response = client.post(request, f"/cases/{pk}/ecju-queries/", json)
    return response.json(), response.status_code


def put_ecju_query(request, pk, query_pk, json):
    data = client.put(request, f"/cases/{pk}/ecju-queries/{query_pk}/", json)
    data.raise_for_status()
    return data.json(), data.status_code


def get_good_on_application(request, pk):
    response = client.get(request, f"/applications/good-on-application/{pk}")
    response.raise_for_status()
    return response.json()


def get_good_on_application_documents(request, pk, good_pk):
    response = client.get(request, f"/applications/{pk}/goods/{good_pk}/documents/")
    response.raise_for_status()
    return response.json()


def get_good_on_application_document_detail(request, pk, good_pk, doc_pk):
    response = client.get(request, f"/applications/{pk}/goods/{good_pk}/documents/{doc_pk}/")
    response.raise_for_status()
    return response.json()


def get_good(request, pk):
    data = client.get(request, f"/goods/{pk}")
    return data.json(), data.status_code


def get_goods_type(request, pk):
    data = client.get(request, f"/goods-types/{pk}")
    # API doesn't structure the endpoints in a way that flags (currently) works,
    # so wrap data in dictionary
    return {"good": data.json()}, data.status_code


# Good Flags
def get_flags_for_team_of_level(request, level, team_id, include_system_flags=False):
    """
    :param request: headers for the request
    :param level: 'cases', 'goods'
    :param include_system_flags: used to indicate adding system flags to list of team flags returned
    :return:
    """
    response = client.get(
        request,
        "/flags/"
        + convert_parameters_to_query_params(locals())
        + "&disable_pagination=True&include_flagging_rules=True",
    )
    response.raise_for_status()

    # Remove system flags from selection while creating routing rules
    return [flag for flag in response.json() if flag["team"]["id"] != "00000000-0000-0000-0000-000000000001"]


def put_flag_assignments(request, json):
    data = client.put(request, "/flags/assign/", json)
    return data.json(), data.status_code


# Letter template decisions
def get_decisions(request):
    data = client.get(request, "/static/decisions/")
    return data.json()["decisions"], data.status_code


# Generated Documents
def post_generated_document(request, pk, json):
    data = client.post(request, f"/cases/{pk}/generated-documents/", json)
    return data.status_code


def get_generated_document_preview(request, pk, template, text, addressee):
    params = convert_parameters_to_query_params(locals())
    data = client.get(request, f"/cases/{pk}/generated-documents/preview/" + params)
    return data.json(), data.status_code


def get_generated_document(request, pk, dpk):
    data = client.get(request, f"/cases/{pk}/generated-documents/{dpk}/")
    return data.json(), data.status_code


def send_generated_document(request, pk, document_pk):
    response = client.post(request, f"/cases/{pk}/generated-documents/{document_pk}/send/")
    return response


def get_destination(request, pk):
    data = client.get(request, f"/cases/destinations/{pk}")
    return data.json()


def put_case_officer(request, pk, json):
    data = client.put(request, f"/cases/{pk}/case-officer/", json)
    return data.json(), data.status_code


def update_case_officer_on_cases(request, case_ids, user_id):
    response = client.put(request, "/cases/cases-update-case-officer/", {"gov_user_pk": user_id, "case_ids": case_ids})
    response.raise_for_status()
    return response.json(), response.status_code


def delete_case_officer(request, pk, *args):
    data = client.delete(request, f"/cases/{pk}/case-officer/")
    return data.json(), data.status_code


def get_case_applicant(request, pk):
    response = client.get(request, f"/cases/{pk}/applicant/")
    return response.json()


def get_case_additional_contacts(request, pk):
    response = client.get(request, f"/cases/{pk}/additional-contacts/")
    return response.json()


def put_rerun_case_routing_rules(request, pk, json):
    response = client.put(request, f"/cases/{pk}/rerun-routing-rules/", {})
    return response.json(), response.status_code


def reissue_ogl(request, pk, json):
    response = client.post(request, f"/cases/{pk}/reissue-ogl/", json)
    return response.json(), response.status_code


def get_blocking_flags(request, case_pk):
    url = f"/flags/?case={case_pk}&status={FlagStatus.ACTIVE.value}&blocks_finalising=True&disable_pagination=True"
    data = client.get(request, url)
    return data.json()


def get_case_sub_statuses(request, case_id):
    response = client.get(request, f"/applications/{case_id}/sub-statuses/")
    response.raise_for_status()
    return response.json()


def put_case_sub_status(request, case_id, data):
    response = client.put(
        request,
        f"/applications/{case_id}/sub-status/",
        data=data,
    )
    response.raise_for_status()
    return response.json(), response.status_code


def get_licence_details(request, license_pk):
    response = client.get(request, f"/licence_details/{license_pk}/")
    return response.json()
