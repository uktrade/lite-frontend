from core import client


def get_ecju_query(request, pk, query_pk):
    data = client.get(request, f"/cases/{pk}/ecju-queries/{query_pk}").json()["ecju_query"]
    return data


def put_ecju_query(request, pk, query_pk, json):
    data = client.put(request, f"/cases/{pk}/ecju-queries/{query_pk}/", json)
    return data.json(), data.status_code
