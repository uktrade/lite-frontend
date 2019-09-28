from urllib.parse import urlencode

from conf.client import get, post, put, delete
from conf.constants import GOODSTYPE_URL, GOODSTYPE_COUNTRY_URL


def get_goods_types(request, params=None):
    if params:
        query_params = urlencode(params)
        data = get(request, GOODSTYPE_URL + '?' + query_params)
    else:
        data = get(request, GOODSTYPE_URL)

    return data.json(), data.status_code


def get_goods_type(request, pk):
    data = get(request, GOODSTYPE_URL + pk)
    return data.json(), data.status_code


def post_goods_type(request, json):
    data = post(request, GOODSTYPE_URL, json)
    return data.json(), data.status_code


def update_goods_type(request, pk, json):
    data = put(request, GOODSTYPE_URL + pk + "/", json)
    return data.json(), data.status_code


def delete_goods_type(request, pk):
    data = delete(request, GOODSTYPE_URL + pk)
    return data.json(), data.status_code


def post_goods_type_countries(request, json):
    data = put(request, GOODSTYPE_COUNTRY_URL, json)
    return data.json(), data.status_code
