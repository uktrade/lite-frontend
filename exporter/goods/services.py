from http import HTTPStatus

from core import client
from core.helpers import convert_parameters_to_query_params, format_date
from exporter.goods.helpers import serialize_goods_data, add_firearm_details_to_data


def get_goods(
    request, page: int = 1, name=None, description=None, part_number=None, control_list_entry=None, for_application=None
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
    serialize_goods_data(request, json)

    data = client.post(request, "/goods/", json)

    return data.json(), data.status_code


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
    add_firearm_details_to_data(request, json)
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


def get_good_document_availability(request, pk):
    data = client.get(request, f"/goods/{pk}/document-availability/")
    return data.json(), data.status_code


def post_good_document_availability(request, pk, json):
    data = client.post(request, f"/goods/{pk}/document-availability/", json)
    return data.json(), data.status_code


def get_good_document_sensitivity(request, pk):
    data = client.get(request, f"/goods/{pk}/document-sensitivity/")
    return data.json(), data.status_code


def post_good_document_sensitivity(request, pk, json):
    data = client.post(request, f"/goods/{pk}/document-sensitivity/", json)
    return data.json(), data.status_code
