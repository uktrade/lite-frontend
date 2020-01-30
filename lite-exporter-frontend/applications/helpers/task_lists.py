from django.shortcuts import render

from applications.helpers.check_your_answers import get_total_goods_value
from applications.helpers.get_application_edit_type import get_application_edit_type
from applications.helpers.task_list_sections import (
    get_reference_number_description,
    get_edit_type,
    get_end_user_document_section,
    get_consignee_document_section,
    get_ultimate_end_users_section,
)
from applications.helpers.validate_status import check_all_parties_have_a_document
from applications.services import (
    get_application_countries,
    get_application_goods_types,
    get_third_parties,
    get_application_goods,
    get_additional_documents,
)
from conf.constants import (
    EXHIBITION_CLEARANCE,
    HMRC_QUERY,
    OPEN_LICENCE,
    STANDARD_LICENCE,
    NOT_STARTED,
    DONE,
    IN_PROGRESS,
    Permissions,
)
from core.services import get_sites_on_draft, get_external_locations_on_draft
from roles.services import get_user_permissions


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
    elif application["application_type"]["key"] == EXHIBITION_CLEARANCE:
        return _get_clearance_application_task_list(request, application, errors)
    else:
        raise NotImplementedError()


def _get_standard_application_task_list(request, application, errors=None):
    reference_number_description = get_reference_number_description(application)
    return get_standard_task_list(
        request, application, "applications/task-lists/standard-application.html", reference_number_description, errors
    )


def _get_clearance_application_task_list(request, application, errors=None):
    return get_standard_task_list(
        request, application, "applications/task-lists/clearance-application.html", None, errors
    )


def get_standard_task_list(request, application, template, reference_number_description=None, errors=None):
    application_id = application["id"]
    ultimate_end_users_required = False
    countries_on_goods_types = False

    is_editing, edit_type = get_edit_type(application)
    sites, _ = get_sites_on_draft(request, application_id)
    external_locations, _ = get_external_locations_on_draft(request, application_id)
    additional_documents, _ = get_additional_documents(request, application_id)
    end_user_document = get_end_user_document_section(request, application)
    consignee_document = get_consignee_document_section(request, application)
    ultimate_end_users, ultimate_end_users_documents_complete = get_ultimate_end_users_section(request, application)
    third_parties = get_third_parties(request, application_id)
    goods = get_application_goods(request, application_id)

    for good in goods:
        if good["is_good_incorporated"]:
            ultimate_end_users_required = True

    user_permissions = get_user_permissions(request)
    submit = Permissions.SUBMIT_LICENCE_APPLICATION in user_permissions

    context = {
        "application": application,
        "is_editing": is_editing,
        "edit_type": edit_type,
        "end_user_status": check_all_parties_have_a_document([application["end_user"]]),
        "consignee_status": DONE if application["consignee"] else NOT_STARTED,
        "reference_number_description": reference_number_description,
        "locations": sites or external_locations["external_locations"],
        "goods": goods,
        "goods_value": get_total_goods_value(goods),
        "ultimate_end_users": ultimate_end_users,
        "ultimate_end_users_required": ultimate_end_users_required,
        "ultimate_end_users_documents_complete": ultimate_end_users_documents_complete,
        "end_user_document": end_user_document,
        "consignee_document": consignee_document,
        "countries_on_goods_types": countries_on_goods_types,
        "third_parties": third_parties,
        "supporting_documents": additional_documents["documents"],
        "errors": errors,
        "can_submit": submit,
    }
    return render(request, template, context)


def _get_open_application_task_list(request, application, errors=None):
    application_id = application["id"]

    # Add the editing type (if possible) to the context to make it easier to read/change in the future
    edit_type = get_application_edit_type(application)

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

    user_permissions = get_user_permissions(request)
    submit = Permissions.SUBMIT_LICENCE_APPLICATION in user_permissions

    context = {
        "application": application,
        "edit_type": edit_type,
        "countries": countries,
        "goodstypes": goodstypes,
        "locations": sites or external_locations["external_locations"],
        "ultimate_end_users": ultimate_end_users,
        "ultimate_end_users_required": ultimate_end_users_required,
        "end_user_document": end_user_document,
        "consignee_document": consignee_document,
        "countries_on_goods_types": countries_on_goods_types,
        "third_parties": third_parties,
        "supporting_documents": additional_documents["documents"],
        "errors": errors,
        "can_submit": submit,
    }
    return render(request, "applications/task-lists/open-application.html", context)


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

    return render(request, "applications/task-lists/hmrc-application.html", context)
