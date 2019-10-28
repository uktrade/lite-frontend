from conf.client import get, post, put, delete
from conf.constants import APPLICATIONS_URL, GOODSTYPES_URL, GOODSTYPE_URL, GOODSTYPE_COUNTRY_URL


def get_goods_type(request, app_pk, good_pk):
    data = get(request, APPLICATIONS_URL + app_pk + GOODSTYPE_URL + good_pk + '/')
    return data.json(), data.status_code


def post_goods_type(request, app_pk, json):
    data = post(request, APPLICATIONS_URL + app_pk + GOODSTYPES_URL, json)
    return data.json(), data.status_code


def delete_goods_type(request, app_pk, good_pk):
    data = delete(request, APPLICATIONS_URL + app_pk + GOODSTYPE_URL + good_pk + "/")
    return data.status_code


def post_goods_type_countries(request, app_pk, good_pk, json):
    data = put(request, APPLICATIONS_URL + app_pk + GOODSTYPE_URL + good_pk + GOODSTYPE_COUNTRY_URL, json)
    return data.json(), data.status_code
