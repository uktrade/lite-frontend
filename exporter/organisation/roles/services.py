from lite_forms.components import Option

from core import client
from exporter.organisation.members.services import get_user


def get_roles(request, organisation_id, convert_to_options=False, page=1):
    url = f"/organisations/{organisation_id}/roles/?disable_pagination={convert_to_options}&page={page}"
    data = client.get(request, url).json()

    if convert_to_options:
        converted = []

        for item in data:
            converted.append(Option(key=item["id"], value=item["name"]))
        return converted

    return data


def get_role(request, pk):
    organisation_id = str(request.session["organisation"])
    data = client.get(request, f"/organisations/{organisation_id}/roles/{pk}")
    return data.json()["role"]


def post_role(request, json):
    organisation_id = request.session["organisation"]
    data = client.post(request, f"/organisations/{organisation_id}/roles/", json)
    return data.json(), data.status_code


def put_role(request, pk, json):
    organisation_id = request.session["organisation"]
    data = client.put(request, f"/organisations/{organisation_id}/roles/{pk}/", json)
    return data.json(), data.status_code


def get_permissions(request, convert_to_options=False):
    data = client.get(request, f"/organisations/permissions/").json().get("permissions")

    if convert_to_options:
        converted = []

        for item in data:
            converted.append(Option(key=item["id"], value=item["name"]))

        return converted

    return data


def get_user_permissions(request):
    user = get_user(request)
    return user["role"]["permissions"]
