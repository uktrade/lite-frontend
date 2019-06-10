from conf.client import get, post, put
from conf.constants import TEAMS_URL


def get_teams(request):
    data = get(request, TEAMS_URL)
    return data.json(), data.status_code


def post_teams(request, json):
    data = post(request, TEAMS_URL, json)
    return data.json(), data.status_code


def get_team(request, pk):
    data = get(request, TEAMS_URL + pk)
    return data.json(), data.status_code


def update_team(request, pk, json):
    data = put(request, TEAMS_URL + pk + "/", json)
    return data.json(), data.status_code
