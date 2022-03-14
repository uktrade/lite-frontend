from _decimal import Decimal

from django.urls import reverse
from django.utils.safestring import mark_safe

from exporter.applications.helpers.countries import ContractTypes
from exporter.core.constants import (
    STANDARD,
    OPEN,
    HMRC,
    EXHIBITION,
    GIFTING,
    F680,
    TEMPORARY,
    PERMANENT,
    CaseTypes,
    APPLICATION_TYPE_STRINGS,
    PartyDocumentType,
)
from core.constants import GoodsTypeCategory
from core.builtins.custom_tags import (
    default_na,
    friendly_boolean,
    date_display,
    get_address,
    pluralise_quantity,
    verbose_goods_starting_point,
    str_date_only,
    sentence_case,
)
from exporter.core.helpers import convert_to_link, convert_control_list_entries
from lite_content.lite_exporter_frontend import applications
from lite_content.lite_exporter_frontend.strings import Parties
from lite_forms.helpers import conditional


def convert_application_to_check_your_answers(application, editable=False, summary=False):
    """
    Returns a correctly formatted check your answers page for the supplied application
    """
    sub_type = application.sub_type
    if sub_type == STANDARD:
        return _convert_standard_application(application, editable, is_summary=summary)
    elif sub_type == OPEN:
        return _convert_open_application(application, editable)
    elif sub_type == HMRC:
        return _convert_hmrc_query(application, editable)
    elif sub_type == EXHIBITION:
        return _convert_exhibition_clearance(application, editable)
    elif sub_type == GIFTING:
        return _convert_gifting_clearance(application, editable)
    elif sub_type == F680:
        return _convert_f680_clearance(application, editable)
    else:
        raise NotImplementedError()


def _convert_exhibition_clearance(application, editable=False):
    return {
        applications.ApplicationSummaryPage.EXHIBITION_DETAILS: _get_exhibition_details(application),
        applications.ApplicationSummaryPage.GOODS: convert_goods_on_application(application["goods"], True),
        applications.ApplicationSummaryPage.GOODS_LOCATIONS: _convert_goods_locations(application["goods_locations"]),
        applications.ApplicationSummaryPage.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(
            application["additional_documents"], application["id"]
        ),
    }


def _convert_f680_clearance(application, editable=False):
    return {
        applications.ApplicationSummaryPage.GOODS: convert_goods_on_application(application["goods"]),
        applications.ApplicationSummaryPage.ADDITIONAL_INFORMATION: _get_additional_information(application),
        applications.ApplicationSummaryPage.END_USE_DETAILS: _get_end_use_details(application),
        applications.ApplicationSummaryPage.END_USER: convert_party(application["end_user"], application, editable),
        applications.ApplicationSummaryPage.THIRD_PARTIES: [
            convert_party(party, application, editable) for party in application["third_parties"]
        ],
        applications.ApplicationSummaryPage.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(
            application["additional_documents"], application["id"]
        ),
    }


def _convert_gifting_clearance(application, editable=False):
    return {
        applications.ApplicationSummaryPage.GOODS: convert_goods_on_application(application["goods"]),
        applications.ApplicationSummaryPage.END_USER: convert_party(application["end_user"], application, editable),
        applications.ApplicationSummaryPage.THIRD_PARTIES: [
            convert_party(party, application, editable) for party in application["third_parties"]
        ],
        applications.ApplicationSummaryPage.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(
            application["additional_documents"], application["id"]
        ),
    }


def _convert_standard_application(application, editable=False, is_summary=False):
    strings = applications.ApplicationSummaryPage
    pk = application["id"]
    url = reverse(f"applications:good_detail_summary", kwargs={"pk": pk})
    old_locations = bool(application["goods_locations"])
    converted = {
        convert_to_link(url, strings.GOODS): convert_goods_on_application(application["goods"], is_summary=is_summary),
        strings.END_USE_DETAILS: _get_end_use_details(application),
        strings.END_USER: convert_party(application["end_user"], application, editable),
        strings.CONSIGNEE: convert_party(application["consignee"], application, editable),
        strings.THIRD_PARTIES: [convert_party(item, application, editable) for item in application["third_parties"]],
        strings.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(application["additional_documents"], pk),
    }
    if old_locations:
        converted[strings.ROUTE_OF_GOODS] = _get_route_of_goods(application)
        converted[strings.GOODS_LOCATIONS] = _convert_goods_locations(application["goods_locations"])
        if _is_application_export_type_temporary(application):
            converted[strings.TEMPORARY_EXPORT_DETAILS] = _get_temporary_export_details(application)
    else:
        product_location = {"Product location and journey": _get_product_location_and_journey(application)}
        converted = {**product_location, **converted}
    if has_incorporated_goods(application):
        ultimate_end_users = [convert_party(item, application, editable) for item in application["ultimate_end_users"]]
        converted[strings.ULTIMATE_END_USERS] = ultimate_end_users
    return converted


