from http import HTTPStatus

from conf.client import get, post, put, delete
from core.helpers import convert_parameters_to_query_params
from conf.constants import (
    GOODS_URL,
    DOCUMENTS_URL,
    CONTROL_LIST_CLASSIFICATIONS_URL,
    DOCUMENT_SENSITIVITY_URL,
    MISSING_DOCUMENT_REASONS_URL,
)
from core.helpers import remove_prefix


def get_goods(request, page: int = 1, description=None, part_number=None, control_rating=None, for_application=None):
    data = get(request, GOODS_URL + convert_parameters_to_query_params(locals()))

    return data.json()


def get_good(request, pk):
    data = get(request, GOODS_URL + str(pk))
    return data.json().get("good"), data.status_code


def post_goods(request, json):
    if json.get("good_description", False) or json.get("good_description") == "":
        post_data = remove_prefix(json, "good_")
    else:
        post_data = json
    data = post(request, GOODS_URL, post_data)
    return data.json(), data.status_code


def validate_good(request, json):
    if json.get("good_description", False) or json.get("good_description") == "":
        post_data = remove_prefix(json, "good_")
    else:
        post_data = json
    post_data["validate_only"] = True
    data = post(request, GOODS_URL, post_data)
    return data


def update_good(request, pk, json):
    data = put(request, GOODS_URL + pk + "/", json)
    return data.json(), data.status_code


def delete_good(request, pk):
    data = delete(request, GOODS_URL + pk)
    return data.json(), data.status_code


def raise_clc_query(request, json):
    data = post(request, CONTROL_LIST_CLASSIFICATIONS_URL, json)
    return data.json(), data.status_code


# Documents
def get_good_document(request, pk, doc_pk):
    data = get(request, GOODS_URL + pk + DOCUMENTS_URL + doc_pk)
    return data.json().get("document") if data.status_code == HTTPStatus.OK else None


def get_good_documents(request, pk):
    data = get(request, GOODS_URL + pk + DOCUMENTS_URL)
    return data.json().get("documents") if data.status_code == HTTPStatus.OK else None


def post_good_documents(request, pk, json):
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
