from http import HTTPStatus

from exporter.applications.helpers.date_fields import format_date
from core import client
from core.helpers import convert_parameters_to_query_params
from exporter.core.services import get_document_download_stream


def get_goods(
    request, page: int = 1, description=None, part_number=None, control_list_entry=None, for_application=None
):
    data = client.get(request, "/goods/" + convert_parameters_to_query_params(locals()))
    return data.json()


def get_good(request, pk, full_detail=False):
    data = client.get(request, f"/goods/{pk}/" + convert_parameters_to_query_params(locals()))
    return data.json().get("good"), data.status_code


def get_good_details(request, pk):
    data = client.get(request, f"/goods/{pk}/details/" + convert_parameters_to_query_params(locals()))
    return data.json().get("good"), data.status_code


def post_goods(request, json):
    if "is_pv_graded" in json and json["is_pv_graded"] == "yes":
        if "reference" in json:
            json["pv_grading_details"] = {
                "grading": json["grading"],
                "custom_grading": json["custom_grading"],
                "prefix": json["prefix"],
                "suffix": json["suffix"],
                "issuing_authority": json["issuing_authority"],
                "reference": json["reference"],
                "date_of_issue": format_date(json, "date_of_issue"),
            }

    if "item_category" in json and json["item_category"] == "group2_firearms":
        add_firearm_details_to_data(json)

    data = client.post(request, "/goods/", json)

    if data.status_code == HTTPStatus.OK:
        data.json().get("good"), data.status_code

    return data.json(), data.status_code


def add_firearm_details_to_data(json):
    """
    Return a firearm_details dictionary to be used when creating/editing a group 2 firearm good
    Mutable - items in firearm_details are removed from the original json (duplicates)
    """
    firearm_details = {}
    if "product_type_step" in json:
        # parent component doesnt get sent when empty unlike the remaining form fields
        firearm_details["type"] = json.get("type")
    if "firearm_ammunition_step" in json:
        firearm_details["year_of_manufacture"] = json.get("year_of_manufacture")
        firearm_details["calibre"] = json.get("calibre")
        del json["year_of_manufacture"]
        del json["calibre"]
    if "section_certificate_step" in json:
        # parent component doesnt get sent when empty unlike the remaining form fields
        firearm_details["is_covered_by_firearm_act_section_one_two_or_five"] = json.get(
            "is_covered_by_firearm_act_section_one_two_or_five", ""
        )
        firearm_details["section_certificate_number"] = json.get("section_certificate_number")
        formatted_section_certificate_date = format_date(json, "section_certificate_date_of_expiry")
        firearm_details["section_certificate_date_of_expiry"] = (
            formatted_section_certificate_date if formatted_section_certificate_date != "--" else None
        )
        del json["section_certificate_number"]
    if "identification_markings_step" in json:
        # parent component doesnt get sent when empty unlike the remaining form fields
        firearm_details["has_identification_markings"] = json.get("has_identification_markings", "")
        firearm_details["identification_markings_details"] = json.get("identification_markings_details")
        firearm_details["no_identification_markings_details"] = json.get("no_identification_markings_details")
        del json["identification_markings_details"]
        del json["no_identification_markings_details"]

    json["firearm_details"] = firearm_details
    return json


def validate_good(request, json):
    post_data = json
    post_data["validate_only"] = True

    return post_goods(request, post_data)


def edit_good(request, pk, json):
    data = client.put(request, f"/goods/{pk}/", json)
    return data.json(), data.status_code


def edit_good_details(request, pk, json):
    data = client.put(request, f"/goods/{pk}/details/", json)
    return data.json(), data.status_code


def edit_good_firearm_details(request, pk, json):
    add_firearm_details_to_data(json)
    return edit_good_details(request, pk, json)


def edit_good_pv_grading(request, pk, json):
    data = {"is_pv_graded": json["is_pv_graded"]}
    if json["is_pv_graded"] == "yes":
        data["pv_grading_details"] = {
            "grading": json["grading"],
            "custom_grading": json["custom_grading"],
            "prefix": json["prefix"],
            "suffix": json["suffix"],
            "issuing_authority": json["issuing_authority"],
            "reference": json["reference"],
            "date_of_issue": format_date(json, "date_of_issue"),
        }
    return edit_good(request, pk, data)


def delete_good(request, pk):
    data = client.delete(request, "/goods/" + pk)
    return data.json(), data.status_code


def raise_goods_query(request, pk, json):
    post_data = json
    post_data["good_id"] = pk

    data = client.post(request, "/queries/goods-queries/", post_data)
    return data.json(), data.status_code


# Documents
def get_good_document(request, pk, doc_pk):
    data = client.get(request, f"/goods/{pk}/documents/" + doc_pk)
    return data.json().get("document") if data.status_code == HTTPStatus.OK else None


def get_good_documents(request, pk):
    data = client.get(request, f"/goods/{pk}/documents/")
    return data.json().get("documents") if data.status_code == HTTPStatus.OK else None


def post_good_documents(request, pk, json):
    if "description" not in json:
        json["description"] = ""
    json = [json]

    data = client.post(request, f"/goods/{pk}/documents/", json)
    return data.json(), data.status_code


def delete_good_document(request, pk, doc_pk):
    data = client.delete(request, f"/goods/{pk}/documents/" + doc_pk)
    return data.json(), data.status_code


# Document Sensitivity
def get_document_missing_reasons(request):
    data = client.get(request, "/static/missing-document-reasons/")
    return data.json(), data.status_code


def post_good_document_sensitivity(request, pk, json):
    data = client.post(request, f"/goods/{pk}/document-sensitivity/", json)
    return data.json(), data.status_code


def get_case_document_download(request, document_pk, case_pk):
    return get_document_download_stream(request, f"/cases/{document_pk}/document/documents/{case_pk}/download/")
