from conf.client import get, put
from conf.constants import ECJU_QUERIES_URL, CASES_URL


def get_ecju_query(request, pk, query_pk):
    data = get(request, CASES_URL + pk + ECJU_QUERIES_URL + query_pk).json()["ecju_query"]
    return data


def put_ecju_query(request, pk, query_pk, json):
    data = put(request, CASES_URL + pk + ECJU_QUERIES_URL + query_pk + "/", json)
    return data.json(), data.status_code
