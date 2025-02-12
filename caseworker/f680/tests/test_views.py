import pytest
from datetime import timedelta
from requests.exceptions import HTTPError

from bs4 import BeautifulSoup
from django.urls import reverse
from django.utils import timezone

from core import client


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_approval_reason,
    mock_denial_reasons,
    mock_proviso,
    mock_footnote_details,
):
    return


@pytest.fixture
def missing_case_id():
    return "5eb8f65f-9ce0-4dd6-abde-5c3fc00b802c"


@pytest.fixture
def mock_missing_case(missing_case_id, requests_mock):
    url = client._build_absolute_uri(f"/cases/{missing_case_id}/")
    return requests_mock.get(url=url, status_code=404)


@pytest.fixture
def f680_case_id():
    return "67271217-7e55-4345-9db4-31de1bfe4067"


@pytest.fixture
def f680_reference_code():
    return "F680/2025/0000016"


@pytest.fixture
def data_f680_case(f680_case_id, f680_reference_code):
    submitted_at = timezone.now() - timedelta(days=7)
    return {
        "case": {
            "advice": [],
            "all_flags": [],
            "amendment_of": None,
            "assigned_users": {},
            "case_officer": None,
            "case_type": {
                "id": "00000000-0000-0000-0000-000000000007",
                "reference": {"key": "f680", "value": "MOD F680 Clearance"},
                "sub_type": {"key": "f680_clearance", "value": "MOD F680 Clearance"},
                "type": {"key": "application", "value": "Application"},
            },
            "copy_of": None,
            "countersign_advice": [],
            "data": {
                "application": {"some": "json"},
                "id": f680_case_id,
                "organisation": {
                    "id": "1363b104-9669-4c53-8602-8fc3717b07cd",  # /PS-IGNORE
                    "name": "Parrish, Crosby and Friedman",
                    "status": "active",
                    "type": "commercial",
                },
                "reference_code": f680_reference_code,
                "status": {"id": "00000000-0000-0000-0000-000000000001", "key": "submitted", "value": "Submitted"},
                "submitted_at": submitted_at.isoformat(),
                "submitted_by": None,
            },
            "flags": [],
            "has_advice": {"final": False, "my_team": False, "my_user": False, "team": False, "user": False},
            "id": f680_case_id,
            "latest_activity": None,
            "licences": [],
            "queue_details": [],
            "queue_names": [],
            "queues": [],
            "reference_code": "F680/2025/0000016",
            "sla_days": 0,
            "sla_remaining_days": None,
            "submitted_at": submitted_at.isoformat(),
            "superseded_by": None,
        }
    }


@pytest.fixture
def mock_f680_case(f680_case_id, requests_mock, data_f680_case):
    url = client._build_absolute_uri(f"/cases/{f680_case_id}/")
    return requests_mock.get(url=url, json=data_f680_case)


class TestCaseDetailView:

    def test_GET_success(
        self, authorized_client, data_queue, mock_f680_case, f680_case_id, f680_reference_code, data_f680_case
    ):
        url = reverse("cases:f680:details", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        response = authorized_client.get(url)
        assert response.status_code == 200
        assert dict(response.context["case"]) == data_f680_case["case"]
        soup = BeautifulSoup(response.content, "html.parser")
        assert f680_reference_code in soup.find("h1").text

    def test_GET_not_logged_in(
        self, client, data_queue, mock_f680_case, f680_case_id, f680_reference_code, data_f680_case
    ):
        url = reverse("cases:f680:details", kwargs={"queue_pk": data_queue["id"], "pk": f680_case_id})
        expected_redirect_location = reverse("auth:login")
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith(expected_redirect_location)

    def test_GET_no_case_404(self, authorized_client, data_queue, missing_case_id, mock_missing_case):
        url = reverse("cases:f680:details", kwargs={"queue_pk": data_queue["id"], "pk": missing_case_id})
        with pytest.raises(HTTPError, match="404"):
            authorized_client.get(url)
