from core.helpers import convert_dict_to_query_params
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


def get_queue(request, pk):
    data = get(request, QUEUES_URL + str(pk))
    return data.json()


def get_cases_search_data(request, queue_pk, params):
    data = get(request, CASE_URL + "?queue_id=" + str(queue_pk) + "&" + convert_dict_to_query_params(params))
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
