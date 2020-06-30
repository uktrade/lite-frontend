from cases.objects import Case
from conf.client import post, get, put, delete, patch
from conf.constants import (
    CASE_URL,
    CASE_NOTES_URL,
    APPLICATIONS_URL,
    ACTIVITY_URL,
    ACTIVITY_FILTERS_URL,
    DOCUMENTS_URL,
    ECJU_QUERIES_URL,
    GOOD_URL,
    FLAGS_URL,
    ASSIGN_FLAGS_URL,
    GOODS_TYPE_URL,
    USER_ADVICE_URL,
    TEAM_ADVICE_URL,
    FINAL_ADVICE_URL,
    VIEW_TEAM_ADVICE_URL,
    GOOD_CLC_REVIEW_URL,
    MANAGE_STATUS_URL,
    FINAL_DECISION_URL,
    DURATION_URL,
    GENERATED_DOCUMENTS_URL,
    GENERATED_DOCUMENTS_PREVIEW_URL,
    DESTINATION_URL,
    CASE_OFFICER_URL,
    CASE_TYPES_URL,
    GOODS_QUERIES_URL,
    CLC_RESPONSE_URL,
    PV_GRADING_RESPONSE_URL,
    DECISIONS_URL,
    FINALISE_CASE_URL,
    QUEUES_URL,
    APPLICANT_URL,
    COMPLIANCE_URL,
    COMPLIANCE_LICENCES_URL,
    COMPLIANCE_SITE_URL,
    COMPLIANCE_VISIT_URL,
    COMPLIANCE_PEOPLE_PRESENT_URL,
)
from core.helpers import convert_parameters_to_query_params, format_date
from flags.enums import FlagStatus


# Case types
def get_case_types(request, type_only=True):
    data = get(request, CASE_TYPES_URL + "?type_only=" + str(type_only))
    return data.json()["case_types"]


# Case
def get_case(request, pk):
    response = get(request, CASE_URL + str(pk))
    return Case(response.json()["case"])


def patch_case(request, pk, json):
    response = patch(request, CASE_URL + str(pk), json)
    return response.json(), response.status_code


# Case Queues
def put_case_queues(request, pk, json):
    data = put(request, CASE_URL + str(pk) + QUEUES_URL, json)
    return data.json(), data.status_code


# Queue assignment actions
def get_user_case_queues(request, pk):
    data = get(request, CASE_URL + str(pk) + "/assigned-queues/")
    return data.json()["queues"], data.status_code


def put_unassign_queues(request, pk, json):
    data = put(request, CASE_URL + str(pk) + "/assigned-queues/", json)
    return data.json(), data.status_code


# Applications
def put_application_status(request, pk, json):
    data = put(request, APPLICATIONS_URL + pk + MANAGE_STATUS_URL, json)
    return data.json(), data.status_code


def get_finalise_application_goods(request, pk):
    data = get(request, f"{APPLICATIONS_URL}{pk}{FINAL_DECISION_URL}")
    return data.json(), data.status_code


def finalise_application(request, pk, json):
    return put(request, f"{APPLICATIONS_URL}{pk}{FINAL_DECISION_URL}", json)


def get_application_default_duration(request, pk):
    return int(get(request, f"{APPLICATIONS_URL}{pk}{DURATION_URL}").json()["licence_duration"])


# Goods Queries
def put_goods_query_clc(request, pk, json):
    # This is a workaround due to RespondCLCQuery not using a SingleFormView
    if "control_list_entries[]" in json:
        json["control_list_entries"] = json.getlist("control_list_entries[]")
    response = put(request, GOODS_QUERIES_URL + str(pk) + CLC_RESPONSE_URL, json)
    return response.json(), response.status_code


def put_goods_query_pv_grading(request, pk, json):
    response = put(request, GOODS_QUERIES_URL + str(pk) + PV_GRADING_RESPONSE_URL, json)
    return response.json(), response.status_code


def put_compliance_status(request, pk, json):
    response = put(request, COMPLIANCE_URL + str(pk) + MANAGE_STATUS_URL, json)
    return response.json(), response.status_code


# Case Notes
def get_case_notes(request, pk):
    data = get(request, CASE_URL + pk + CASE_NOTES_URL)
    return data.json(), data.status_code


def post_case_notes(request, pk, json):
    data = post(request, CASE_URL + pk + CASE_NOTES_URL, json)
    return data.json(), data.status_code


# Activity
def get_activity(request, pk, activity_filters=None):
    url = CASE_URL + pk + ACTIVITY_URL
    if activity_filters:
        params = convert_parameters_to_query_params(activity_filters)
        url = url + params
    data = get(request, url)
    return data.json()["activity"]


