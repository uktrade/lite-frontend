from conf.client import get
from conf.constants import LICENCES_URL, NLR_URL, LicenceType
from core.helpers import convert_parameters_to_query_params


def get_licences(
    request, page=1, licence_type="licence", reference=None, clc=None, country=None, end_user=None, active_only=None,
):
    if request.GET.get("licence_type") == LicenceType.NLR:
        data = get(request, LICENCES_URL + NLR_URL + convert_parameters_to_query_params(locals()))
    else:
        data = get(request, LICENCES_URL + convert_parameters_to_query_params(locals()))
    return data.json()


def get_licence(request, pk):
    data = get(request, LICENCES_URL + str(pk) + "/")
    return data.json(), data.status_code
