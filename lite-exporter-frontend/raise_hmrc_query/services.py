from conf.client import get
from conf.constants import ORGANISATIONS_URL


def get_organisations(request, params):
    data = get(request, ORGANISATIONS_URL + '?' + params)
    return data.json(), data.status_code
