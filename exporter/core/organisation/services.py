from core import client


def register_organisation(request, json):

    data = {
        "user": {"email": request.session["email"]},
    }
    response = client.post(request, "/organisations/", {**json, **data})
    return response.json(), response.status_code


def validate_organisation(request, json):
    json["validate_only"] = True
    return register_organisation(request, json)


def validate_registration_number(request, json):
    response = client.post(request, "/organisations/registration_number", {**json})
    return response.json(), response.status_code
