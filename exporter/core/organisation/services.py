from core import client


def register_organisation(request, json):
    data = {
        "user": {"email": request.session["email"]},
    }
    response = client.post(request, "/organisations/", {**json, **data})
    return response.json(), response.status_code


def update_organisation(request, pk, json):
    response = client.put(request, f"/organisations/{pk}/update/", json)
    return response.json(), response.status_code
