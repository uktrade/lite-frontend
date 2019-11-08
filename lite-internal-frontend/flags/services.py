import functools

from lite_forms.components import Option

from conf.client import get, post, put
from conf.constants import FLAGS_URL


def get_flags(request):
    data = get(request, FLAGS_URL)
    return data.json(), data.status_code


def _get_team_flags(level, request, convert_to_options=False):
    data = get(request, f'{FLAGS_URL}?level={level}&team=True').json()['flags']
    if convert_to_options:
        return [Option(key=flag['id'], value=flag['name']) for flag in data]

    return data


get_cases_flags = functools.partial(_get_team_flags, 'Case')
get_goods_flags = functools.partial(_get_team_flags, 'Good')
get_organisation_flags = functools.partial(_get_team_flags, 'Organisation')


def post_flags(request, json):
    data = post(request, FLAGS_URL, json)
    return data.json(), data.status_code


def get_flag(request, pk):
    data = get(request, FLAGS_URL + pk)
    return data.json(), data.status_code


def put_flag(request, pk, json):
    data = put(request, FLAGS_URL + pk + "/", json)
    return data.json(), data.status_code