def _convert_open_application(application, editable=False):
    return {
        **(
            {
                applications.ApplicationSummaryPage.GOODS_CATEGORIES: _get_goods_categories(application),
            }
            if application.case_type["reference"]["key"] == CaseTypes.OIEL
            and application.goodstype_category["key"]
            in [GoodsTypeCategory.MILITARY, GoodsTypeCategory.UK_CONTINENTAL_SHELF]
            else {}
        ),
        applications.ApplicationSummaryPage.GOODS: _convert_goods_types(application["goods_types"]),
        **(
            {
                applications.ApplicationSummaryPage.END_USE_DETAILS: _get_end_use_details(application),
            }
            if not is_application_oiel_of_type("cryptographic", application)
            else {}
        ),
        **(
            {
                applications.ApplicationSummaryPage.ROUTE_OF_GOODS: _get_route_of_goods(application),
            }
            if not is_application_oiel_of_type("cryptographic", application)
            else {}
        ),
        **(
            {
                applications.ApplicationSummaryPage.TEMPORARY_EXPORT_DETAILS: _get_temporary_export_details(
                    application
                ),
            }
            if _is_application_export_type_temporary(application)
            else {}
        ),
        **(
            {
                applications.ApplicationSummaryPage.GOODS_LOCATIONS: _convert_goods_locations(
                    application["goods_locations"]
                ),
            }
            if not is_application_oiel_of_type("cryptographic", application)
            else {}
        ),
        **(
            {
                applications.ApplicationSummaryPage.END_USER: [
                    convert_party(application["end_user"], application, editable)
                ],
            }
            if is_open_application_with_end_user(application)
            else {}
        ),
        applications.ApplicationSummaryPage.COUNTRIES: _convert_countries(application["destinations"]["data"]),
        **(
            {
                applications.ApplicationSummaryPage.ULTIMATE_END_USERS: [
                    convert_party(party, application, editable) for party in application["ultimate_end_users"]
                ],
            }
            if has_incorporated_goods_types(application)
            and application["goodstype_category"]["key"] == GoodsTypeCategory.MILITARY
            else {}
        ),
        applications.ApplicationSummaryPage.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(
            application["additional_documents"], application["id"]
        ),
        **(
            {
                applications.ApplicationSummaryPage.THIRD_PARTIES: [
                    convert_party(party, application, editable) for party in application["third_parties"]
                ],
            }
            if is_application_oiel_of_type("cryptographic", application)
            else {}
        ),
    }


def _convert_hmrc_query(application, editable=False):
    return {
        applications.ApplicationSummaryPage.ON_BEHALF_OF: application["organisation"]["name"],
        applications.ApplicationSummaryPage.GOODS: _convert_goods_types(application["goods_types"]),
        applications.ApplicationSummaryPage.GOODS_LOCATIONS: conditional(
            application["have_goods_departed"],
            {applications.ApplicationSummaryPage.GOODS_DEPARTED: "Yes"},
            _convert_goods_locations(application["goods_locations"]),
        ),
        applications.ApplicationSummaryPage.END_USER: convert_party(application["end_user"], application, editable),
        applications.ApplicationSummaryPage.ULTIMATE_END_USERS: [
            convert_party(party, application, editable) for party in application["ultimate_end_users"]
        ],
        applications.ApplicationSummaryPage.THIRD_PARTIES: [
            convert_party(party, application, editable) for party in application["third_parties"]
        ],
        applications.ApplicationSummaryPage.CONSIGNEE: convert_party(application["consignee"], application, editable),
        applications.ApplicationSummaryPage.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(
            application["supporting_documentation"], application["id"]
        ),
        applications.ApplicationSummaryPage.OPTIONAL_NOTE: application["reasoning"],
    }


