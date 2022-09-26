from core import client


def get_wassenaar_entries(request):
    response = client.get(request, "/static/regimes/wassenaar/entries/")

    return response.json(), response.status_code


def get_mtcr_entries(request):
    response = client.get(request, "/static/regimes/mtcr/entries/")

    return response.json(), response.status_code
