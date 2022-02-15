from caseworker.cases.objects import Case
from core import client

from caseworker.core.helpers import format_date
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


# Applications
def put_application_status(request, pk, json):
    data = client.put(request, f"/applications/{pk}/status/", json)
    return data.json(), data.status_code


def get_finalise_application_goods(request, pk):
    data = client.get(request, f"/applications/{pk}/final-decision/")
    return data.json(), data.status_code


def finalise_application(request, pk, json):
    return client.put(request, f"/applications/{pk}/final-decision/", json)


def get_application_default_duration(request, pk):
    return int(client.get(request, f"/applications/{pk}/duration/").json()["licence_duration"])


# Goods Queries
def put_goods_query_clc(request, pk, json):
    # This is a workaround due to RespondCLCQuery not using a SingleFormView
    if "control_list_entries[]" in json:
        json["control_list_entries"] = json.getlist("control_list_entries[]")
    response = client.put(request, f"/queries/goods-queries/{pk}/clc-response/", json)
    return response.json(), response.status_code


def put_goods_query_pv_grading(request, pk, json):
    response = client.put(request, f"/queries/goods-queries/{pk}/pv-grading-response/", json)
    return response.json(), response.status_code


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


def post_ecju_query(request, pk, json):
    response = client.post(request, f"/cases/{pk}/ecju-queries/", json)
    return response.json(), response.status_code


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


def post_review_goods(request, case_id, json):
    json = {
        "objects": request.GET.getlist("goods", request.GET.getlist("goods_types")),
        "comment": request.POST.get("comment"),
        "control_list_entries": request.POST.getlist("control_list_entries[]", []),
        "is_good_controlled": request.POST.get("is_good_controlled") == "True",
        "report_summary": request.POST.get("report_summary"),
    }
    response = client.post(request, f"/goods/control-list-entries/{case_id}/", json)
    return response.json(), response.status_code


def post_review_good(request, case_id, data):
    response = client.post(request, f"/goods/control-list-entries/{case_id}/", data)
    response.raise_for_status()
    return response.json()


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


def get_destination(request, pk):
    data = client.get(request, f"/cases/destinations/{pk}")
    return data.json()


def put_case_officer(request, pk, json):
    data = client.put(request, f"/cases/{pk}/case-officer/", json)
    return data.json(), data.status_code


def delete_case_officer(request, pk, *args):
    data = client.delete(request, f"/cases/{pk}/case-officer/")
    return data.json(), data.status_code


def put_next_review_date(request, pk, json):
    if "next_review_dateday" in json:
        json["next_review_date"] = format_date(json, "next_review_date")
    data = client.put(request, f"/cases/{pk}/review-date/", json)
    return data.json(), data.status_code


def get_case_applicant(request, pk):
    response = client.get(request, f"/cases/{pk}/applicant/")
    return response.json()


def get_case_additional_contacts(request, pk):
    response = client.get(request, f"/cases/{pk}/additional-contacts/")
    return response.json()


def post_case_additional_contacts(request, pk, json):
    response = client.post(request, f"/cases/{pk}/additional-contacts/", json)
    return response.json(), response.status_code


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


def get_compliance_licences(request, case_id, reference, page):
    data = client.get(
        request,
        f"/compliance/{case_id}/licences/?reference={reference}&page={page}",
    )
    return data.json()


def post_create_compliance_visit(request, case_id):
    data = client.post(request, f"/compliance/site/{case_id}/visit/", data={})
    return data


def get_compliance_visit_case(request, case_id):
    data = client.get(request, f"/compliance/visit/{case_id}")
    return data.json()


def patch_compliance_visit_case(request, case_id, json):
    if "visit_date_day" in json:
        json["visit_date"] = format_date(json, "visit_date_")
    data = client.patch(request, f"/compliance/visit/{case_id}", data=json)
    return data.json(), data.status_code


def get_compliance_people_present(request, case_id):
    data = client.get(request, f"/compliance/visit/{case_id}/people-present/?disable_pagination=True")
    return data.json()


def post_compliance_person_present(request, case_id, json):
    data = client.post(request, f"/compliance/visit/{case_id}/people-present/", data=json)

    # Translate errors to be more user friendly, from
    #   {'errors': [{}, {'name': ['This field may not be blank.'], 'job_title': ['This field may not be blank.']}, ...]}
    #   to
    #   {'errors': {'name-2': ['This field may not be blank'], 'job-title-2': ['This field may not be blank'], ...}}
    # This allows the errors to specify the specific textbox input for name/job-title inputs allowing the users
    #   to see the exact field it didn't validate on.
    if "errors" in data.json():
        errors = data.json()["errors"]
        translated_errors = {}

        index = 1
        for error in errors:
            if error:
                if "name" in error:
                    translated_errors[f"name-{index}"] = [f"{index}. " + error.pop("name")[0]]
                if "job_title" in error:
                    translated_errors[f"job-title-{index}"] = [f"{index}. " + error.pop("job_title")[0]]
            index += 1

        return {**json, "errors": translated_errors}, data.status_code
    return data.json(), data.status_code
