import json

from lite_forms.components import Option

from conf.client import get, post, put
from conf.constants import QUEUES_URL


def get_queues(request, convert_to_options=False, include_system_queues=False):
    data = get(request, QUEUES_URL + "?include_system_queues=" + str(include_system_queues))

    if convert_to_options:
        converted = []

        for queue in data.json().get('queues'):
            converted.append(
                Option(queue.get('id'), queue.get('name'), description=queue.get('team').get('name'))
            )

        return converted

    return data.json(), data.status_code


def post_queues(request, json):
    data = post(request, QUEUES_URL, json)
    return data.json(), data.status_code


def get_queue(request, pk, case_type=None, status=None, sort=None):
    filter_and_sort = []

    if case_type:
        filter_and_sort.append('case_type=' + case_type)

    if status:
        filter_and_sort.append('status=' + status)

    if sort:
        sort_json = sort.split('-')
        if len(sort_json) == 2:
            sort = json.dumps({sort_json[0]: sort_json[1]})
            filter_and_sort.append('sort=' + sort)

    filter_and_sort = '?' + '&'.join(filter_and_sort) if len(filter_and_sort) > 0 else ''

    data = get(request, QUEUES_URL + pk + filter_and_sort)

    return data.json(), data.status_code


def put_queue(request, pk, json):
    data = put(request, QUEUES_URL + pk + '/', json)
    return data.json(), data.status_code


# Case Assignments


def get_queue_case_assignments(request, pk):
    data = get(request, QUEUES_URL + pk + '/case-assignments/')
    return data.json(), data.status_code


def put_queue_case_assignments(request, pk, json):
    data = put(request, QUEUES_URL + pk + '/case-assignments/', json)
    return data.json(), data.status_code

