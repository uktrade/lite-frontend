from _decimal import Decimal

from django.urls import reverse
from django.utils.safestring import mark_safe

from exporter.applications.helpers.countries import ContractTypes
from exporter.applications.helpers.parties import party_requires_ec3_document
from exporter.core.constants import (
    TEMPORARY,
    PERMANENT,
    PartyDocumentType,
)
from core.constants import SecurityClassifiedApprovalsType
from core.builtins.custom_tags import (
    default_na,
    friendly_boolean,
    get_address,
    pluralise_quantity,
    verbose_goods_starting_point,
    str_date_only,
    sentence_case,
    list_to_choice_labels,
)
from exporter.core.helpers import convert_to_link, convert_control_list_entries
from exporter.goods.helpers import requires_serial_numbers
from exporter.applications.constants import ApplicationStatus

from lite_content.lite_exporter_frontend import applications
from lite_content.lite_exporter_frontend.strings import Parties


def convert_application_to_check_your_answers(application, editable=False, is_summary=False):
    strings = applications.ApplicationSummaryPage
    pk = application["id"]
    url = reverse(f"applications:good_detail_summary", kwargs={"pk": pk})
    old_locations = bool(application["goods_locations"])
    converted = {
        convert_to_link(url, strings.GOODS): convert_goods_on_application(
            application, application["goods"], is_summary=is_summary
        ),
        strings.END_USE_DETAILS: _get_end_use_details(application),
        strings.END_USER: convert_party(application["end_user"], application, editable),
        strings.CONSIGNEE: convert_party(application["consignee"], application, editable),
        strings.THIRD_PARTIES: [convert_party(item, application, editable) for item in application["third_parties"]],
        strings.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(application["additional_documents"], pk),
    }

    security_approvals = {"Do you have a security approval?": _get_security_approvals(application)}
    converted = {**security_approvals, **converted}

    if old_locations:
        converted[strings.ROUTE_OF_GOODS] = _get_route_of_goods(application)
        converted[strings.GOODS_LOCATIONS] = _convert_goods_locations(application["goods_locations"])
        if _is_application_export_type_temporary(application):
            converted[strings.TEMPORARY_EXPORT_DETAILS] = _get_temporary_export_details(application)
    else:
        product_location = {"Product location and journey": _get_product_location_and_journey(application)}
        converted = {**product_location, **converted}

    if has_ultimate_end_users(application) and has_incorporated_goods_on_application(application):
        ultimate_end_users = [convert_party(item, application, editable) for item in application["ultimate_end_users"]]
        converted[strings.ULTIMATE_END_USERS] = ultimate_end_users

    return converted


def convert_goods_on_application(application, goods_on_application, is_exhibition=False, is_summary=False):
    converted = []

    def requires_actions(application, good_on_application):
        return not is_summary and requires_serial_numbers(application, good_on_application)

    requires_actions_column = any(requires_actions(application, g) for g in goods_on_application)
    for good_on_application in goods_on_application:
        # When it is in Draft stage it will show all CLEs otherwise it will show the ones assessed by TAU
        if application["status"].get("key") == ApplicationStatus.DRAFT:
            control_list_entries = convert_control_list_entries(good_on_application["good"]["control_list_entries"])
        else:
            control_list_entries = convert_control_list_entries(good_on_application["control_list_entries"])

        if good_on_application["good"].get("name"):
            name = good_on_application["good"]["name"]
        else:
            name = good_on_application["good"]["description"]

        item = {
            "Name": name,
            "Part number": default_na(good_on_application["good"]["part_number"]),
            "Control list entries": mark_safe(control_list_entries),  # noqa: S308
        }
        if is_exhibition:
            item["Product type"] = good_on_application["other_item_type"] or good_on_application["item_type"]
        else:
            item["Quantity"] = pluralise_quantity(good_on_application)
            item["Value"] = f"£{good_on_application['value']}"
        if requires_actions(application, good_on_application):
            update_serial_numbers_url = reverse(
                "applications:update_serial_numbers",
                kwargs={
                    "pk": good_on_application["application"],
                    "good_on_application_pk": good_on_application["id"],
                },
            )
            item[mark_safe('<span class="govuk-visually-hidden">Actions</a>')] = mark_safe(  # noqa: S308
                f'<a class="govuk-link" href="{update_serial_numbers_url}">Add serial numbers</a>'
            )
        elif requires_actions_column:
            item[mark_safe('<span class="govuk-visually-hidden">Actions</a>')] = (  # noqa: S308
                " "  # Not just an empty string or it will get converted into N/A
            )
        converted.append(item)

    return converted