def convert_goods_on_application(goods_on_application, is_exhibition=False, is_summary=False):
    converted = []

    def requires_actions(good_on_application):
        return not is_summary and requires_serial_numbers(good_on_application)

    requires_actions_column = any(requires_actions(g) for g in goods_on_application)
    for good_on_application in goods_on_application:
        # TAU's review is saved at "good on application" level, while exporter's answer is at good level.
        if good_on_application["good"]["is_good_controlled"] is None:
            is_controlled = "N/A"
        else:
            is_controlled = good_on_application["good"]["is_good_controlled"]["value"]

        control_list_entries = convert_control_list_entries(good_on_application["good"]["control_list_entries"])
        if good_on_application["is_good_controlled"] is not None:
            is_controlled_application = good_on_application["is_good_controlled"]["value"]
            if is_controlled != is_controlled_application:
                is_controlled = f"<span class='strike'>{is_controlled}</span><br> {is_controlled_application}"
            control_list_application = convert_control_list_entries(good_on_application["control_list_entries"])
            if control_list_entries != control_list_application:
                control_list_entries = f"<span class='strike'>{control_list_entries}</span> {control_list_application}"

        if good_on_application["good"].get("name"):
            name = good_on_application["good"]["name"]
        else:
            name = good_on_application["good"]["description"]

        item = {
            "Name": name,
            "Part number": default_na(good_on_application["good"]["part_number"]),
            "Controlled": mark_safe(is_controlled),  # nosec
            "Control list entries": mark_safe(control_list_entries),  # nosec
        }
        if is_exhibition:
            item["Product type"] = good_on_application["other_item_type"] or good_on_application["item_type"]
        else:
            item["Incorporated"] = friendly_boolean(good_on_application["is_good_incorporated"])
            item["Quantity"] = pluralise_quantity(good_on_application)
            item["Value"] = f"£{good_on_application['value']}"
        if requires_actions(good_on_application):
            update_serial_numbers_url = reverse(
                "applications:update_serial_numbers",
                kwargs={
                    "pk": good_on_application["application"],
                    "good_on_application_pk": good_on_application["id"],
                },
            )
            item[mark_safe('<span class="govuk-visually-hidden">Actions</a>')] = mark_safe(  # nosec
                f'<a class="govuk-link" href="{update_serial_numbers_url}">Add serial numbers</a>'
            )
        elif requires_actions_column:
            item[
                mark_safe('<span class="govuk-visually-hidden">Actions</a>')  # nosec
            ] = " "  # Not just an empty string or it will get converted into N/A
        converted.append(item)

    return converted


def _get_exhibition_details(application):
    data = {
        "Title": application["title"],
        "Exhibition start date": date_display(application["first_exhibition_date"]),
        "Required by": date_display(application["required_by_date"]),
    }
    if application["reason_for_clearance"]:
        data["Reason for clearance"] = application["reason_for_clearance"]
    return data


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
        locations_details[
            "Will the products remain under your direct control while overseas?"
        ] = application.is_temp_direct_control
        locations_details[
            "Who will be in control of the products while overseas, and what is your relationship to them?"
        ] = application.temp_direct_control_details
        locations_details["Proposed date the products will return to the UK"] = str_date_only(
            application.proposed_return_date
        )

    locations_details[
        "Are the products being shipped from the UK on an air waybill or bill of lading?"
    ] = friendly_boolean(application.is_shipped_waybill_or_lading)

    if not application.is_shipped_waybill_or_lading:
        locations_details["Route details"] = application.non_waybill_or_lading_route_details

    locations_details["Who are the products going to?"] = sentence_case(application.goods_recipients)
    return locations_details


def _convert_goods_types(goods_types):
    return [
        {
            "Description": good["description"],
            "Controlled": friendly_boolean(good["is_good_controlled"]),
            "Control list entries": convert_control_list_entries(good["control_list_entries"]),
            "Incorporated": friendly_boolean(good["is_good_incorporated"]),
        }
        for good in goods_types
    ]


def _convert_countries(countries):
    return [
        {"Name": country["country"]["name"], "Contract types": convert_country_contract_types(country)}
        if country["contract_types"]
        else {"Name": country["country"]["name"]}
        for country in countries
    ]


