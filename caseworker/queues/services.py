from http import HTTPStatus
from urllib import parse

from django.http import HttpResponse

from core import client
from core.helpers import convert_parameters_to_query_params
from lite_content.lite_internal_frontend.users import AssignUserPage
from lite_forms.components import Option


def get_queues(
    request,
    disable_pagination=True,
    page=1,
    convert_to_options=False,
    users_team_first=False,
    include_system=False,
    name=None,
):
    querystring = convert_parameters_to_query_params(
        {
            "disable_pagination": disable_pagination,
            "page": page,
            "convert_to_options": convert_to_options,
            "users_team_first": users_team_first,
            "include_system": include_system,
            "name": name,
        }
    )
    data = client.get(request, f"/queues/{querystring}").json()

    if convert_to_options:
        options = []

        for queue in data:
            option = Option(queue.get("id"), queue.get("name"), id=queue.get("id"))

            queue_team = queue.get("team")
            if queue_team:
                option.description = queue_team.get("name")
                option.data_attribute = queue_team.get("id")

            options.append(option)
        return options
    else:
        return data


def post_queues(request, json):
    data = client.post(request, "/queues/", json)
    return data.json(), data.status_code


def get_queue(request, pk):
    if hasattr(request, "queue") and request.queue.get("id") == pk:
        return request.queue

    response = client.get(request, "/queues/" + str(pk))
    response.raise_for_status()
    return response.json()


def get_cases_search_data(request, queue_pk, params):
    response = client.get(request, "/cases/" + f"?queue_id={queue_pk}&" + parse.urlencode(params, doseq=True))
    return response


def head_cases_search_count(request, queue_pk, params):
    querystring = convert_parameters_to_query_params({"queue_id": queue_pk, **params})
    response = client.head(request, f"/cases/{querystring}")
    return response.headers["Resource-Count"]


def put_queue(request, pk, json):
    data = client.put(request, f"/queues/{pk}/", json)
    return data.json(), data.status_code


def get_queue_case_assignments(request, pk):
    data = client.get(request, f"/queues/{pk}/case-assignments/")
    return data.json(), data.status_code


def put_queue_case_assignments(request, queue_id, case_ids, user_ids, note):
    data = {"case_assignments": [], "remove_existing_assignments": False, "note": note}
    for case_id in case_ids:
        data["case_assignments"].append({"case_id": case_id, "users": user_ids})
    response = client.put(request, f"/queues/{queue_id}/case-assignments/", data)
    return response.json(), response.status_code


def put_queue_single_case_assignment(request, pk, json):
    queue = json.get("queue")
    if queue:
        json = {
            "case_assignments": [{"case_id": json.get("case_pk"), "users": [json.get("user_pk")]}],
            "note": json.get("note"),
        }
        data = client.put(request, f"/queues/{queue}/case-assignments/", json)
        return data.json(), data.status_code
    else:
        return {"errors": {"queue": [AssignUserPage.QUEUE_ERROR_MESSAGE]}}, HTTPStatus.BAD_REQUEST


def get_enforcement_xml(request, queue_pk):
    data = client.get(request, "/cases/enforcement-check/" + str(queue_pk))

    # Check if XML
    if data.headers._store["content-type"][1] == "text/xml":
        response = HttpResponse(data.content, content_type="text/xml")
        response["Content-Disposition"] = 'attachment; filename="enforcement_check.xml"'
        return response, data.status_code
    else:
        return None, data.status_code


def post_enforcement_xml(request, queue_pk, json):
    response = client.post(request, f"/cases/enforcement-check/{queue_pk}", json)
    return response
