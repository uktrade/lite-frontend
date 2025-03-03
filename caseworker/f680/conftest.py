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
def mock_post_recommendation(requests_mock, data_submitted_f680_case):
    user_recommendation_create_url = f"/cases/{data_submitted_f680_case['case']['id']}/user-advice/"
    return requests_mock.post(user_recommendation_create_url, json={}, status_code=201)


@pytest.fixture
def mock_proviso_no_results(requests_mock):
    url = client._build_absolute_uri("/picklist/?type=proviso&page=1&disable_pagination=True&show_deactivated=False")
    return requests_mock.get(url=url, json={"results": []})