def convert_country_contract_types(country):
    return default_na(
        "\n".join(
            [
                ContractTypes.get_str_representation(ContractTypes(contract_type))
                if contract_type != "other_contract_type"
                else "Other contract type - " + country["other_contract_type_text"]
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


def _get_goods_categories(application):
    return [
        {
            "Description": applications.GoodsCategories.GOODS_CATEGORIES,
            "Answer": friendly_boolean(application.get("contains_firearm_goods")),
        }
    ]


def _get_additional_information(application):
    field_titles = {
        "electronic_warfare_requirement": applications.AdditionalInformation.ELECTRONIC_WARFARE_REQUIREMENT,
        "expedited": applications.AdditionalInformation.EXPEDITED,
        "expedited_date": applications.AdditionalInformation.EXPEDITED_DATE,
        "foreign_technology": applications.AdditionalInformation.FOREIGN_TECHNOLOGY,
        "foreign_technology_type": applications.AdditionalInformation.FOREIGN_TECHNOLOGY_TYPE,
        "locally_manufactured": applications.AdditionalInformation.LOCALLY_MANUFACTURED,
        "mtcr_type": applications.AdditionalInformation.MTCR_TYPE,
        "uk_service_equipment": applications.AdditionalInformation.UK_SERVICE_EQUIPMENT,
        "uk_service_equipment_type": applications.AdditionalInformation.UK_SERVICE_EQUIPMENT_TYPE,
        "value": applications.AdditionalInformation.VALUE,
    }

    values_to_print = []
    for field, title in field_titles.items():
        value = application.get(field)
        if value is not None:
            values_to_print.append(
                {
                    "Description": title,
                    "Answer": (
                        friendly_boolean(value) + "\n" + application.get(f"{field}_description")
                        if isinstance(value, bool) and application.get(f"{field}_description") is not None
                        else friendly_boolean(value)
                        if isinstance(value, bool)
                        else value["value"]
                        if isinstance(value, dict)
                        else value
                    ),
                }
            )

    return values_to_print


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
            document_type = PartyDocumentType.SUPPORTING_DOCUMENT
            if doc["type"] == PartyDocumentType.END_USER_UNDERTAKING_DOCUMENT:
                document_type = "End user document"
            if doc["type"] == PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT:
                document_type = "English translation of the end user document"
            if doc["type"] == PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT:
                document_type = "Document on company letterhead"

            data[document_type] = _convert_end_user_document(application["id"], party["id"], doc, editable)

            if doc["type"] == PartyDocumentType.END_USER_UNDERTAKING_DOCUMENT and party["product_differences_note"]:
                key = "Describe any differences between products listed in the document and products on the application (optional)"
                data[key] = party["product_differences_note"]
    else:
        data[document_availability_key] = "No, I do not have an end-user undertaking or stockist undertaking"
        document_key_heading = "Explain why you do not have an end-user undertaking or stockist undertaking"
        data[document_key_heading] = party["end_user_document_missing_reason"]

    return data


def convert_party(party, application, editable):
    if not party:
        return {}

    has_clearance = application["case_type"]["sub_type"]["key"] == F680

    data = {
        "Name": party["name"],
        "Type": party["sub_type_other"] if party["sub_type_other"] else party["sub_type"]["value"],
        "Clearance level": None,
        "Descriptors": party.get("descriptors"),
        "Address": get_address(party),
        "Website": convert_to_link(party["website"]),
    }

    if party["type"] == "end_user":
        data["Signatory name"] = party.get("signatory_name_euu")

    if party["type"] == "third_party":
        data["Role"] = party.get("role_other") if party.get("role_other") else party.get("role").get("value")

    if application["case_type"]["sub_type"]["key"] != OPEN:
        if party["type"] == "end_user":
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

    if has_clearance:
        data["Clearance level"] = party["clearance_level"].get("value") if party["clearance_level"] else None
    else:
        data.pop("Clearance level")
        # Only display descriptors on third parties for non F680 applications
        if party["type"] != "third_party" and not data.get("Descriptors"):
            data.pop("Descriptors")

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


def _convert_attachable_document(address, attach_address, document, editable):
    if not document and editable:
        return convert_to_link(attach_address, Parties.Documents.ATTACH)

    return convert_to_link(address, "Download")


def get_total_goods_value(goods: list):
    total_value = 0
    for good in goods:
        total_value += Decimal(good["value"])
    return total_value


def _is_application_export_type_temporary(application):
    return application.get("export_type").get("key") == TEMPORARY


def is_application_export_type_permanent(application):
    return False if not application.get("export_type") else (application.get("export_type").get("key") == PERMANENT)


def has_incorporated_goods(application):
    for good in application["goods"]:
        if good["is_good_incorporated"]:
            return True

    return False


def has_incorporated_goods_types(application):
    for goods_type in application["goods_types"]:
        if goods_type["is_good_incorporated"]:
            return True

    return False


def is_application_oiel_of_type(oiel_type, application):
    return (
        False
        if not application.get("goodstype_category")
        else (application.get("goodstype_category").get("key") == oiel_type)
    )


def is_open_application_with_end_user(application):
    if application.end_user:
        if application.type_reference == application.type_reference or application.goodstype_category["key"] in [
            GoodsTypeCategory.MILITARY,
            GoodsTypeCategory.UK_CONTINENTAL_SHELF,
        ]:
            return True
    return False


def _convert_goods_categories(goods_categories):
    return (", ".join([x["value"] for x in goods_categories]),)


def get_application_type_string(application):
    application_type = application.case_type["sub_type"]["key"]
    if application.case_type["reference"]["key"] == CaseTypes.SITL:
        return applications.ApplicationPage.Summary.Licence.TRANSHIPMENT
    elif application.case_type["reference"]["key"] == CaseTypes.SICL:
        return applications.ApplicationPage.Summary.Licence.TRADE_CONTROL
    else:
        return APPLICATION_TYPE_STRINGS[application_type]


def requires_serial_numbers(good_on_application):
    firearm_details = good_on_application.get("firearm_details")
    if not firearm_details:
        return False

    if firearm_details["serial_numbers_available"] == "NOT_AVAILABLE":
        return False

    serial_numbers = firearm_details["serial_numbers"]
    added_serial_numbers = [sn for sn in serial_numbers if sn]
    number_of_items = firearm_details["number_of_items"]

    return number_of_items != len(added_serial_numbers)
