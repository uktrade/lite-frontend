import pytest

from bs4 import BeautifulSoup
from pytest_django.asserts import assertTemplateUsed
from urllib import parse

from django.urls import reverse

from caseworker.queues.rules import BULK_APPROVE_ALLOWED_QUEUES
from core import client


@pytest.fixture
def mod_queue_id():
    return BULK_APPROVE_ALLOWED_QUEUES["MOD_CAPPROT"]


@pytest.fixture
def fcdo_queue_id():
    return "12346bed-fd45-4293-95b8-eda9468aa254"


@pytest.fixture
def mod_bulk_approval_url(request, mod_queue_id):
    return reverse(f"queues:bulk_approval", kwargs={"pk": mod_queue_id})


@pytest.fixture
def mock_post_mod_bulk_approval_recommendation(requests_mock, mod_queue_id):
    url = client._build_absolute_uri(f"/caseworker/queues/{mod_queue_id}/bulk-approval/")
    yield requests_mock.post(url=url, json={}, status_code=201)


@pytest.fixture
def fcdo_queue_view(request, fcdo_queue_id):
    return reverse(f"queues:cases", kwargs={"queue_pk": fcdo_queue_id})


@pytest.fixture
def mock_get_fcdo_queue_cases(requests_mock, fcdo_queue_id):
    url = client._build_absolute_uri(f"/queues/{fcdo_queue_id}/")
    yield requests_mock.get(url=url, json={})


@pytest.fixture
def mock_fcdo_queue_detail(requests_mock, fcdo_queue_id):
    url = client._build_absolute_uri(f"/queues/{fcdo_queue_id}/")
    yield requests_mock.get(url=url, json={"id": fcdo_queue_id})


@pytest.fixture
def mock_fcdo_queue_search_data(requests_mock, fcdo_queue_id):
    query_params = {"queue_id": fcdo_queue_id, "page": 1, "selected_tab": "all_cases", "hidden": False}
    url = client._build_absolute_uri(f"/cases/")
    url = f"{url}?{parse.urlencode(query_params, doseq=True)}"
    yield requests_mock.get(url=url, json={"results": {"cases": [], "filters": {"gov_users": []}}})


@pytest.mark.parametrize(
    "cases",
    (
        (["54725d74-e900-43b1-b2cb-2af44ae9182d", "2468bc19-979d-4ba3-a57c-b0ce253c6237"]),
        (["54725d74-e900-43b1-b2cb-2af44ae9182d"]),
    ),
)
def test_user_bulk_approval_success(
    authorized_client,
    requests_mock,
    MOD_team1_user,
    mod_bulk_approval_url,
    mock_gov_mod_capprot_user,
    mock_post_mod_bulk_approval_recommendation,
    cases,
):
    data = {
        "cases": cases,
        "advice": {
            "text": "No concerns: Approved using bulk approval",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "team": str(MOD_team1_user["team"]["id"]),
        },
    }
    response = authorized_client.post(mod_bulk_approval_url, data=data)
    assert response.status_code == 302

    bulk_approval_request = requests_mock.request_history.pop()
    assert bulk_approval_request.method == "POST"
    assert bulk_approval_request.json() == data


def test_bulk_approval_missing_for_nonpermitted_users(
    authorized_client,
    fcdo_queue_view,
    mock_get_fcdo_queue_cases,
    mock_fcdo_queue_search_data,
    mock_cases_search_head,
    mock_control_list_entries,
    mock_regime_entries,
    mock_countries,
    mock_queues_list,
    mock_fcdo_queue_detail,
    mock_bookmarks,
):
    response = authorized_client.get(fcdo_queue_view)
    assertTemplateUsed(response, "queues/cases.html")
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("button", {"id": "bulk-approve-button"}) is None
