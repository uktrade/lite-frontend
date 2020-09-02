from core import client


def authenticate_exporter_user(request, json):
    data = client.post(request, "/users/authenticate/", json)
    return data.json(), data.status_code
