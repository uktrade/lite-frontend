from core import client


def post_f680_application(request, json):
    data = client.post(request, "/exporter/f680/", json)
    return data.json(), data.status_code
