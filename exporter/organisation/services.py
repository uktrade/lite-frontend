from core import client


def post_organisation_documents(request, organisation_id, data):
    response = client.post(request, f"/organisations/{organisation_id}/documents/", data)
    response.raise_for_status()
    return response
