from core import client


def post_document_on_organisation(request, organisation_id, data):
    response = client.post(request, f"/organisations/{organisation_id}/documents/", data)
    response.raise_for_status()
    return response


def get_document_on_organisation(request, organisation_id, document_id):
    response = client.get(request, f"/organisations/{organisation_id}/document/{document_id}/")
    response.raise_for_status()
    return response
