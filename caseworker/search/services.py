from core import client
from urllib import parse

from caseworker.conf.constants import SEARCH_URL


def get_search_results(request, query_params):
    response = client.get(request, SEARCH_URL + f"?{parse.urlencode(query_params)}")
    response.raise_for_status()
    return response.json()
