from core import client


def get_regime_entries(request, regime_type):
    response = client.get(request, f"/static/regimes/entries/{regime_type.lower()}/")

    return response.json(), response.status_code


def get_regime_entries_all(request):
    response = client.get(request, f"/static/regimes/entries/")

    return response.json(), response.status_code
