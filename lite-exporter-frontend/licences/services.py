from conf.client import get
from conf.constants import LICENCES_URL, NLR_URL
from core.helpers import convert_parameters_to_query_params


def get_licences(
    request, page=1, licence_type="licence", reference=None, clc=None, country=None, end_user=None, active_only=None,
):
    response = get(request, LICENCES_URL + convert_parameters_to_query_params(locals()))
    return response.json()


def get_licence(request, pk):
    response = get(request, LICENCES_URL + str(pk) + "/")
    return response.json(), response.status_code


def get_nlr_letters(
    request, page=1, reference=None, clc=None, country=None, end_user=None, active_only=None,
):
    response = get(request, LICENCES_URL + NLR_URL + convert_parameters_to_query_params(locals()))
    return response.json()
