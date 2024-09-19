from core import client


def create_exporter_user(request, org_pk, json):
    response = client.post(request, f"/caseworker/organisations/{org_pk}/exporter-users/", json)
    response.raise_for_status()
    return response.json(), response.status_code
