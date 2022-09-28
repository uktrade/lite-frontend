from core import client


def get_mtcr_entries(request):
    response = client.get(request, "/static/regimes/mtcr/entries/")

    return response.json(), response.status_code
