from applications.services import get_end_user_document, get_consignee_document, get_ultimate_end_users
from conf.constants import APPLICANT_EDITING


def get_reference_number_description(application):
    have_you_been_informed = application["have_you_been_informed"]
    reference_number_on_information_form = application["reference_number_on_information_form"]
    if have_you_been_informed == "yes":
        if not reference_number_on_information_form:
            reference_number_on_information_form = "not provided"
        reference_number_description = "Yes. Reference number: " + reference_number_on_information_form
    else:
        reference_number_description = "No"

    return reference_number_description


def get_edit_type(application):
    # Add the editing type (if possible) to the context to make it easier to read/change in the future
    is_editing = False
    edit_type = None

    if application["status"]:
        is_editing = application["status"]["key"] == "submitted" or application["status"]["key"] == APPLICANT_EDITING
        if is_editing:
            edit_type = "minor_edit" if application["status"]["key"] == "submitted" else "major_edit"

    return is_editing, edit_type


def get_end_user_document_section(request, application):
    if application.get("end_user"):
        end_user_document, _ = get_end_user_document(request, application["id"])
        return end_user_document.get("document")
    else:
        return None


def get_consignee_document_section(request, application):
    if application.get("consignee"):
        consignee_document, _ = get_consignee_document(request, application["id"])
        return consignee_document.get("document")
    else:
        return None


def get_ultimate_end_users_section(request, application):
    ultimate_end_users = get_ultimate_end_users(request, application["id"])
    ultimate_end_users_documents_complete = True

    for ueu in ultimate_end_users:
        if not ueu.get("document"):
            ultimate_end_users_documents_complete = False
            break

    return ultimate_end_users, ultimate_end_users_documents_complete
