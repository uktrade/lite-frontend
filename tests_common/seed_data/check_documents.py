from . import make_requests
from ..tools import wait


def check_document(url, base_url, export_headers):
    response = make_requests.make_request("GET", base_url=base_url, url=url, headers=export_headers)
    return response.json()['document']['safe']


def check_end_user_document_is_processed(draft_id, base_url, export_headers):
    return check_document('/applications/' + draft_id + '/end-user/document/', base_url, export_headers)


def check_consignee_document_is_processed(draft_id, base_url, export_headers):
    return check_document('/applications/' + draft_id + '/consignee/document/', base_url, export_headers)


def check_ultimate_end_user_document_is_processed(draft_id, ultimate_end_user_id, base_url, export_headers):
    return check_document('/applications/' + draft_id + '/ultimate-end-user/' + ultimate_end_user_id + '/document/',
                          base_url, export_headers)


def check_third_party_document_is_processed(draft_id, third_party_id, base_url, export_headers):
    return check_document('/applications/' + draft_id + '/third-parties/' + third_party_id + '/document/', base_url,
                          export_headers)


def check_additional_document_is_processed(draft_id, document_id, base_url, export_headers):
    return check_document('/applications/' + draft_id + '/documents/' + document_id + '/', base_url, export_headers)


def check_documents(base_url, export_headers, draft_id, ultimate_end_user_id, third_party_id, additional_document_id):
    end_user_document_is_processed = wait.wait_for_document(
        func=check_end_user_document_is_processed, draft_id=draft_id, base_url=base_url, export_headers=export_headers)
    assert end_user_document_is_processed, "End user document wasn't successfully processed"
    consignee_document_is_processed = wait.wait_for_document(
        func=check_consignee_document_is_processed, draft_id=draft_id, base_url=base_url, export_headers=export_headers)
    assert consignee_document_is_processed, "Consignee document wasn't successfully processed"
    ultimate_end_user_document_is_processed = wait.wait_for_ultimate_end_user_document(
        func=check_ultimate_end_user_document_is_processed, draft_id=draft_id,
        ultimate_end_user_id=ultimate_end_user_id, base_url=base_url, export_headers=export_headers)
    assert ultimate_end_user_document_is_processed, "Ultimate end user document wasn't successfully processed"
    third_party_document_is_processed = wait.wait_for_third_party_document(
        func=check_third_party_document_is_processed, draft_id=draft_id,
        third_party_id=third_party_id, base_url=base_url, export_headers=export_headers)
    assert third_party_document_is_processed, "Third party document wasn't successfully processed"
    additional_document_is_processed = wait.wait_for_additional_document(
        func=check_additional_document_is_processed, draft_id=draft_id,
        document_id=additional_document_id, base_url=base_url, export_headers=export_headers)
    assert additional_document_is_processed, "Additional document wasn't successfully processed"
