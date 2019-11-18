from _decimal import Decimal

from django.shortcuts import render

from applications.libraries.validate_status import check_all_parties_have_a_document
from applications.services import (
    get_application_countries,
    get_application_goods_types,
    get_ultimate_end_users,
    get_third_parties,
    get_application_goods,
    get_end_user_document,
    get_consignee_document,
    get_additional_documents,
)
from conf.constants import HMRC_QUERY, OPEN_LICENCE, STANDARD_LICENCE, APPLICANT_EDITING, NOT_STARTED, DONE, IN_PROGRESS
from core.services import get_sites_on_draft, get_external_locations_on_draft


def get_application_task_list(request, application, errors=None):
    """
    Returns a correctly formatted task list page for the supplied application
    """
    if application["application_type"]["key"] == STANDARD_LICENCE:
        return _get_standard_application_task_list(request, application, errors)
    elif application["application_type"]["key"] == OPEN_LICENCE:
        return _get_open_application_task_list(request, application, errors)
    elif application["application_type"]["key"] == HMRC_QUERY:
        return _get_hmrc_query_task_list(request, application)
    else:
        raise NotImplementedError()


def _get_standard_application_task_list(request, application, errors=None):
    application_id = application["id"]

    # Add the editing type (if possible) to the context to make it easier to read/change in the future
    is_editing = False
    edit_type = None

    reference_number_description = _get_reference_number_description(
        application["have_you_been_informed"], application["reference_number_on_information_form"]
    )

    if application["status"]:
        is_editing = application["status"]["key"] == "submitted" or application["status"]["key"] == APPLICANT_EDITING
        if is_editing:
            edit_type = "minor_edit" if application["status"]["key"] == "submitted" else "major_edit"

    sites, _ = get_sites_on_draft(request, application_id)
    external_locations, _ = get_external_locations_on_draft(request, application_id)
    additional_documents, _ = get_additional_documents(request, application_id)

    ultimate_end_users_required = False
    end_user_document = None
    consignee_document = None
    countries_on_goods_types = False

    ultimate_end_users = get_ultimate_end_users(request, application_id)
    third_parties = get_third_parties(request, application_id)
    end_user = application.get("end_user")
    consignee = application.get("consignee")
    goods = get_application_goods(request, application_id)

    if end_user:
        end_user_document, _ = get_end_user_document(request, application_id)
        end_user_document = end_user_document.get("document")

    if consignee:
        consignee_document, _ = get_consignee_document(request, application_id)
        consignee_document = consignee_document.get("document")

    total_goods_value = 0
    for good in goods:
        total_goods_value += Decimal(good["value"]).quantize(Decimal(".01"))
        if not good["good"]["is_good_end_product"]:
            ultimate_end_users_required = True

    context = {
        "application": application,
        "is_editing": is_editing,
        "edit_type": edit_type,
        "reference_number_description": reference_number_description,
        "sites": sites["sites"],
        "goods": goods,
        "total_goods_value": total_goods_value,
        "external_locations": external_locations["external_locations"],
        "ultimate_end_users": ultimate_end_users,
        "ultimate_end_users_required": ultimate_end_users_required,
        "end_user_document": end_user_document,
        "consignee_document": consignee_document,
        "countries_on_goods_types": countries_on_goods_types,
        "third_parties": third_parties,
        "additional_documents": additional_documents["documents"],
        "errors": errors,
    }
    return render(request, "applications/standard-application-edit.html", context)


def _get_open_application_task_list(request, application, errors=None):
    application_id = application["id"]

    # Add the editing type (if possible) to the context to make it easier to read/change in the future
    is_editing = False
    edit_type = None
    if application["status"]:
        is_editing = application["status"]["key"] == "submitted" or application["status"]["key"] == APPLICANT_EDITING
        if is_editing:
            edit_type = "minor_edit" if application["status"]["key"] == "submitted" else "major_edit"

    reference_number_description = _get_reference_number_description(
        application["have_you_been_informed"], application["reference_number_on_information_form"]
    )

    sites, _ = get_sites_on_draft(request, application_id)
    external_locations, _ = get_external_locations_on_draft(request, application_id)
    additional_documents, _ = get_additional_documents(request, application_id)

    ultimate_end_users = []
    ultimate_end_users_required = False
    third_parties = []
    end_user_document = None
    consignee_document = None
    countries_on_goods_types = False
    goodstypes = get_application_goods_types(request, application_id)
    countries = get_application_countries(request, application_id)

    for good in goodstypes:
        if good["countries"]:
            countries_on_goods_types = True

    context = {
        "application": application,
        "is_editing": is_editing,
        "edit_type": edit_type,
        "reference_number_description": reference_number_description,
        "countries": countries,
        "goodstypes": goodstypes,
        "sites": sites,
        "external_locations": external_locations["external_locations"],
        "ultimate_end_users": ultimate_end_users,
        "ultimate_end_users_required": ultimate_end_users_required,
        "end_user_document": end_user_document,
        "consignee_document": consignee_document,
        "countries_on_goods_types": countries_on_goods_types,
        "third_parties": third_parties,
        "additional_documents": additional_documents["documents"],
        "errors": errors,
    }
    return render(request, "applications/open-application-edit.html", context)


def _get_hmrc_query_task_list(request, application):
    context = {
        "application": application,
        "goods_types_status": DONE if application["goods_types"] else NOT_STARTED,
        "goods_locations_status": DONE if application["goods_locations"] else NOT_STARTED,
        "end_user_status": check_all_parties_have_a_document([application["end_user"]]),
        "ultimate_end_users_status": check_all_parties_have_a_document(application["ultimate_end_users"]),
        "third_parties_status": DONE if application["third_parties"] else NOT_STARTED,
        "consignee_status": DONE if application["consignee"] else NOT_STARTED,
        "supporting_documentation_status": DONE if application["supporting_documentation"] else NOT_STARTED,
        "optional_note_status": DONE if application["reasoning"] else NOT_STARTED,
    }

    context["show_submit_button"] = (
        context["goods_types_status"] == DONE
        and context["goods_locations_status"] == DONE
        and context["end_user_status"] == DONE
        and context["ultimate_end_users_status"] != IN_PROGRESS
    )

    return render(request, "hmrc/task-list.html", context)


def _get_reference_number_description(have_you_been_informed: str, reference_number_on_information_form):
    if have_you_been_informed == "yes":
        if not reference_number_on_information_form:
            reference_number_on_information_form = "not provided"
        reference_number_description = "Yes. Reference number: " + reference_number_on_information_form
    else:
        reference_number_description = "No"

    return reference_number_description
