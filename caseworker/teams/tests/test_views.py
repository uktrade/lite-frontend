import pytest
from django.urls import reverse
from unit_tests.caseworker.conftest import (
    authorized_client,
    mock_gov_user,
    mock_notifications,
    mock_case_statuses,
    authorized_client_factory,
)
from core import client
import requests
import requests_mock

session = requests.Session()

pk = "67b9a4a3-6f3d-4511-8a19-23ccff221a74"


@pytest.fixture
def form_team_data():
    return {
        "name": "Test",
        "part_of_ecju": True,
        "is_ogd": True,
    }


def test_edit_team_view(authorized_client, form_team_data):
    url = reverse("teams:edit", kwargs={"pk": pk})
    with requests_mock.Mocker() as req_mock:
        req_mock.post(url, json=form_team_data)

        history = req_mock.request_history
        print(history)
        assert len(history) == 1
