from django.urls import reverse_lazy

from conf.constants import NEWLINE, STANDARD_LICENCE, OPEN_LICENCE, HMRC_QUERY
from core.builtins.custom_tags import default_na, friendly_boolean
from core.helpers import convert_to_link


def convert_application_to_check_your_answers(application):
    """
    Returns a correctly formatted check your answers page for the supplied application
    """
    if application["application_type"]["key"] == STANDARD_LICENCE:
        return _convert_standard_application(application)
    elif application["application_type"]["key"] == OPEN_LICENCE:
        return _convert_open_application(application)
    elif application["application_type"]["key"] == HMRC_QUERY:
        return _convert_hmrc_query(application)
    else:
        raise NotImplementedError()


def _convert_standard_application(application):
    raise NotImplementedError()


def _convert_open_application(application):
    raise NotImplementedError()


def _convert_hmrc_query(application):
    return {
        "On behalf of": application["organisation"]["name"],
        "Goods": _convert_goods_types(application["goods_types"]),
        "Goods locations": _convert_goods_locations(application["goods_locations"]),
        "End user": convert_end_user(application["end_user"], application["id"]),
        "Ultimate end users": _convert_ultimate_end_users(application["ultimate_end_users"], application["id"]),
        "Third parties": _convert_third_parties(application["third_parties"], application["id"]),
        "Consignee": convert_consignee(application["consignee"], application["id"]),
        "Supporting documentation": _get_supporting_documentation(
            application["supporting_documentation"], application["id"]
        ),
        "Optional note": application["reasoning"],
    }


def _convert_goods(goods):
    return [
        {
            "Description": good["description"],
            "Part number": good["part_number"],
            "Controlled": friendly_boolean(good["is_good_controlled"]),
            "Control list entry": default_na(good["control_code"]),
            "Quantity": "?",  # TODO for when we bring this feature to standard/open apps
            "Monetary value": "£",  # TODO for when we bring this feature to standard/open apps
        }
        for good in goods
    ]


def _convert_goods_types(goods_types):
    return [
        {
            "Description": good["description"],
            "Controlled": friendly_boolean(good["is_good_controlled"]),
            "Control list entry": default_na(good["control_code"]),
        }
        for good in goods_types
    ]


def convert_end_user(end_user, application_id):
    if not end_user:
        return {}

    if end_user.get("document"):
        document = _convert_document(end_user["document"], "end-user", application_id)
    else:
        document = convert_to_link(
            reverse_lazy("applications:end_user_attach_document", kwargs={"pk": application_id}), "Attach document"
        )
    return {
        "Name": end_user["name"],
        "Type": end_user["sub_type"]["value"],
        "Address": end_user["address"] + NEWLINE + end_user["country"]["name"],
        "Website": convert_to_link(end_user["website"]),
        "Document": document,
    }


def _convert_ultimate_end_users(ultimate_end_users, application_id):
    return [
        {
            **convert_end_user(ultimate_end_user, application_id),
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
            ),
        }
        for ultimate_end_user in ultimate_end_users
    ]


def convert_consignee(consignee, application_id):
    if not consignee:
        return {}

    if consignee["document"]:
        document = _convert_document(consignee["document"], "consignee", application_id)
    else:
        document = convert_to_link(
            reverse_lazy("applications:consignee_attach_document", kwargs={"pk": application_id}), "Attach document"
        )

    return {
        "Name": consignee["name"],
        "Type": consignee["sub_type"]["value"],
        "Address": consignee["address"] + NEWLINE + consignee["country"]["name"],
        "Website": convert_to_link(consignee["website"]),
        "Document": document,
    }


def _convert_third_parties(third_parties, application_id):
    return [
        {
            "Name": third_party["name"],
            "Type": third_party["sub_type"]["value"],
            "Address": third_party["address"] + NEWLINE + third_party["country"]["name"],
            "Website": convert_to_link(third_party["website"]),
            "Document": _convert_attachable_document(
                reverse_lazy(
                    "applications:third_party_download_document",
                    kwargs={"pk": application_id, "obj_pk": third_party["id"]},
                ),
                reverse_lazy("applications:third_party_attach_document", kwargs={"pk": application_id}),
                third_party["document"],
            ),
        }
        for third_party in third_parties
    ]


def _convert_goods_locations(goods_locations):
    if goods_locations["type"] == "sites":
        return [
            {
                "Site": site["name"],
                "Address": site["address"]["address_line_1"]
                + NEWLINE
                + site["address"]["address_line_2"]
                + NEWLINE
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
                "Site": external_location["name"],
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


def _convert_document(document, document_type, application_id):
    if not document:
        return default_na(None)

    if document["safe"] is None:
        return "Processing"

    if not document["safe"]:
        return convert_to_link(f"/applications/{application_id}/{document_type}/document/attach", "Attach another")

    return convert_to_link(
        f"/applications/{application_id}/{document_type}/document/download", "Download", include_br=True
    ) + convert_to_link(f"/applications/{application_id}/{document_type}/document/delete", "Delete")


def _convert_attachable_document(address, attach_address, document):
    if not document:
        return convert_to_link(attach_address, "Attach document")

    return convert_to_link(address, document["name"])
