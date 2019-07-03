from conf.client import get, post, put
from conf.constants import QUEUES_URL


def get_queues(request):
    data = get(request, QUEUES_URL)
    return data.json(), data.status_code


def post_queues(request, json):
    data = post(request, QUEUES_URL, json)
    return data.json(), data.status_code


def get_queue(request, pk):
    data = get(request, QUEUES_URL + pk)
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

