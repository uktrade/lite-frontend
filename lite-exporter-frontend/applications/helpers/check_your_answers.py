from _decimal import Decimal

from django.contrib.humanize.templatetags.humanize import intcomma
from django.urls import reverse_lazy

from conf.constants import (
    NEWLINE,
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
    GoodsTypeCategory,
)
from core.builtins.custom_tags import default_na, friendly_boolean, pluralise_unit, date_display, get_address
from core.helpers import convert_to_link, convert_control_list_entries
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
        applications.ApplicationSummaryPage.GOODS: _convert_goods(application["goods"], True),
        applications.ApplicationSummaryPage.GOODS_LOCATIONS: _convert_goods_locations(application["goods_locations"]),
        applications.ApplicationSummaryPage.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(
            application["additional_documents"], application["id"]
        ),
    }


def _convert_f680_clearance(application, editable=False):
    return {
        applications.ApplicationSummaryPage.GOODS: _convert_goods(application["goods"]),
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
        applications.ApplicationSummaryPage.GOODS: _convert_goods(application["goods"]),
        applications.ApplicationSummaryPage.END_USER: convert_party(application["end_user"], application, editable),
        applications.ApplicationSummaryPage.THIRD_PARTIES: [
            convert_party(party, application, editable) for party in application["third_parties"]
        ],
        applications.ApplicationSummaryPage.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(
            application["additional_documents"], application["id"]
        ),
    }


def _convert_standard_application(application, editable=False, is_summary=False):
    return {
        **(
            {
                applications.ApplicationSummaryPage.GOODS_CATEGORIES: ", ".join(
                    [x["value"] for x in application["goods_categories"]]
                ),
            }
            if is_summary is False
            else {}
        ),
        applications.ApplicationSummaryPage.GOODS: _convert_goods(application["goods"]),
        applications.ApplicationSummaryPage.END_USE_DETAILS: _get_end_use_details(application),
        applications.ApplicationSummaryPage.ROUTE_OF_GOODS: _get_route_of_goods(application),
        **(
            {applications.ApplicationSummaryPage.TEMPORARY_EXPORT_DETAILS: _get_temporary_export_details(application),}
            if _is_application_export_type_temporary(application)
            else {}
        ),
        applications.ApplicationSummaryPage.GOODS_LOCATIONS: _convert_goods_locations(application["goods_locations"]),
        applications.ApplicationSummaryPage.END_USER: convert_party(application["end_user"], application, editable),
        **(
            {
                applications.ApplicationSummaryPage.ULTIMATE_END_USERS: [
                    convert_party(party, application, editable) for party in application["ultimate_end_users"]
                ],
            }
            if has_incorporated_goods(application)
            else {}
        ),
        applications.ApplicationSummaryPage.CONSIGNEE: convert_party(application["consignee"], application, editable),
        applications.ApplicationSummaryPage.THIRD_PARTIES: [
            convert_party(party, application, editable) for party in application["third_parties"]
        ],
        applications.ApplicationSummaryPage.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(
            application["additional_documents"], application["id"]
        ),
    }


