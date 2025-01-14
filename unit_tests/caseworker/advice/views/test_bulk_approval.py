import pytest
import re

from bs4 import BeautifulSoup
from pytest_django.asserts import assertTemplateUsed
from urllib import parse

from django.urls import reverse

from caseworker.advice.constants import (
    DESNZ_CHEMICAL,
    DESNZ_NUCLEAR,
    FCDO_TEAM,
    MOD_CAPPROT_TEAM,
    MOD_DI_TEAM,
    MOD_DSR_TEAM,
    MOD_DSTL_TEAM,
    MOD_ECJU,
    NCSC_TEAM,
    DESNZ_CHEMICAL_CASES_TO_REVIEW,
    DESNZ_NUCLEAR_CASES_TO_REVIEW,
    FCDO_CASES_TO_REVIEW_QUEUE,
    MOD_CAPPROT_CASES_TO_REVIEW,
    MOD_DI_DIRECT_CASES_TO_REVIEW,
    MOD_DI_INDIRECT_CASES_TO_REVIEW,
    MOD_DSR_CASES_TO_REVIEW,
    MOD_DSTL_CASES_TO_REVIEW,
    MOD_ECJU_REVIEW_AND_COMBINE,
    NCSC_CASES_TO_REVIEW,
)
from core import client


@pytest.fixture
def mock_get_queue_cases(requests_mock):
    def _mock_get_queue_cases(queue_id):
        url = client._build_absolute_uri(f"/queues/{queue_id}/")
        return requests_mock.get(url=url, json={})

    return _mock_get_queue_cases


@pytest.fixture
def mock_get_queue_detail(requests_mock):
    def _mock_get_queue_detail(queue_id):
        url = client._build_absolute_uri(f"/queues/{queue_id}/")
        return requests_mock.get(url=url, json={"id": queue_id})

    return _mock_get_queue_detail


@pytest.fixture
def mock_get_queue_search_data(requests_mock):
    def _mock_get_queue_search_data(queue_id):
        query_params = {"queue_id": queue_id, "page": 1, "selected_tab": "all_cases", "hidden": False}
        url = client._build_absolute_uri(f"/cases/")
        url = f"{url}?{parse.urlencode(query_params, doseq=True)}"
        return requests_mock.get(url=url, json={"results": {"cases": [], "filters": {"gov_users": []}}})

    return _mock_get_queue_search_data


@pytest.fixture
def OGD_team_user(gov_uk_user_id):
    def _OGD_team_user(team_id):
        return {
            "email": "ogd.team@example.com",
            "first_name": "OGD Team",
            "id": gov_uk_user_id,
            "last_name": "User",
            "role_name": "Super User",
            "status": "Active",
            "team": {
                "id": team_id,
                "name": "OGD Team",
                "alias": "OGD_TEAM",
                "part_of_ecju": False,
                "is_ogd": True,
            },
        }

    return _OGD_team_user


@pytest.mark.parametrize(
    "team_id, queue_id",
    (
        (MOD_CAPPROT_TEAM, MOD_CAPPROT_CASES_TO_REVIEW),
        (MOD_DI_TEAM, MOD_DI_DIRECT_CASES_TO_REVIEW),
        (MOD_DI_TEAM, MOD_DI_INDIRECT_CASES_TO_REVIEW),
        (MOD_DSR_TEAM, MOD_DSR_CASES_TO_REVIEW),
        (MOD_DSTL_TEAM, MOD_DSTL_CASES_TO_REVIEW),
        (NCSC_TEAM, NCSC_CASES_TO_REVIEW),
    ),
)
def test_user_bulk_approval_success(
    authorized_client,
    requests_mock,
    mock_gov_user,
    OGD_team_user,
    team_id,
    queue_id,
):
    # setup mock requests
    # There are multiple fixtures that require parameterizing hence these cannot
    # be parameterized outside of this test
    url = client._build_absolute_uri(f"/caseworker/queues/{queue_id}/bulk-approval/")
    requests_mock.post(url=url, json={}, status_code=201)

    ogd_advisor = OGD_team_user(team_id)
    mock_gov_user["user"]["team"] = ogd_advisor["team"]

    url = client._build_absolute_uri("/gov-users/")
    requests_mock.get(url=f"{url}me/", json=mock_gov_user)
    requests_mock.get(url=re.compile(f"{url}{mock_gov_user['user']['id']}/"), json=mock_gov_user)

    data = {
        "cases": ["54725d74-e900-43b1-b2cb-2af44ae9182d", "2468bc19-979d-4ba3-a57c-b0ce253c6237"],
        "advice": {
            "text": "No concerns: Approved using bulk approval",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "team": team_id,
        },
    }
    url = reverse("queues:bulk_approval", kwargs={"pk": queue_id})
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302

    bulk_approval_request = requests_mock.request_history.pop()
    assert bulk_approval_request.method == "POST"
    assert bulk_approval_request.json() == data


@pytest.mark.parametrize(
    "team_id, queue_id",
    (
        # team_id is not required in this test but included for completenes
        (FCDO_TEAM, FCDO_CASES_TO_REVIEW_QUEUE),
        (DESNZ_CHEMICAL, DESNZ_CHEMICAL_CASES_TO_REVIEW),
        (DESNZ_NUCLEAR, DESNZ_NUCLEAR_CASES_TO_REVIEW),
        (MOD_ECJU, MOD_ECJU_REVIEW_AND_COMBINE),
    ),
)
def test_user_bulk_approval_not_available_error(
    authorized_client,
    requests_mock,
    team_id,
    queue_id,
):
    url = client._build_absolute_uri(f"/caseworker/queues/{queue_id}/bulk-approval/")
    bulk_approval_request = requests_mock.post(url=url, json={}, status_code=201)

    url = reverse("queues:bulk_approval", kwargs={"pk": queue_id})
    response = authorized_client.post(url, data={})
    assert response.status_code == 404

    assert bulk_approval_request.call_count == 0


@pytest.mark.parametrize(
    "queue_id, expected",
    (
        (DESNZ_CHEMICAL_CASES_TO_REVIEW, False),
        (DESNZ_NUCLEAR_CASES_TO_REVIEW, False),
        (FCDO_CASES_TO_REVIEW_QUEUE, False),
        (MOD_ECJU_REVIEW_AND_COMBINE, False),
        (MOD_CAPPROT_CASES_TO_REVIEW, True),
        (MOD_DI_DIRECT_CASES_TO_REVIEW, True),
        (MOD_DI_INDIRECT_CASES_TO_REVIEW, True),
        (MOD_DSR_CASES_TO_REVIEW, True),
        (MOD_DSTL_CASES_TO_REVIEW, True),
        (NCSC_CASES_TO_REVIEW, True),
    ),
)
def test_bulk_approval_button_status_for_ogd_queue(
    authorized_client,
    mock_get_queue_cases,
    mock_get_queue_search_data,
    mock_cases_search_head,
    mock_control_list_entries,
    mock_regime_entries,
    mock_countries,
    mock_queues_list,
    mock_get_queue_detail,
    mock_bookmarks,
    queue_id,
    expected,
):
    mock_get_queue_cases(queue_id)
    mock_get_queue_search_data(queue_id)
    mock_get_queue_detail(queue_id)

    url = reverse(f"queues:cases", kwargs={"queue_pk": queue_id})
    response = authorized_client.get(url)
    assertTemplateUsed(response, "queues/cases.html")
    soup = BeautifulSoup(response.content, "html.parser")
    assert bool(soup.find("button", {"id": "bulk-approve-button"})) is expected
