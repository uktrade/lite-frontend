from _decimal import Decimal

from django.contrib.humanize.templatetags.humanize import intcomma
from django.urls import reverse_lazy

from conf.constants import NEWLINE, STANDARD_LICENCE, OPEN_LICENCE, HMRC_QUERY, EXHIBITION_CLEARANCE
from core.builtins.custom_tags import default_na, friendly_boolean, pluralise_unit
from core.helpers import convert_to_link
from lite_content.lite_exporter_frontend import applications
from lite_content.lite_exporter_frontend.strings import Parties
from lite_forms.helpers import conditional


def convert_application_to_check_your_answers(application, editable=False):
    """
    Returns a correctly formatted check your answers page for the supplied application
    """
    if application["application_type"]["key"] == STANDARD_LICENCE:
        return _convert_standard_application(application, editable)
    elif application["application_type"]["key"] == OPEN_LICENCE:
        return _convert_open_application(application, editable)
    elif application["application_type"]["key"] == HMRC_QUERY:
        return _convert_hmrc_query(application, editable)
    elif application["application_type"]["key"] == EXHIBITION_CLEARANCE:
        return _convert_exhibition_clearance(application, editable)
    else:
        raise NotImplementedError()


def _convert_exhibition_clearance(application, editable=False):
    # Temp as exhibition clearance is currently the same as standard but will change
    return _convert_standard_application(application, editable)


def _convert_standard_application(application, editable=False):
    return {
        applications.ApplicationSummaryPage.GOODS: _convert_goods(application["goods"]),
        applications.ApplicationSummaryPage.GOODS_LOCATIONS: _convert_goods_locations(application["goods_locations"]),
        applications.ApplicationSummaryPage.END_USER: convert_party(
            application["end_user"], application["id"], editable
        ),
        applications.ApplicationSummaryPage.ULTIMATE_END_USERS: _convert_ultimate_end_users(
            application["ultimate_end_users"], application["id"], editable
        ),
        applications.ApplicationSummaryPage.THIRD_PARTIES: _convert_third_parties(
            application["third_parties"], application["id"], editable
        ),
        applications.ApplicationSummaryPage.CONSIGNEE: convert_party(
            application["consignee"], application["id"], editable
        ),
        applications.ApplicationSummaryPage.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(
            application["additional_documents"], application["id"]
        ),
        applications.ApplicationSummaryPage.GOODS_CATEGORIES: ", ".join(
            [x["value"] for x in application["goods_categories"]]
        ),
    }


def _convert_open_application(application, editable=False):
    return {
        applications.ApplicationSummaryPage.GOODS: _convert_goods_types(application["goods_types"]),
        applications.ApplicationSummaryPage.GOODS_LOCATIONS: _convert_goods_locations(application["goods_locations"]),
        applications.ApplicationSummaryPage.COUNTRIES: _convert_countries(application["destinations"]["data"]),
        applications.ApplicationSummaryPage.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(
            application["additional_documents"], application["id"]
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
        applications.ApplicationSummaryPage.END_USER: convert_party(
            application["end_user"], application["id"], editable
        ),
        applications.ApplicationSummaryPage.ULTIMATE_END_USERS: _convert_ultimate_end_users(
            application["ultimate_end_users"], application["id"], editable
        ),
        applications.ApplicationSummaryPage.THIRD_PARTIES: _convert_third_parties(
            application["third_parties"], application["id"], editable
        ),
        applications.ApplicationSummaryPage.CONSIGNEE: convert_party(
            application["consignee"], application["id"], editable
        ),
        applications.ApplicationSummaryPage.SUPPORTING_DOCUMENTATION: _get_supporting_documentation(
            application["supporting_documentation"], application["id"]
        ),
        applications.ApplicationSummaryPage.OPTIONAL_NOTE: application["reasoning"],
    }


def _convert_goods(goods):
    return [
        {
            "Description": good["good"]["description"],
            "Part number": default_na(good["good"]["part_number"]),
            "Controlled": friendly_boolean(good["good"]["is_good_controlled"]),
            "CLC": default_na(good["good"]["control_code"]),
            "Quantity": intcomma(good["quantity"]) + " " + pluralise_unit(good["unit"]["value"], good["quantity"]),
            "Value": "£" + good["value"],
        }
        for good in goods
    ]


def _convert_goods_types(goods_types):
    return [
        {
            "Description": good["description"],
            "Controlled": friendly_boolean(good["is_good_controlled"]),
            "CLC": default_na(good["control_code"]),
        }
        for good in goods_types
    ]


def _convert_countries(countries):
    return [{"Name": country["name"]} for country in countries]


def convert_party(party, application_id, editable):
    if not party:
        return {}

    document_type = party["type"] if party["type"] != "end_user" else "end-user"

    if party.get("document"):
        document = _convert_document(party, document_type, application_id, editable)
    else:
        document = convert_to_link(
            reverse_lazy(
                f"applications:{party['type']}_attach_document", kwargs={"pk": application_id, "obj_pk": party["id"]}
            ),
            "Attach document",
        )
    return {
        "Name": party["name"],
        "Type": party["sub_type"]["value"],
        "Address": party["address"] + NEWLINE + party["country"]["name"],
        "Website": convert_to_link(party["website"]),
        "Document": document,
    }


def _convert_ultimate_end_users(ultimate_end_users, application_id, editable):
    return [
        {
            **convert_party(ultimate_end_user, application_id, editable),
            "Document": _convert_attachable_document(
                reverse_lazy(
                    "applications:ultimate_end_user_download_document",
                    kwargs={"pk": application_id, "obj_pk": ultimate_end_user["id"]},
                ),
                reverse_lazy(
                    "applications:ultimate_end_user_attach_document",
                    kwargs={"pk": application_id, "obj_pk": ultimate_end_user["id"]},
                ),
                ultimate_end_user["document"],
                editable,
            ),
        }
        for ultimate_end_user in ultimate_end_users
    ]


def _convert_third_parties(third_parties, application_id, editable):
    return [
        {
            "Name": third_party["name"],
            "Type": third_party["sub_type"]["value"],
            "Role": third_party["role"]["value"],
            "Address": third_party["address"] + NEWLINE + third_party["country"]["name"],
            "Website": convert_to_link(third_party["website"]),
            "Document": _convert_attachable_document(
                reverse_lazy(
                    "applications:third_party_download_document",
                    kwargs={"pk": application_id, "obj_pk": third_party["id"]},
                ),
                reverse_lazy("applications:third_party_attach_document", kwargs={"pk": application_id}),
                third_party["document"],
                editable,
            ),
        }
        for third_party in third_parties
    ]


def _convert_goods_locations(goods_locations):
    if "type" not in goods_locations:
        return

    if goods_locations["type"] == "sites":
        return [
            {
                "Site": site["name"],
                "Address": site["address"]["address_line_1"]
                + NEWLINE
                + (site["address"]["address_line_2"] + NEWLINE if site["address"]["address_line_2"] else "")
                + site["address"]["city"]
                + NEWLINE
                + site["address"]["region"]
                + NEWLINE
                + site["address"]["postcode"]
                + NEWLINE
                + site["address"]["country"]["name"],
            }
            for site in goods_locations["data"]
        ]
    else:
        return [
            {
                "Name": external_location["name"],
                "Address": external_location["address"] + NEWLINE + external_location["country"]["name"],
            }
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
