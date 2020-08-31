from urllib import parse

from caseworker.conf.client import get
from caseworker.conf.constants import SEARCH_URL


def get_search_results(request, query_params):
    response = get(request, SEARCH_URL + f"?{parse.urlencode(query_params)}")
    response.raise_for_status()
    return response.json()
