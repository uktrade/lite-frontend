from core import client


def post_f680_application(request, json):
    data = client.post(request, "/exporter/f680/application/", json)
    return data.json(), data.status_code


def get_f680_application(request, application_id):
    data = client.get(request, f"/exporter/f680/application/{application_id}/")
    return data.json(), data.status_code
