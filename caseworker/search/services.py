from urllib import parse

from django.conf import settings

from core import client


def get_application_search_results(request, query_params):
    if not settings.LITE_API_SEARCH_ENABLED:
        return []

    querystring = parse.urlencode(query_params, doseq=True)
    response = client.get(request, f"/search/application/search/?{querystring}")
    response.raise_for_status()
    return response.json()


def get_application_autocomplete(request, q):
    if not settings.LITE_API_SEARCH_ENABLED:
        return []

    url = f"/search/application/suggest/?q={q}"
    response = client.get(request, url)
    response.raise_for_status()
    return response.json()


def get_product_search_results(request, query_params):
    if not settings.LITE_API_SEARCH_ENABLED:
        return []

    if query_params:
        query_params["ordering"] = "canonical_name"
    querystring = parse.urlencode(query_params, doseq=True)
    response = client.get(request, f"/search/product/search/?{querystring}")
    response.raise_for_status()
    return response.json()


def get_product_autocomplete(request, q):
    if not settings.LITE_API_SEARCH_ENABLED:
        return []

    url = f"/search/product/suggest/?q={q}"
    response = client.get(request, url)
    response.raise_for_status()
    return response.json()


def get_spire_product(request, pk):
    response = client.get(request, f"/search/product/spire/{pk}/")
    response.raise_for_status()
    return response.json()


def get_lite_product(request, pk):
    response = client.get(request, f"/search/product/lite/{pk}/")
    response.raise_for_status()
    return response.json()