def _get_product_location_and_journey(application):
    is_permanent = application.export_type["key"] == "permanent"
    locations_details = {
        "Where will the products begin their export journey?": verbose_goods_starting_point(
            application["goods_starting_point"]
        ),
        "Are the products being permanently exported?": friendly_boolean(is_permanent),
    }
    if not is_permanent:
        locations_details["Explain why the products are being exported temporarily"] = application.temp_export_details
        locations_details["Will the products remain under your direct control while overseas?"] = (
            application.is_temp_direct_control
        )
        locations_details[
            "Who will be in control of the products while overseas, and what is your relationship to them?"
        ] = application.temp_direct_control_details
        locations_details["Proposed date the products will return to the UK"] = str_date_only(
            application.proposed_return_date
        )

    locations_details["Are the products being shipped from the UK on an air waybill or bill of lading?"] = (
        friendly_boolean(application.is_shipped_waybill_or_lading)
    )

    if not application.is_shipped_waybill_or_lading:
        locations_details["Route details"] = application.non_waybill_or_lading_route_details

    locations_details["Who are the products going to?"] = sentence_case(application.goods_recipients)
    return locations_details


def _get_security_approvals(application):
    security_details = {
        "Do you have an MOD security approval, such as F680 or F1686?": friendly_boolean(
            application.is_mod_security_approved
        )
    }

    if application.is_mod_security_approved:
        security_details["What type of approval do you have?"] = list_to_choice_labels(
            application.security_approvals, SecurityClassifiedApprovalsType
        )
        if SecurityClassifiedApprovalsType.F680 in application.security_approvals:
            itar_question = "Are any products on this application subject to ITAR controls?"
            security_details[itar_question] = friendly_boolean(application.subject_to_itar_controls)
            security_details["What is the F680 reference number?"] = application.f680_reference_number

        if SecurityClassifiedApprovalsType.F1686 in application.security_approvals:
            security_details["What is the F1686 reference number?"] = application.f1686_reference_number
            security_details["When was the F1686 approved?"] = str_date_only(application.f1686_approval_date)

        if SecurityClassifiedApprovalsType.OTHER in application.security_approvals:
            security_details["Provide details of your written approval"] = application.other_security_approval_details

    return security_details


def convert_country_contract_types(country):
    return default_na(
        "\n".join(
            [
                (
                    ContractTypes.get_str_representation(ContractTypes(contract_type))
                    if contract_type != "other_contract_type"
                    else "Other contract type - " + country["other_contract_type_text"]
                )
                for contract_type in country["contract_types"]
            ]
        )
    )


def _get_route_of_goods(application):
    return [
        {
            "Description": "Shipped air waybill or lading",
            "Answer": friendly_boolean(application.get("is_shipped_waybill_or_lading"))
            + "\n"
            + (application.get("non_waybill_or_lading_route_details") or ""),
        }
    ]


