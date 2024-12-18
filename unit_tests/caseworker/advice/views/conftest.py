import pytest


@pytest.fixture
def mock_post_advice(requests_mock, data_standard_case):
    user_advice_create_url = f"/cases/{data_standard_case['case']['id']}/user-advice/"
    return requests_mock.post(user_advice_create_url, json={}, status_code=201)
