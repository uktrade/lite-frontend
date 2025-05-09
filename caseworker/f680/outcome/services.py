from json.decoder import JSONDecodeError

from core import client


def post_outcome(request, case_id, data):
    response = client.post(request, f"/caseworker/f680/{case_id}/outcome/", data)
    return response.json(), response.status_code


def get_outcomes(request, case_id):
    response = client.get(request, f"/caseworker/f680/{case_id}/outcome/")
    return response.json(), response.status_code


def delete_outcome(request, case_id, outcome_id):
    response = client.delete(request, f"/caseworker/f680/{case_id}/outcome/{outcome_id}/")
    try:
        body = response.json()
    except JSONDecodeError:
        body = None
    return body, response.status_code


def get_hydrated_outcomes(request, case):
    response = client.get(request, f"/caseworker/f680/{case['id']}/outcome/")
    response.raise_for_status()
    security_release_requests_by_id = {
        release_request["id"]: release_request for release_request in case["data"]["security_release_requests"]
    }
    outcomes = []
    for outcome in response.json():
        outcome["security_release_request_ids"] = outcome["security_release_requests"]
        release_requests = []
        for release_request_id in outcome["security_release_request_ids"]:
            release_requests.append(security_release_requests_by_id[release_request_id])
        outcome["security_release_requests"] = release_requests

        outcomes.append(outcome)
    return outcomes, response.status_code


def get_releases_with_no_outcome(request, existing_outcomes, case):
    release_requests_with_outcome = set()
    for outcome in existing_outcomes:
        release_requests_with_outcome.update(outcome["security_release_requests"])
    remaining_request_ids_without_outcome = set()
    remaining_requests_without_outcome = []
    for release_request in case.data["security_release_requests"]:
        if release_request["id"] in release_requests_with_outcome:
            continue
        remaining_requests_without_outcome.append(release_request)
        remaining_request_ids_without_outcome.add(release_request["id"])
    return remaining_requests_without_outcome, remaining_request_ids_without_outcome


def get_outcome_documents(request, case_id):
    response = client.get(request, f"/caseworker/f680/{case_id}/outcome_document/")
    return response.json(), response.status_code


def get_required_outcome_documents(letter_templates, outcome_docs):
    required_outcome_documents = letter_templates.copy()
    for required_outcome_document in required_outcome_documents:
        for outcome_doc in outcome_docs:
            if required_outcome_document["id"] == outcome_doc["template"]:
                required_outcome_document["generated_document"] = outcome_doc
    return required_outcome_documents
