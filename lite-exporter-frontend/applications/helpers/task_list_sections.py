from applications.services import get_party_document, get_ultimate_end_users
from conf.constants import APPLICANT_EDITING, STANDARD, OPEN


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


def get_party_document_section(request, application, party_type):
    if application.get(party_type):
        party_document, _ = get_party_document(request, application["id"], application[party_type]["id"])
        return party_document.get("document")
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


def get_end_use_details(application):
    fields = ["intended_end_use"]
    if application.sub_type in [STANDARD, OPEN]:
        fields += ["is_military_end_use_controls", "is_informed_wmd", "is_suspected_wmd"]
        if application.sub_type == STANDARD:
            fields.append("is_eu_military")
    for field in fields:
        if application.get(field) is None:
            return False
    return True
