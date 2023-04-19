from core import client
from core.helpers import convert_parameters_to_query_params


def get_licences(
    request,
    licence_type="licence",
    page=None,
    reference=None,
    clc=None,
    country=None,
    end_user=None,
    active_only=None,
):
    url = "/licences/" + convert_parameters_to_query_params(locals())
    response = client.get(request, url)
    return response.json()


def get_licence(request, pk):
    response = client.get(request, f"/licences/{pk}/")
    return response.json(), response.status_code


def get_nlr_letters(
    request,
    page=None,
    reference=None,
    clc=None,
    country=None,
    end_user=None,
    active_only=None,
):
    response = client.get(request, "/licences/nlrs/" + convert_parameters_to_query_params(locals()))
    return response.json()
