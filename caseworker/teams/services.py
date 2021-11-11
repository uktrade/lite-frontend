from lite_forms.components import Option

from core import client


def get_teams(request, converted_to_options=False):
    data = client.get(request, "/teams/")

    if converted_to_options:
        converted_units = []

        for team in data.json().get("teams"):
            converted_units.append(Option(team.get("id"), team.get("name")))

        return converted_units

    return data.json()["teams"]


def get_users_team_queues(request, user, convert_to_options=True):
    data = client.get(request, f"/users/{user}/team-queues/")
    if convert_to_options:
        data = data.json()
        return [Option(key=queue[0], value=queue[1], description=None) for queue in data["queues"]]
    return data.json(), data.status_code


def post_teams(request, json):
    data = client.post(request, "/teams/", json)
    return data.json(), data.status_code


def get_team(request, pk):
    data = client.get(request, f"/teams/{pk}")
    return data.json(), data.status_code


def put_team(request, pk, json):
    data = client.put(request, f"/teams/{pk}/", json)
    return data.json(), data.status_code


def get_users_by_team(request, pk, convert_to_options=False):
    data = client.get(request, f"/teams/{pk}/users")
    if convert_to_options:
        return [Option(user["id"], user["email"]) for user in data.json()["users"] if user["email"]]
    return data.json(), data.status_code


def get_team_queues(request, pk, convert_to_options=False, ignore_pagination=False):
    post_fix = "?disable_pagination=True" if ignore_pagination else ""
    data = client.get(request, f"/teams/{pk}/queues/" + post_fix)
    if convert_to_options:
        return [Option(key=queue["id"], value=queue["name"], description=None) for queue in data.json()]
    return data.json()