def get_activity_filters(request, pk):
    data = get(request, CASE_URL + pk + ACTIVITY_FILTERS_URL)
    return data.json()["filters"]


# Case Documents
def get_case_document(request, pk, document_metadata_id):
    data = get(request, CASE_URL + pk + DOCUMENTS_URL + document_metadata_id)
    return data.json(), data.status_code


def get_case_documents(request, pk):
    data = get(request, CASE_URL + pk + DOCUMENTS_URL)
    return data.json(), data.status_code


def post_case_documents(request, pk, json):
    data = post(request, CASE_URL + pk + DOCUMENTS_URL, json)
    return data.json(), data.status_code


def delete_case_document(request, pk, s3_key):
    data = delete(request, CASE_URL + pk + DOCUMENTS_URL + s3_key)
    return data.json(), data.status_code


# Advice
def get_user_case_advice(request, case_pk):
    data = get(request, CASE_URL + case_pk + USER_ADVICE_URL)
    return data.json(), data.status_code


def get_team_case_advice(request, case_pk, team_pk):
    data = get(request, CASE_URL + case_pk + VIEW_TEAM_ADVICE_URL + team_pk)
    return data.json(), data.status_code


def coalesce_user_advice(request, case_pk):
    data = get(request, CASE_URL + case_pk + TEAM_ADVICE_URL)
    return data.json(), data.status_code


def clear_team_advice(request, case_pk):
    data = delete(request, CASE_URL + case_pk + TEAM_ADVICE_URL)
    return data.json(), data.status_code


def get_final_decision_documents(request, case_pk):
    data = get(request, CASE_URL + str(case_pk) + "/final-advice-documents/")
    return data.json(), data.status_code


def grant_licence(request, case_pk, _):
    data = put(request, CASE_URL + str(case_pk) + FINALISE_CASE_URL, {})
    return data.json(), data.status_code


def get_licence(request, case_pk):
    data = get(request, CASE_URL + case_pk + FINALISE_CASE_URL)
    return data.json(), data.status_code


def coalesce_team_advice(request, case_pk):
    data = get(request, CASE_URL + case_pk + FINAL_ADVICE_URL)
    return data.json(), data.status_code


def clear_final_advice(request, case_pk):
    data = delete(request, CASE_URL + case_pk + FINAL_ADVICE_URL)
    return data.json(), data.status_code


def get_good_countries_decisions(request, case_pk):
    data = get(request, CASE_URL + str(case_pk) + "/goods-countries-decisions/")
    return data.json()


def post_good_countries_decisions(request, pk, json):
    response = post(request, CASE_URL + str(pk) + "/goods-countries-decisions/", json)
    return response.json(), response.status_code


def post_user_case_advice(request, pk, json):
    response = post(request, CASE_URL + str(pk) + USER_ADVICE_URL, json)
    return response.json(), response.status_code


def post_team_case_advice(request, pk, json):
    response = post(request, CASE_URL + str(pk) + TEAM_ADVICE_URL, json)
    return response.json(), response.status_code


def post_final_case_advice(request, pk, json):
    response = post(request, CASE_URL + str(pk) + FINAL_ADVICE_URL, json)
    return response.json(), response.status_code


def get_document(request, pk):
    data = get(request, DOCUMENTS_URL + pk)
    return data.json(), data.status_code


# ECJU Queries
def get_ecju_queries(request, pk):
    data = get(request, CASE_URL + pk + ECJU_QUERIES_URL)
    return data.json(), data.status_code


def post_ecju_query(request, pk, json):
    response = post(request, CASE_URL + str(pk) + ECJU_QUERIES_URL, json)
    return response.json(), response.status_code


def get_good(request, pk):
    data = get(request, GOOD_URL + pk)
    return data.json(), data.status_code


def get_goods_type(request, pk):
    data = get(request, GOODS_TYPE_URL + pk)
    # API doesn't structure the endpoints in a way that flags (currently) works,
    # so wrap data in dictionary
    return {"good": data.json()}, data.status_code


def post_review_goods(request, case_id, json):
    json = {
        "objects": request.GET.getlist("goods", request.GET.getlist("goods_types")),
        "comment": request.POST.get("comment"),
        "control_list_entries": request.POST.getlist("control_list_entries[]", []),
        "is_good_controlled": request.POST.get("is_good_controlled"),
        "report_summary": request.POST.get("report_summary"),
    }
    response = post(request, GOOD_CLC_REVIEW_URL + str(case_id) + "/", json)
    return response.json(), response.status_code


# Good Flags
def get_flags_for_team_of_level(request, level, team_id, include_system_flags=False):
    """
    :param request: headers for the request
    :param level: 'cases', 'goods'
    :param include_system_flags: used to indicate adding system flags to list of team flags returned
    :return:
    """
    data = get(request, FLAGS_URL + convert_parameters_to_query_params(locals()) + "&disable_pagination=True")
    return data.json(), data.status_code