def _get_end_use_details(application):
    fields = [
        ("intended_end_use", "", applications.EndUseDetails.CheckYourAnswers.INTENDED_END_USE_TITLE),
        (
            "is_military_end_use_controls",
            "military_end_use_controls_ref",
            applications.EndUseDetails.CheckYourAnswers.INFORMED_TO_APPLY_TITLE,
        ),
        ("is_informed_wmd", "informed_wmd_ref", applications.EndUseDetails.CheckYourAnswers.INFORMED_WMD_TITLE),
        ("is_suspected_wmd", "suspected_wmd_ref", applications.EndUseDetails.CheckYourAnswers.SUSPECTED_WMD_TITLE),
        ("is_eu_military", "", applications.EndUseDetails.CheckYourAnswers.EU_MILITARY_TITLE),
        (
            "is_compliant_limitations_eu",
            "compliant_limitations_eu_ref",
            applications.EndUseDetails.CheckYourAnswers.COMPLIANT_LIMITATIONS_EU_TITLE,
        ),
    ]

    values_to_print = []
    for main_field, ref_field, display_string in fields:
        ds = {}
        if application.get(main_field) is not None:
            ds["Description"] = display_string
            if not isinstance(application.get(main_field), str):
                ds["Answer"] = friendly_boolean(application.get(main_field)) + "\n" + (application.get(ref_field) or "")
            else:
                ds["Answer"] = application.get(main_field)
        if ds:
            values_to_print.append(ds)

    return values_to_print


def _get_temporary_export_details(application):
    if _is_application_export_type_temporary(application):
        fields = [
            ("temp_export_details", applications.TemporaryExportDetails.CheckYourAnswers.TEMPORARY_EXPORT_DETAILS),
            (
                "is_temp_direct_control",
                applications.TemporaryExportDetails.CheckYourAnswers.PRODUCTS_UNDER_DIRECT_CONTROL,
            ),
            ("proposed_return_date", applications.TemporaryExportDetails.CheckYourAnswers.PROPOSED_RETURN_DATE),
        ]

        values_to_print = []
        for field, display_string in fields:
            display_entry = {}
            if application.get(field) is not None:
                display_entry["Description"] = display_string
                display_entry["Answer"] = (
                    friendly_boolean(application.get(field))
                    + "\n"
                    + (application.get("temp_direct_control_details") or "")
                    if field == "is_temp_direct_control"
                    else application.get(field)
                )
            if display_entry:
                values_to_print.append(display_entry)

        return values_to_print


def get_end_user_data(application, party, editable):
    data = {}
    document_availability_key = "Do you have an end-user document?"
    if party["end_user_document_available"]:
        data[document_availability_key] = "Yes"
        for doc in party["documents"]:
            if doc["type"] == PartyDocumentType.END_USER_UNDERTAKING_DOCUMENT:
                document_type = "End user document"
            elif doc["type"] == PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT:
                document_type = "English translation of the end user document"
            elif doc["type"] == PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT:
                document_type = "Document on company letterhead"
            else:
                continue

            data[document_type] = _convert_end_user_document(application["id"], party["id"], doc, editable)

            if doc["type"] == PartyDocumentType.END_USER_UNDERTAKING_DOCUMENT and party["product_differences_note"]:
                key = "Describe any differences between products listed in the document and products on the application (optional)"
                data[key] = party["product_differences_note"]
    else:
        data[document_availability_key] = "No, I do not have an end-user undertaking or stockist undertaking"
        document_key_heading = "Explain why you do not have an end-user undertaking or stockist undertaking"
        data[document_key_heading] = party["end_user_document_missing_reason"]

    ec3_required = party_requires_ec3_document(application)
    if ec3_required:
        ec3_document = [
            document for document in party["documents"] if document["type"] == PartyDocumentType.END_USER_EC3_DOCUMENT
        ]
        if not ec3_document and not party["ec3_missing_reason"]:
            data["Upload an EC3 form (optional)"] = " "
            data["If you do not have an EC3 form, explain why (optional)"] = " "
        else:
            if ec3_document:
                data["Upload an EC3 form (optional)"] = _convert_end_user_document(
                    application["id"], party["id"], ec3_document[0], editable
                )
            elif party["ec3_missing_reason"]:
                data["If you do not have an EC3 form, explain why (optional)"] = party["ec3_missing_reason"]

    return data


