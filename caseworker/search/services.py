from urllib import parse

from django.conf import settings

from core import client


def get_search_results(request, query_params):
    if not settings.LITE_API_SEARCH_ENABLED:
        return []

    querystring = parse.urlencode(query_params, doseq=True)
    response = client.get(request, f"/search/application/application_search/?{querystring}")
    response.raise_for_status()
    return response.json()


def get_autocomplete(request, q):
    if not settings.LITE_API_SEARCH_ENABLED:
        return []
    url = f"/search/application/suggest/?q={q}"
    response = client.get(request, url)
    response.raise_for_status()
    return response.json()
