from conf.client import get, post, put
from conf.constants import FLAGS_URL


def get_flags(request):
    data = get(request, FLAGS_URL)
    return data.json(), data.status_code


def post_flags(request, json):
    data = post(request, FLAGS_URL, json)
    return data.json(), data.status_code


def get_flag(request, pk):
    data = get(request, FLAGS_URL + pk)
    return data.json(), data.status_code


def put_flag(request, pk, json):
    data = put(request, FLAGS_URL + pk + "/", json)
    return data.json(), data.status_code
