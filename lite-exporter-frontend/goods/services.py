from http import HTTPStatus
from urllib.parse import urlencode

from conf.client import get, post, put, delete
from conf.constants import GOODS_URL, DOCUMENTS_URL, CONTROL_LIST_CLASSIFICATIONS_URL
from core.helpers import remove_prefix


def get_goods(request, params=None):
    if params:
        query_params = urlencode(params)
        data = get(request, GOODS_URL + "?" + query_params)
    else:
        data = get(request, GOODS_URL)

    return data.json().get("goods"), data.status_code


def get_good(request, pk):
    data = get(request, GOODS_URL + pk)
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


def get_clc_query(request, pk):
    data = get(request, CONTROL_LIST_CLASSIFICATIONS_URL + pk)
    return data.json().get("control_list_classification_query") if data.status_code == HTTPStatus.OK else None


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
