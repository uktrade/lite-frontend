import pytest

from core import client


@pytest.fixture
def f680_case_id():
    return "67271217-7e55-4345-9db4-31de1bfe4067"


@pytest.fixture
def mock_f680_case_with_assigned_user(f680_case_id, requests_mock, data_submitted_f680_case, data_queue, mock_gov_user):
    data_submitted_f680_case["case"]["assigned_users"] = {data_queue["name"]: [mock_gov_user["user"]]}
    url = client._build_absolute_uri(f"/cases/{f680_case_id}/")
    return requests_mock.get(url=url, json=data_submitted_f680_case)
