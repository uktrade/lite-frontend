from django.shortcuts import render

from exporter.applications.helpers.check_your_answers import _is_application_export_type_temporary
from exporter.applications.helpers.parties import party_requires_ec3_document
from exporter.applications.helpers.task_list_sections import (
    get_reference_number_description,
    get_edit_type,
    get_route_of_goods,
    get_temporary_export_details,
    get_product_location_and_journey_details,
    get_security_approval_details,
)
from exporter.applications.services import (
    get_application_goods,
    get_additional_documents,
    get_case_notes,
)
from exporter.core.constants import (
    PartyDocumentType,
    Permissions,
)
from lite_content.lite_exporter_frontend.strings import applications
from exporter.organisation.roles.services import get_user_permissions


def get_application_task_list(request, application, errors=None):
    user_permissions = get_user_permissions(request)
    additional_documents, _ = get_additional_documents(request, application["id"])
    application_type = application.sub_type
    is_editing, edit_type = get_edit_type(application)

    context = {
        "strings": applications.StandardApplicationTaskList,
        "application": application,
        "application_type": application_type,
        "is_editing": is_editing,
        "edit_type": edit_type,
        "licence_type": applications.ApplicationPage.Summary.Licence.STANDARD,
        "errors": errors,
    }

    require_ec3 = party_requires_ec3_document(application)
    end_user = application.get("end_user", {})
    ec3_details_available = False
    if end_user:
        ec3_document_available = any(
            document["type"] == PartyDocumentType.END_USER_EC3_DOCUMENT for document in end_user["documents"]
        )
        ec3_details_available = ec3_document_available or end_user["ec3_missing_reason"]

    context["show_ec3_banner"] = require_ec3 and not ec3_details_available
    context["can_submit"] = Permissions.SUBMIT_LICENCE_APPLICATION in user_permissions
    context["supporting_documents"] = additional_documents["documents"]
    context["locations"] = get_product_location_and_journey_details(application)
    context["notes"] = get_case_notes(request, application["id"])["case_notes"]

    context["security_approvals"] = get_security_approval_details(application)
    context["reference_number_description"] = get_reference_number_description(application)
    context["route_of_goods"] = get_route_of_goods(application)
    context["goods"] = get_application_goods(request, application["id"])
    context["ultimate_end_users_required"] = any(
        good.get("is_onward_exported") or good.get("is_good_incorporated") for good in context["goods"]
    )
    if _is_application_export_type_temporary(application):
        context["temporary_export_details"] = get_temporary_export_details(application)

    return render(request, "applications/task-list.html", context)
