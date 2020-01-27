from http import HTTPStatus

from conf.client import get, post, put, delete
from conf.constants import (
    GOODS_URL,
    DOCUMENTS_URL,
    GOODS_QUERY_URL,
    DOCUMENT_SENSITIVITY_URL,
    MISSING_DOCUMENT_REASONS_URL,
    GENERATED_DOCUMENTS_URL,
    CASES_URL,
    ADDITIONAL_DOCUMENT_URL,
    DOWNLOAD_URL,
)
from goods.helpers import process_pv_grading_for_post
from core.helpers import convert_parameters_to_query_params
from core.services import get_document_download_stream


def get_goods(request, page: int = 1, description=None, part_number=None, control_rating=None, for_application=None):
    data = get(request, GOODS_URL + convert_parameters_to_query_params(locals()))
    return data.json()


def get_good(request, pk):
    data = get(request, GOODS_URL + str(pk))
    return data.json().get("good"), data.status_code


def post_goods(request, json):
    data = post(request, GOODS_URL, json)
    if data.status_code == HTTPStatus.OK:
        data.json().get("good"), data.status_code
    return data.json(), data.status_code


def validate_good(request, json):
    post_data = json
    post_data["validate_only"] = True

    data = post_goods(request, post_data)
    return data


def post_good_with_pv_grading(request, json):
    post_data = process_pv_grading_for_post(json)

    data = post_goods(request, post_data)
    return data


def edit_good(request, pk, json):
    data = put(request, GOODS_URL + pk + "/", json)
    return data.json(), data.status_code


def validate_edit_good(request, pk, json):
    post_data = json

    post_data["validate_only"] = True
    return edit_good(request, pk, post_data)


def edit_good_with_pv_grading(request, pk, json):
    post_data = process_pv_grading_for_post(json)

    data = edit_good(request, pk, post_data)
    return data


def delete_good(request, pk):
    data = delete(request, GOODS_URL + pk)
    return data.json(), data.status_code


def raise_goods_query(request, pk, json):
    post_data = json
    post_data["good_id"] = pk

    data = post(request, GOODS_QUERY_URL, post_data)
    return data.json(), data.status_code


def get_goods_query_generated_documents(request, pk):
    data = get(request, GOODS_QUERY_URL + pk + GENERATED_DOCUMENTS_URL)
    return data.json(), data.status_code


# Documents
def get_good_document(request, pk, doc_pk):
    data = get(request, GOODS_URL + pk + DOCUMENTS_URL + doc_pk)
    return data.json().get("document") if data.status_code == HTTPStatus.OK else None


def get_good_documents(request, pk):
    data = get(request, GOODS_URL + pk + DOCUMENTS_URL)
    return data.json().get("documents") if data.status_code == HTTPStatus.OK else None


def post_good_documents(request, pk, json):
    if "description" not in json:
        json["description"] = ""
    json = [json]

    data = post(request, GOODS_URL + pk + DOCUMENTS_URL, json)
    return data.json(), data.status_code


def delete_good_document(request, pk, doc_pk):
    data = delete(request, GOODS_URL + pk + DOCUMENTS_URL + doc_pk)
    return data.json(), data.status_code


# Document Sensitivity
def get_document_missing_reasons(request):
    data = get(request, MISSING_DOCUMENT_REASONS_URL)
    return data.json(), data.status_code


def post_good_document_sensitivity(request, pk, json):
    data = post(request, GOODS_URL + str(pk) + DOCUMENT_SENSITIVITY_URL, json)
    return data.json(), data.status_code


def get_case_document_download(request, document_pk, case_pk):
    return get_document_download_stream(
        request, CASES_URL + str(document_pk) + ADDITIONAL_DOCUMENT_URL + str(case_pk) + DOWNLOAD_URL
    )
