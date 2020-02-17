from django.shortcuts import render

from applications.helpers.task_list_sections import (
    get_reference_number_description,
    get_edit_type,
)
from applications.helpers.validate_status import check_all_parties_have_a_document
from applications.services import (
    get_application_countries,
    get_application_goods_types,
    get_application_goods,
    get_additional_documents,
)
from conf.constants import (
    HMRC_QUERY,
    OPEN_LICENCE,
    STANDARD_LICENCE,
    EXHIBITION_CLEARANCE,
    F680_CLEARANCE,
    GIFTING_CLEARANCE,
    NOT_STARTED,
    DONE,
    IN_PROGRESS,
    Permissions,
)
from core.services import get_sites_on_draft, get_external_locations_on_draft
from lite_content.lite_exporter_frontend.strings import applications
from roles.services import get_user_permissions


def get_application_task_list(request, application, errors=None):
    """
    Returns a correctly formatted task list page for the supplied application
    """
    if application["application_type"]["key"] == HMRC_QUERY:
        return _get_hmrc_query_task_list(request, application)
    else:
        return _get_task_list(request, application, errors)


def _get_strings(application_type):
    if application_type == STANDARD_LICENCE:
        return applications.StandardApplicationTaskList
    elif application_type == OPEN_LICENCE:
        return applications.OpenApplicationTaskList
    elif application_type == HMRC_QUERY:
        return applications.HMRCApplicationTaskList
    elif application_type == EXHIBITION_CLEARANCE:
        return applications.ExhibitionClearanceTaskList
    elif application_type == F680_CLEARANCE:
        return applications.F680ClearanceTaskList
    elif application_type == GIFTING_CLEARANCE:
        return applications.GiftingClearanceTaskList
    else:
        raise NotImplementedError(f"No string class for given for {application_type}")


def _get_task_list(request, application, errors=None):
    user_permissions = get_user_permissions(request)
    additional_documents, _ = get_additional_documents(request, application["id"])
    sites, _ = get_sites_on_draft(request, application["id"])
    external_locations, _ = get_external_locations_on_draft(request, application["id"])
    application_type = application["application_type"]["key"]
    edit = get_edit_type(application)

    context = {
        "strings": _get_strings(application_type),
        "application": application,
        "application_type": application_type,
        "is_editing": edit[0],
        "edit_type": edit[1],
        "errors": errors,
        "can_submit": Permissions.SUBMIT_LICENCE_APPLICATION in user_permissions,
        "supporting_documents": additional_documents["documents"],
        "locations": sites["sites"] or external_locations["external_locations"],
    }

    if application_type == STANDARD_LICENCE:
        context["reference_number_description"] = get_reference_number_description(application)

    if application_type == OPEN_LICENCE:
        context["countries"] = get_application_countries(request, application["id"])
        context["goodstypes"] = get_application_goods_types(request, application["id"])
    else:
        context["goods"] = get_application_goods(request, application["id"])
        context["ultimate_end_users_required"] = True in [good["is_good_incorporated"] for good in context["goods"]]

    return render(request, "applications/task-list.html", context)


def _get_hmrc_query_task_list(request, application):
    context = {
        "application": application,
        "goods_types_status": DONE if application["goods_types"] else NOT_STARTED,
        "goods_locations_status": DONE
        if application["goods_locations"] or application["have_goods_departed"]
        else NOT_STARTED,
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

    return render(request, "applications/hmrc-application.html", context)
