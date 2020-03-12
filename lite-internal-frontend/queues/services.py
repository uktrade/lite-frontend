from lite_content.lite_internal_frontend.users import AssignUserPage
from lite_forms.components import Option

from conf.client import get, post, put
from conf.constants import QUEUES_URL, CASE_URL
from http import HTTPStatus


def get_queues(request, convert_to_options=False):
    data = get(request, QUEUES_URL)
    if convert_to_options:
        converted = []

        for queue in data.json().get("queues"):
            converted.append(Option(queue.get("id"), queue.get("name"), description=queue.get("team").get("name")))

        return converted

    return data.json()["queues"]


def post_queues(request, json):
    data = post(request, QUEUES_URL, json)
    return data.json(), data.status_code


def get_queue(request, pk, case_type=None, status=None, sort=None):
    filter_and_sort = []

    if case_type:
        filter_and_sort.append("case_type=" + case_type)

    if status:
        filter_and_sort.append("status=" + status)

    if sort:
        sort_json = sort.split("-")
        import json

        if len(sort_json) == 2:
            sort = json.dumps({sort_json[0]: sort_json[1]})
            filter_and_sort.append("sort=" + sort)

    filter_and_sort = "?" + "&".join(filter_and_sort) if len(filter_and_sort) > 0 else ""

    data = get(request, QUEUES_URL + str(pk) + filter_and_sort)

    return data.json()


def get_cases_search_data(request, params):
    data = get(request, CASE_URL + "?" + params)
    return data.json()


def put_queue(request, pk, json):
    data = put(request, QUEUES_URL + str(pk) + "/", json)
    return data.json(), data.status_code


def get_queue_case_assignments(request, pk):
    data = get(request, QUEUES_URL + pk + "/case-assignments/")
    return data.json(), data.status_code


def put_queue_case_assignments(request, pk, json):
    data = put(request, QUEUES_URL + str(pk) + "/case-assignments/", json)
    return data.json(), data.status_code


def put_queue_single_case_assignment(request, pk, json):
    queue = json.get("queue")
    if queue:
        json = {"case_assignments": [{"case_id": json.get("case_pk"), "users": [json.get("user_pk")]}]}
        data = put(request, QUEUES_URL + queue + "/case-assignments/", json)
        return data.json(), data.status_code
    else:
        return {"errors": {"queue": [AssignUserPage.QUEUE_ERROR_MESSAGE]}}, HTTPStatus.BAD_REQUEST
