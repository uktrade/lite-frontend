import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from caseworker.cases.objects import Case
from core import client


@pytest.fixture(autouse=True)
def setup(
    settings,
    mock_queue,
    mock_case,
    mock_standard_case_activity_filters,
    mock_standard_case_activity_system_user,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
):
    yield


def test_notes_and_timeline_tab(authorized_client, data_queue, data_standard_case):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    assertTemplateUsed(response, "layouts/case.html")
    assert response.context["tabs"][5].name == "Notes and timeline"


@pytest.fixture
def notes_and_timelines_url(data_queue, data_standard_case):
    return reverse(
        "cases:activities:notes-and-timeline",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


def test_notes_and_timelines_view_flag_on_status_code(authorized_client, notes_and_timelines_url, requests_mock):
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": [],
        },
    )
    response = authorized_client.get(notes_and_timelines_url)
    assert response.status_code == 200


def test_notes_and_timelines_view_templates(authorized_client, notes_and_timelines_url, requests_mock):
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": [],
        },
    )
    response = authorized_client.get(notes_and_timelines_url)
    assertTemplateUsed(response, "activities/notes-and-timeline.html")
    assertTemplateUsed(response, "layouts/case.html")
    assertTemplateUsed(response, "includes/case-tabs.html")


def test_notes_and_timelines_context_data(
    authorized_client,
    notes_and_timelines_url,
    data_standard_case,
    standard_case_activity,
    data_queue,
    mock_standard_case_activity_system_user,
    mock_gov_user,
    requests_mock,
):
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": [],
        },
    )
    response = authorized_client.get(notes_and_timelines_url)
    assert response.context["case"] == Case(data_standard_case["case"])
    assert response.context["queue"] == data_queue
    assert response.context["activities"] == standard_case_activity["activity"]
    assert response.context["current_user"] == mock_gov_user["user"]
    assert not response.context["filtering_by"]
    assert response.context["team_filters"] == [
        (
            "e0cb73c5-6bca-447c-b2a3-688fe259f0e9",
            "Team 1",
            "/queues/00000000-0000-0000-0000-000000000001/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/activities/?team_id=e0cb73c5-6bca-447c-b2a3-688fe259f0e9",
            False,
        ),
        (
            "4db83c63-1184-4569-a488-491a0b1b351d",
            "Team 2",
            "/queues/00000000-0000-0000-0000-000000000001/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/activities/?team_id=4db83c63-1184-4569-a488-491a0b1b351d",
            False,
        ),
    ]


def test_notes_and_timelines_searching_by_team(
    authorized_client, notes_and_timelines_url, mock_standard_case_activity_system_user, requests_mock
):
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": [],
        },
    )
    response = authorized_client.get(f"{notes_and_timelines_url}?team_id=e0cb73c5-6bca-447c-b2a3-688fe259f0e9")
    assert mock_standard_case_activity_system_user.last_request.qs == {
        "team_id": ["e0cb73c5-6bca-447c-b2a3-688fe259f0e9"]
    }
    assert response.context["filtering_by"] == ["team_id"]
    assert response.context["team_filters"] == [
        (
            "e0cb73c5-6bca-447c-b2a3-688fe259f0e9",
            "Team 1",
            "/queues/00000000-0000-0000-0000-000000000001/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/activities/?team_id=e0cb73c5-6bca-447c-b2a3-688fe259f0e9",
            True,
        ),
        (
            "4db83c63-1184-4569-a488-491a0b1b351d",
            "Team 2",
            "/queues/00000000-0000-0000-0000-000000000001/cases/8fb76bed-fd45-4293-95b8-eda9468aa254/activities/?team_id=4db83c63-1184-4569-a488-491a0b1b351d",
            False,
        ),
    ]


def test_notes_and_timelines_searching_by_user_type(
    authorized_client, notes_and_timelines_url, mock_standard_case_activity_system_user, requests_mock
):
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": [],
        },
    )
    response = authorized_client.get(f"{notes_and_timelines_url}?user_type=exporter")
    assert mock_standard_case_activity_system_user.last_request.qs == {"user_type": ["exporter"]}
    assert response.context["filtering_by"] == ["user_type"]
