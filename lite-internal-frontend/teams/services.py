from lite_forms.components import Option

from conf.client import get, post, put
from conf.constants import TEAMS_URL


def get_teams(request, converted_to_options=False):
    data = get(request, TEAMS_URL)

    if converted_to_options:
        converted_units = []

        for team in data.json().get("teams"):
            converted_units.append(Option(team.get("id"), team.get("name")))

        return converted_units

    return data.json(), data.status_code


def get_users_team_queues(request, user, convert_to_options=True):
    data = get(request, "/users/" + user + "/team-queues/").json()
    if convert_to_options:
        return [Option(key=queue[0], value=queue[1], description=None) for queue in data["queues"]]
    return data, data.status_code


def post_teams(request, json):
    data = post(request, TEAMS_URL, json)
    return data.json(), data.status_code


def get_team(request, pk):
    data = get(request, TEAMS_URL + str(pk))
    return data.json(), data.status_code


def put_team(request, pk, json):
    data = put(request, TEAMS_URL + str(pk) + "/", json)
    return data.json(), data.status_code


def get_users_by_team(request, pk):
    data = get(request, TEAMS_URL + pk + "/users")
    return data.json(), data.status_code
