from core.constants import CaseStatusEnum
import pytest

from core import client


@pytest.fixture
def f680_case_id():
    return "67271217-7e55-4345-9db4-31de1bfe4067"


@pytest.fixture
def queue_f680_cases_to_review():
    return {
        "id": "5641aa2b-09ca-47f6-adcf-682b0472bc93",
        "alias": "F680 Cases to review",
        "name": "F680 Cases to review",
        "is_system_queue": True,
        "countersigning_queue": None,
    }


@pytest.fixture
def recommendations(current_user, admin_team, data_submitted_f680_case):
    security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
    return [
        {
            "created_at": "2021-10-16T23:48:39.486679+01:00",
            "id": "429c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
            "type": {"key": "approve", "value": "Approve"},
            "conditions": "No concerns",
            "refusal_reasons": "",
            "security_release_request": release_request["id"],
            "user": current_user,
            "team": admin_team,
        }
        for release_request in security_release_requests
    ]


@pytest.fixture
def mock_outcomes_no_outcomes(requests_mock, data_submitted_f680_case):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/outcome/"
    return requests_mock.get(url, json=[], status_code=200)


@pytest.fixture
def data_outcomes(current_user, admin_team, data_submitted_f680_case):
    security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]
    return [
        {
            "id": "429c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
            "created_at": "2021-10-16T23:48:39.486679+01:00",
            "outcome": "approve",
            "conditions": "No concerns",
            "refusal_reasons": None,
            "security_grading": "official",
            "approval_types": ["training"],
            "security_release_requests": [security_release_requests[0]["id"]],
            "user": current_user,
            "team": admin_team,
        }
    ]


@pytest.fixture
def data_outcomes_all_releases(current_user, admin_team, data_submitted_f680_case):
    security_release_requests = data_submitted_f680_case["case"]["data"]["security_release_requests"]

    return [
        {
            "id": "429c5596-fe8b-4540-988b-c37805cd08de",  # /PS-IGNORE
            "created_at": "2021-10-16T23:48:39.486679+01:00",
            "outcome": "approve",
            "conditions": "No concerns",
            "refusal_reasons": None,
            "security_grading": "official",
            "approval_types": ["training"],
            "security_release_requests": [srr["id"]],
            "user": current_user,
            "team": admin_team,
        }
        for srr in security_release_requests
    ]


@pytest.fixture
def mock_outcomes_single_outcome(requests_mock, data_outcomes, data_submitted_f680_case):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/outcome/"
    return requests_mock.get(url, json=data_outcomes, status_code=200)


@pytest.fixture
def mock_outcomes_no_outcome(requests_mock, data_submitted_f680_case):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/outcome/"
    return requests_mock.get(url, json=[], status_code=200)


@pytest.fixture
def mock_outcomes_complete(requests_mock, data_outcomes, data_submitted_f680_case):
    security_release_request_ids = [
        release_request["id"]
        for release_request in data_submitted_f680_case["case"]["data"]["security_release_requests"]
    ]
    data_outcomes[0]["security_release_requests"] = security_release_request_ids
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/outcome/"
    return requests_mock.get(url, json=data_outcomes, status_code=200)


@pytest.fixture
def mock_outcomes_approve_refuse(requests_mock, data_outcomes_all_releases, data_submitted_f680_case):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/outcome/"
    return requests_mock.get(url, json=data_outcomes_all_releases, status_code=200)


@pytest.fixture
def mock_outcomes_complete_approval(requests_mock, data_outcomes, data_submitted_f680_case):
    security_release_request_ids = [
        release_request["id"]
        for release_request in data_submitted_f680_case["case"]["data"]["security_release_requests"]
    ]
    data_outcomes[0]["security_release_requests"] = security_release_request_ids
    data_outcomes[0]["outcome"] = "approve"
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/outcome/"
    return requests_mock.get(url, json=data_outcomes, status_code=200)


@pytest.fixture
def mock_outcomes_complete_refusal(requests_mock, data_outcomes, data_submitted_f680_case):
    security_release_request_ids = [
        release_request["id"]
        for release_request in data_submitted_f680_case["case"]["data"]["security_release_requests"]
    ]
    data_outcomes[0]["security_release_requests"] = security_release_request_ids
    data_outcomes[0]["outcome"] = "refuse"
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/outcome/"
    return requests_mock.get(url, json=data_outcomes, status_code=200)


@pytest.fixture
def mock_f680_case_with_assigned_user(f680_case_id, requests_mock, data_submitted_f680_case, data_queue, mock_gov_user):
    data_submitted_f680_case["case"]["assigned_users"] = {data_queue["name"]: [mock_gov_user["user"]]}
    url = client._build_absolute_uri(f"/cases/{f680_case_id}/")
    return requests_mock.get(url=url, json=data_submitted_f680_case)


@pytest.fixture
def f680_reference_code():
    return "F680/2025/0000016"


@pytest.fixture
def mock_f680_case(f680_case_id, requests_mock, data_submitted_f680_case):
    url = client._build_absolute_uri(f"/cases/{f680_case_id}/")
    return requests_mock.get(url=url, json=data_submitted_f680_case)


@pytest.fixture
def mock_f680_case_under_review(f680_case_id, requests_mock, data_submitted_f680_case):
    url = client._build_absolute_uri(f"/cases/{f680_case_id}/")
    data_submitted_f680_case["case"]["data"]["status"]["key"] = CaseStatusEnum.UNDER_FINAL_REVIEW
    return requests_mock.get(url=url, json=data_submitted_f680_case)


@pytest.fixture
def mock_post_recommendation(requests_mock, data_submitted_f680_case):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/recommendation/"
    return requests_mock.post(url, json={}, status_code=201)


@pytest.fixture
def mock_get_case_recommendations(requests_mock, data_submitted_f680_case, recommendations):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/recommendation/"
    return requests_mock.get(url, json=recommendations, status_code=200)


@pytest.fixture
def mock_get_case_no_recommendations(requests_mock, data_submitted_f680_case, recommendations):
    url = f"/caseworker/f680/{data_submitted_f680_case['case']['id']}/recommendation/"
    return requests_mock.get(url, json=[], status_code=200)


@pytest.fixture
def mock_proviso_no_results(requests_mock):
    url = client._build_absolute_uri("/picklist/?type=proviso&page=1&disable_pagination=True&show_deactivated=False")
    return requests_mock.get(url=url, json={"results": []})


@pytest.fixture
def missing_case_id():
    return "5eb8f65f-9ce0-4dd6-abde-5c3fc00b802c"


@pytest.fixture
def mock_missing_case(missing_case_id, requests_mock):
    url = client._build_absolute_uri(f"/cases/{missing_case_id}/")
    return requests_mock.get(url=url, status_code=404)
