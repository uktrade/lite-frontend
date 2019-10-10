from lite_forms.components import Option

from conf.client import get, post, put
from conf.constants import FLAGS_URL, FLAGS_CASE_LEVEL_FOR_TEAM, FLAGS_GOOD_LEVEL_FOR_TEAM, FLAGS_ORGANISATION_LEVEL_FOR_TEAM


def get_flags(request):
    data = get(request, FLAGS_URL)
    return data.json(), data.status_code


def get_cases_flags(request, convert_to_options=False):
    data = get(request, FLAGS_CASE_LEVEL_FOR_TEAM).json()['flags']

    if convert_to_options:
        converted = []

        for flag in data:
            converted.append(
                Option(key=flag['id'],
                       value=flag['name'])
            )

        return converted

    return data


def get_goods_flags(request, convert_to_options=False):
    data = get(request, FLAGS_GOOD_LEVEL_FOR_TEAM).json()['flags']

    if convert_to_options:
        converted = []

        for flag in data:
            converted.append(
                Option(key=flag['id'],
                       value=flag['name'])
            )

        return converted

    return data


def get_organisation_flags(request, convert_to_options=False):
    data = get(request, FLAGS_ORGANISATION_LEVEL_FOR_TEAM).json()['flags']

    if convert_to_options:
        converted = []

        for flag in data:
            converted.append(
                Option(key=flag['id'],
                       value=flag['name'])
            )

        return converted

    return data


def post_flags(request, json):
    data = post(request, FLAGS_URL, json)
    return data.json(), data.status_code


def get_flag(request, pk):
    data = get(request, FLAGS_URL + pk)
    return data.json(), data.status_code


def put_flag(request, pk, json):
    data = put(request, FLAGS_URL + pk + "/", json)
    return data.json(), data.status_code
