from core import client


def get_680_application(request, application_id):
    data = client.get(request, f"/exporter/f680/{application_id}/")
    return data.json()


def post_f680_application(request, json):
    data = client.post(request, "/exporter/f680/", json)
    return data.json(), data.status_code
