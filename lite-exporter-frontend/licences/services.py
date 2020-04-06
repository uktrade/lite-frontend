from conf.client import get
from conf.constants import LICENCES_URL
from core.helpers import convert_parameters_to_query_params


def get_licences(
    request, page=1, licence_type="licence", reference=None, clc=None, country=None, end_user=None, active_only=None
):
    data = get(request, LICENCES_URL + convert_parameters_to_query_params(locals()))
    return data.json()
