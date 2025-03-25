from core import client


def post_outcome(request, case_id, data):
    response = client.post(request, f"/caseworker/f680/{case_id}/outcome/", data)
    return response.json(), response.status_code


def get_outcomes(request, case_id):
    response = client.get(request, f"/caseworker/f680/{case_id}/outcome/")
    return response.json(), response.status_code