def put_flag_assignments(request, json):
    data = put(request, ASSIGN_FLAGS_URL, json)
    return data.json(), data.status_code


def _generate_post_data_and_errors(keys, request_data, action):
    post_data = []
    errors = {}
    for key in keys:
        good_pk = key.split(".")[0]
        country_pk = key.split(".")[1]
        if key not in request_data and not action == "save":
            if good_pk in errors:
                errors[good_pk].append(country_pk)
            else:
                errors[good_pk] = [country_pk]
        else:
            post_data.append({"good": good_pk, "country": country_pk, "decision": request_data.get(key)})
    return post_data, errors


# Letter template decisions
def get_decisions(request):
    data = get(request, DECISIONS_URL)
    return data.json()["decisions"], data.status_code


# Generated Documents
def post_generated_document(request, pk, json):
    data = post(request, CASE_URL + pk + GENERATED_DOCUMENTS_URL, json)
    return data.status_code


def get_generated_document_preview(request, pk, template, text, addressee):
    params = convert_parameters_to_query_params(locals())
    data = get(request, CASE_URL + pk + GENERATED_DOCUMENTS_PREVIEW_URL + params)
    return data.json(), data.status_code


def get_generated_document(request, pk, dpk):
    data = get(request, CASE_URL + str(pk) + GENERATED_DOCUMENTS_URL + str(dpk) + "/")
    return data.json(), data.status_code


def get_destination(request, pk):
    data = get(request, DESTINATION_URL + pk)
    return data.json()


def put_case_officer(request, pk, json):
    data = put(request, CASE_URL + str(pk) + CASE_OFFICER_URL, json)
    return data.json(), data.status_code


def delete_case_officer(request, pk, *args):
    data = delete(request, CASE_URL + str(pk) + CASE_OFFICER_URL)
    return data.json(), data.status_code


def get_case_applicant(request, pk):
    response = get(request, CASE_URL + str(pk) + APPLICANT_URL)
    return response.json()


def get_case_additional_contacts(request, pk):
    response = get(request, CASE_URL + str(pk) + "/additional-contacts/")
    return response.json()


def post_case_additional_contacts(request, pk, json):
    response = post(request, CASE_URL + str(pk) + "/additional-contacts/", json)
    return response.json(), response.status_code


def put_rerun_case_routing_rules(request, pk, json):
    response = put(request, CASE_URL + str(pk) + "/rerun-routing-rules/", {})
    return response.json(), response.status_code


def get_blocking_flags(request, case_pk):
    data = get(
        request,
        FLAGS_URL + f"?case={case_pk}&status={FlagStatus.ACTIVE.value}&blocks_approval=True&disable_pagination=True",
    )
    return data.json()


def get_compliance_licences(request, case_id, reference, page):
    data = get(request, COMPLIANCE_URL + case_id + COMPLIANCE_LICENCES_URL + f"?reference={reference}&page={page}",)
    return data.json()


def post_create_compliance_visit(request, case_id):
    data = post(request, COMPLIANCE_URL + COMPLIANCE_SITE_URL + case_id + "/" + COMPLIANCE_VISIT_URL, request_data={})
    return data


def get_compliance_visit_case(request, case_id):
    data = get(request, COMPLIANCE_URL + COMPLIANCE_VISIT_URL + str(case_id))
    return data.json()


def patch_compliance_visit_case(request, case_id, json):
    if "visit_date_day" in json:
        json["visit_date"] = format_date(json, "visit_date_")
    data = patch(request, COMPLIANCE_URL + COMPLIANCE_VISIT_URL + str(case_id), request_data=json)
    return data.json(), data.status_code


def get_compliance_people_present(request, case_id):
    data = get(
        request,
        COMPLIANCE_URL
        + COMPLIANCE_VISIT_URL
        + str(case_id)
        + "/"
        + COMPLIANCE_PEOPLE_PRESENT_URL
        + "?disable_pagination=True",
    )
    return data.json()


def post_compliance_person_present(request, case_id, json):
    data = post(
        request,
        COMPLIANCE_URL + COMPLIANCE_VISIT_URL + str(case_id) + "/" + COMPLIANCE_PEOPLE_PRESENT_URL,
        request_data=json,
    )

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
                    translated_errors["name-" + str(index)] = [str(index) + ". " + error.pop("name")[0]]
                if "job_title" in error:
                    translated_errors["job-title-" + str(index)] = [str(index) + ". " + error.pop("job_title")[0]]
            index += 1

        return {**json, "errors": translated_errors}, data.status_code
    return data.json(), data.status_code