def convert_party(party, application, editable):
    if not party:
        return {}

    data = {
        "Name": party["name"],
        "Type": party["sub_type_other"] if party["sub_type_other"] else party["sub_type"]["value"],
        "Address": get_address(party),
        "Website": convert_to_link(party["website"]),
    }

    if party["type"] == "third_party":
        data["Role"] = party.get("role_other") if party.get("role_other") else party.get("role").get("value")

    if party["type"] == "end_user":
        data["Signatory name"] = party.get("signatory_name_euu")
        party_data = get_end_user_data(application, party, editable)
        data = dict(data, **party_data)
    else:
        if party.get("document"):
            party_type = party["type"]
            if party["type"] == "third_party":
                party_type = "third-parties"
            document = _convert_document(party, party_type, application["id"], editable)
        else:
            document = convert_to_link(
                reverse(
                    f"applications:{party['type']}_attach_document",
                    kwargs={"pk": application["id"], "obj_pk": party["id"]},
                ),
                "Attach document",
            )

        data["Document"] = document

    return data


def _convert_goods_locations(goods_locations):
    if "type" not in goods_locations:
        return

    if goods_locations["type"] == "sites":
        return [{"Site": site["name"], "Address": get_address(site)} for site in goods_locations["data"]]
    else:
        return [
            {
                "Name": external_location["name"],
                "Address": get_address(external_location),
            }
            for external_location in goods_locations["data"]
        ]


def _get_supporting_documentation(supporting_documentation, application_id):
    return [
        {
            "File name": convert_to_link(
                reverse(
                    "applications:download_additional_document", kwargs={"pk": application_id, "obj_pk": document["id"]}
                ),
                document["name"],
            ),
            "Description": default_na(document["description"]),
        }
        for document in supporting_documentation
    ]


def _convert_end_user_document(application_id, party_id, document, editable):
    if document["safe"] is None:
        return "Processing"

    if not document["safe"]:
        return convert_to_link(
            f"/applications/{application_id}/end-user/{party_id}/document/attach/", Parties.Documents.VIRUS
        )

    if editable:
        return convert_to_link(
            f"/applications/{application_id}/end-user/{party_id}/document/{document['id']}",
            document["name"],
            include_br=True,
        ) + convert_to_link(
            f"/applications/{application_id}/end-user/{party_id}/document/{document['id']}", Parties.Documents.DELETE
        )
    else:
        return convert_to_link(
            f"/applications/{application_id}/end-user/{party_id}/document/{document['id']}",
            document["name"],
            include_br=True,
        )


def _convert_document(party, document_type, application_id, editable):
    document = party.get("document")

    if not document:
        return default_na(None)

    if document["safe"] is None:
        return "Processing"

    if not document["safe"]:
        return convert_to_link(
            f"/applications/{application_id}/{document_type}/{party['id']}/document/attach/", Parties.Documents.VIRUS
        )

    if editable:
        return convert_to_link(
            f"/applications/{application_id}/{document_type}/{party['id']}/document/download",
            "Download",
            include_br=True,
        ) + convert_to_link(
            f"/applications/{application_id}/{document_type}/{party['id']}/document/delete", Parties.Documents.DELETE
        )
    else:
        return convert_to_link(
            f"/applications/{application_id}/{document_type}/{party['id']}/document/download",
            Parties.Documents.DOWNLOAD,
            include_br=True,
        )


def get_total_goods_value(goods: list):
    total_value = 0
    for good in goods:
        total_value += Decimal(good["value"])
    return total_value


def _is_application_export_type_temporary(application):
    return application.get("export_type").get("key") == TEMPORARY


def is_application_export_type_permanent(application):
    return False if not application.get("export_type") else (application.get("export_type").get("key") == PERMANENT)


def has_ultimate_end_users(application):
    return bool(application["ultimate_end_users"])


def has_incorporated_goods_on_application(application):
    for goa in application["goods"]:
        if goa.get("is_good_incorporated") or goa.get("is_onward_incorporated"):
            return True

    return False


def is_application_oiel_of_type(oiel_type, application):
    return (
        False
        if not application.get("goodstype_category")
        else (application.get("goodstype_category").get("key") == oiel_type)
    )
