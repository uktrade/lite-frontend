from exporter.applications.services import get_party_document, get_ultimate_end_users
from exporter.core.constants import APPLICANT_EDITING


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


def get_route_of_goods(application):
    if application.get("is_shipped_waybill_or_lading") is None:
        return False
    return True


def get_temporary_export_details(application):
    fields = [
        "temp_export_details",
        "is_temp_direct_control",
        "proposed_return_date",
    ]
    for field in fields:
        if application.get(field) is None:
            return False
    return True


def get_product_location_and_journey_details(application):
    """
    Determines if Product Location adn Journey section is complete or not
    """
    fields = [
        "goods_starting_point",
        "export_type",
        "is_shipped_waybill_or_lading",
        "goods_recipients",
    ]
    export_type_temporary = [
        "temp_export_details",
        "is_temp_direct_control",
        "proposed_return_date",
    ]
    temp_direct_control_false = [
        "temp_direct_control_details",
    ]
    is_shipped_waybill_or_lading_false = [
        "non_waybill_or_lading_route_details",
    ]
    for field in fields:
        if application.get(field) is None:
            return False

    if application["export_type"] == "temporary":
        for field in export_type_temporary:
            if application.get(field) is None:
                return False
        if not application["is_temp_direct_control"]:
            for field in temp_direct_control_false:
                if application.get(field) is None:
                    return False
    if not application["is_shipped_waybill_or_lading"]:
        for field in is_shipped_waybill_or_lading_false:
            if application.get(field) is None:
                return False
    return True


def get_security_approval_details(application):
    """
    Determines if security approval journey section is complete or not
    """
    fields = [
        "is_mod_security_approved",
    ]
    for field in fields:
        if application.get(field) is None:
            return False
    return True
