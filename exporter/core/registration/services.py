from core import client


def register_organisation(request, json):
    data = {
        "user": {"email": request.session["email"]},
    }
    print(json)
    response = client.post(request, "/organisations/", {**json, **data})
    return response.json(), response.status_code