def _convert_open_application(application, editable=False):
    return {
        applications.ApplicationSummaryPage.GOODS: _convert_goods_types(application["goods_types"]),
        **(
            {applications.ApplicationSummaryPage.END_USE_DETAILS: _get_end_use_details(application),}
            if not is_application_oiel_cryptographic(application)
            else {}
        ),
        applications.ApplicationSummaryPage.ROUTE_OF_GOODS: _get_route_of_goods(application),
        **(
            {applications.ApplicationSummaryPage.TEMPORARY_EXPORT_DETAILS: _get_temporary_export_details(application),}
            if _is_application_export_type_temporary(application)
            else {}
        ),
        **(
            {
                applications.ApplicationSummaryPage.GOODS_LOCATIONS: _convert_goods_locations(
                    application["goods_locations"]
                ),
            }
            if not is_application_oiel_cryptographic(application)
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
            if is_application_oiel_cryptographic(application)
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


def _convert_goods(goods, is_exhibition=False):
    goods_list = []

    for good in goods:
        goods_dict = {
            "Description": good["good"]["description"],
            "Part number": default_na(good["good"]["part_number"]),
            "Controlled": friendly_boolean(good["good"]["is_good_controlled"]),
            "Control list entries": convert_control_list_entries(good["good"]["control_list_entries"]),
        }
        if is_exhibition:
            goods_dict["Product type"] = good["other_item_type"] if good["other_item_type"] else good["item_type"]
        else:
            goods_dict["Quantity"] = (
                intcomma(good["quantity"]) + " " + pluralise_unit(good["unit"]["value"], good["quantity"])
            )
            goods_dict["Value"] = "£" + good["value"]

        goods_list.append(goods_dict)

    return goods_list


def _get_exhibition_details(application):
    data = {
        "Title": application["title"],
        "Exhibition start date": date_display(application["first_exhibition_date"]),
        "Required by": date_display(application["required_by_date"]),
    }
    if application["reason_for_clearance"]:
        data["Reason for clearance"] = application["reason_for_clearance"]
    return data


def _convert_goods_types(goods_types):
    return [
        {
            "Description": good["description"],
            "Controlled": friendly_boolean(good["is_good_controlled"]),
            "Control list entries": convert_control_list_entries(good["control_list_entries"]),
        }
        for good in goods_types
    ]


def _convert_countries(countries):
    return [{"Name": country["name"]} for country in countries]


def _get_route_of_goods(application):
    return [
        {
            "Description": "Shipped air waybill or lading",
            "Answer": friendly_boolean(application.get("is_shipped_waybill_or_lading"))
            + NEWLINE
            + (application.get("non_waybill_or_lading_route_details") or ""),
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
                        friendly_boolean(value) + NEWLINE + application.get(f"{field}_description")
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
                ds["Answer"] = (
                    friendly_boolean(application.get(main_field)) + NEWLINE + (application.get(ref_field) or "")
                )
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
                    + NEWLINE
                    + (application.get("temp_direct_control_details") or "")
                    if field == "is_temp_direct_control"
                    else application.get(field)
                )
            if display_entry:
                values_to_print.append(display_entry)

        return values_to_print


def convert_party(party, application, editable):
    if not party:
        return {}

    has_clearance = application["case_type"]["sub_type"]["key"] == F680

    document_type = party["type"] if party["type"] != "end_user" else "end-user"

    if party.get("document"):
        document = _convert_document(party, document_type, application["id"], editable)
    else:
        document = convert_to_link(
            reverse_lazy(
                f"applications:{party['type']}_attach_document", kwargs={"pk": application["id"], "obj_pk": party["id"]}
            ),
            "Attach document",
        )

    data = {
        "Name": party["name"],
        "Type": party["sub_type"]["value"],
        "Clearance level": None,
        "Descriptors": party.get("descriptors"),
        "Address": get_address(party),
        "Website": convert_to_link(party["website"]),
        "Document": document,
    }

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
            {"Name": external_location["name"], "Address": get_address(external_location),}
            for external_location in goods_locations["data"]
        ]


def _get_supporting_documentation(supporting_documentation, application_id):
    return [
        {
            "File name": convert_to_link(
                reverse_lazy(
                    "applications:download_additional_document", kwargs={"pk": application_id, "obj_pk": document["id"]}
                ),
                document["name"],
            ),
            "Description": default_na(document["description"]),
        }
        for document in supporting_documentation
    ]


def _convert_document(party, document_type, application_id, editable):
    document = party.get("document")

    if not document:
        return default_na(None)

    if document["safe"] is None:
        return "Processing"

    if not document["safe"]:
        return convert_to_link(f"/applications/{application_id}/{document_type}/document/attach", "Attach another")

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
        total_value += Decimal(good["value"]).quantize(Decimal(".01"))
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


def is_application_oiel_cryptographic(application):
    return (
        False
        if not application.get("goodstype_category")
        else (application.get("goodstype_category").get("key") == "cryptographic")
    )


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
