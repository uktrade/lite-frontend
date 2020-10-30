from core import client


def get_ecju_query(request, pk, query_pk):
    data = client.get(request, f"/cases/{pk}/ecju-queries/{query_pk}").json()["ecju_query"]
    return data


def put_ecju_query(request, pk, query_pk, json):
    data = client.put(request, f"/cases/{pk}/ecju-queries/{query_pk}/", json)
    return data.json(), data.status_code


# Document Sensitivity
def get_ecju_query_document_missing_reasons(request):
    response = client.get(request, "/static/missing-document-reasons/ecju-query")
    response.raise_for_status()
    return response.json(), response.status_code


def post_ecju_query_document_sensitivity(request, pk, query_pk, json):
    response = client.post(request, f"/cases/{pk}/ecju-queries/{query_pk}/document-sensitivity/", json)
    return response.json(), response.status_code


def post_ecju_query_document(request, pk, query_pk, json):
    if "description" not in json:
        json["description"] = ""
    json = [json]

    data = client.post(request, f"/cases/{pk}/ecju-queries/{query_pk}/document/", json)
    return data.json(), data.status_code
