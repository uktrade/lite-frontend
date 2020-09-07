from core import client
from urllib import parse


def get_search_results(request, query_params):
    response = client.get(request, f"/search/application/application_search/?{parse.urlencode(query_params)}")
    response.raise_for_status()
    return response.json()


def get_autocomplete(request, q):
    url = f"/search/application/suggest/?q={q}"
    response = client.get(request, url)
    response.raise_for_status()
    return response.json()
