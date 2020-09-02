from core import client


def authenticate_gov_user(request, json):
    data = client.post(request, "/gov-users/authenticate/", json)
    return data.json(), data.status_code
