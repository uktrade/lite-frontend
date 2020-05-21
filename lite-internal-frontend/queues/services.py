from http import HTTPStatus
from urllib import parse

from django.http import HttpResponse

from conf.client import get, post, put
from conf.constants import QUEUES_URL, CASE_URL
from core.helpers import convert_parameters_to_query_params
from lite_content.lite_internal_frontend.users import AssignUserPage
from lite_forms.components import Option


def get_queues(
    request, disable_pagination=True, page=1, convert_to_options=False, users_team_first=False, include_system=False
):
    data = get(request, QUEUES_URL + convert_parameters_to_query_params(locals())).json()

    if convert_to_options:
        options = []

        for queue in data:
            option = Option(queue.get("id"), queue.get("name"))

            queue_team = queue.get("team")
            if queue_team:
                option.description = queue_team.get("name")
                option.data_attribute = queue_team.get("id")

            options.append(option)

        return options
    else:
        return data


def post_queues(request, json):
    data = post(request, QUEUES_URL, json)
    return data.json(), data.status_code


def get_queue(request, pk):
    data = get(request, QUEUES_URL + str(pk))
    return data.json()


def get_cases_search_data(request, queue_pk, params):
    data = get(request, CASE_URL + "?queue_id=" + str(queue_pk) + "&" + parse.urlencode(params, doseq=True))
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


def get_enforcement_xml(request, queue_pk):
    data = get(request, CASE_URL + "enforcement-check/" + str(queue_pk))

    # Check if XML
    if data.headers._store["content-type"][1] == "text/xml":
        response = HttpResponse(data.content, content_type="text/xml")
        response["Content-Disposition"] = 'attachment; filename="enforcement_check.xml"'
        return response, data.status_code
    else:
        return None, data.status_code
