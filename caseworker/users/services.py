from http import HTTPStatus
from urllib.parse import urlencode

from core import client
from lite_content.lite_internal_frontend.users import AssignUserPage
from lite_forms.components import Option

from caseworker.core.constants import SUPER_USER_ROLE_ID


def get_gov_users(request, params=None):
    if params:
        query_params = urlencode(params)
        data = client.get(request, f"/gov-users/?{query_params}")
    else:
        data = client.get(request, "/gov-users/")
    return data.json(), data.status_code


def convert_users_to_choices(data):
    choices = []
    for user in data:
        # Hide users without emails (eg system users)
        email = user["email"]
        if email:
            display = email
            if user.get("first_name"):
                display = f'{user["first_name"]} {user["last_name"]} ({user["team"]["name"]})'

            choices.append((user["id"], display))
    return choices


def convert_users_to_options(data):
    converted = []
    for user in data:
        # Hide users without emails (eg system users)
        email = user["email"]
        if email:
            value = email
            description = None

            if user.get("first_name"):
                value = f'{user["first_name"]} {user["last_name"]}'
                description = email

            converted.append(Option(key=user.get("id"), value=value, description=description))
    return converted


def get_gov_user(request, pk=None):
    if pk:
        if not hasattr(request, "cached_get_gov_user_response_by_pk"):
            request.cached_get_gov_user_response_by_pk = {}
        if not request.cached_get_gov_user_response_by_pk.get(pk):
            request.cached_get_gov_user_response_by_pk[pk] = client.get(request, f"/gov-users/{pk}")
        response = request.cached_get_gov_user_response_by_pk[pk]
    else:
        if not hasattr(request, "cached_get_gov_user_response"):
            request.cached_get_gov_user_response = client.get(request, "/gov-users/" + "me/")
        response = request.cached_get_gov_user_response

    return response.json(), response.status_code


def get_gov_user_from_form_selection(request, pk, json):
    user = json.get("user")
    if user:
        data = client.get(request, f"/gov-users/{user}")
        return data.json(), data.status_code
    return {"errors": {"user": [AssignUserPage.USER_ERROR_MESSAGE]}}, HTTPStatus.BAD_REQUEST


def post_gov_users(request, json):
    json.setdefault("first_name", "")
    json.setdefault("last_name", "")
    data = client.post(request, "/gov-users/", json)
    return data.json(), data.status_code


def put_gov_user(request, pk, json):
    data = client.put(request, f"/gov-users/{pk}/", json)
    return data.json(), data.status_code


# Roles and Permissions
def get_roles(request, convert_to_options=False):
    data = client.get(request, "/gov-users/roles/")

    if convert_to_options:
        converted = []

        for item in data.json().get("roles"):
            converted.append(Option(key=item["id"], value=item["name"]))

        return converted

    return data.json(), data.status_code


def get_role(request, pk):
    data = client.get(request, f"/gov-users/roles/{pk}")
    return data.json(), data.status_code


def post_role(request, json):
    data = client.post(request, "/gov-users/roles/", json)
    return data.json(), data.status_code


def put_role(request, pk, json):
    data = client.put(request, f"/gov-users/roles/{pk}/", json)
    return data.json(), data.status_code


def get_permissions(request, convert_to_options=False):
    data = client.get(request, "/gov-users/permissions/")

    if convert_to_options:
        converted = []

        for item in data.json().get("permissions"):
            converted.append(Option(key=item["id"], value=item["name"]))

        return converted

    return data.json()["permissions"]


def is_super_user(user):
    return user["user"]["role"]["id"] == SUPER_USER_ROLE_ID


def is_user_in_team(user, team_id):
    return user["user"]["team"]["id"] == team_id


def get_user_case_note_mentions(request, params):

    query_params = urlencode(params)
    url = f"/cases/user-case-note-mentions/?{query_params}"
    response = client.get(request, url)
    response.raise_for_status()
    return response.json(), response.status_code
