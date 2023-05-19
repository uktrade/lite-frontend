import pytest

from pytest_django.asserts import assertTemplateUsed
from bs4 import BeautifulSoup

from django.urls import reverse

from core import client
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


@pytest.fixture(autouse=True)
def default_feature_flags(settings):
    settings.FEATURE_MENTIONS_ENABLED = True


@pytest.fixture
def mentions_data(data_standard_case, mock_gov_user):
    return {"results": [{"id": data_standard_case["case"]["id"], "user": mock_gov_user["user"]}]}


@pytest.fixture
def mock_case_note_mentions(requests_mock, data_standard_case, mentions_data):
    data_standard_case_pk = data_standard_case["case"]["id"]
    url = client._build_absolute_uri(f"/cases/{data_standard_case_pk}/case-note-mentions/")
    return requests_mock.get(url=url, json=mentions_data)


def test_notes_and_timelines_view_flag_on_status_code(
    authorized_client, notes_and_timelines_url, requests_mock, mock_gov_users
):
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": mock_gov_users,
        },
    )
    response = authorized_client.get(notes_and_timelines_url)
    assert response.status_code == 200


def test_notes_and_timelines_view_templates(authorized_client, notes_and_timelines_url, requests_mock, mock_gov_users):
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": mock_gov_users,
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
    mock_gov_users,
):
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": mock_gov_users,
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
    authorized_client, notes_and_timelines_url, mock_standard_case_activity_system_user, requests_mock, mock_gov_users
):
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": mock_gov_users,
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
    authorized_client, notes_and_timelines_url, mock_standard_case_activity_system_user, requests_mock, mock_gov_users
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


def test_notes_and_timelines_user_dropdown(authorized_client, notes_and_timelines_url, requests_mock, mock_gov_users):
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": mock_gov_users,
        },
    )
    response = authorized_client.get(notes_and_timelines_url)
    users = []
    for user in mock_gov_users:
        value = (
            f'{user["first_name"]} {user["last_name"]} ({user["team"]["name"]})'
            if user["first_name"]
            else user["email"]
        )
        users.append((user["id"], value))
    assert response.context["form"].fields["mentions"].choices == users


@pytest.mark.parametrize(
    "data, mock_data, mock_status, expected_status, template_used",
    (
        (
            {"text": "this is text", "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"], "is_urgent": False},
            {},
            201,
            302,
            "activites/notes-and-timelines.html",
        ),
        (
            {"text": "this is text", "mentions": ["1f288b81-2c26-439f-ac32-2a43c8b1a5cb"], "is_urgent": False},
            {"errors": {"text": ["test"]}},
            400,
            200,
            "error.html",
        ),
    ),
)
def test_notes_and_timelines_post_valid(
    data,
    mock_data,
    mock_status,
    expected_status,
    template_used,
    authorized_client,
    notes_and_timelines_url,
    mock_gov_users,
    data_standard_case,
    requests_mock,
):
    requests_mock.post(
        client._build_absolute_uri(f'/cases/{data_standard_case["case"]["id"]}/case-notes/'),
        json=mock_data,
        status_code=mock_status,
    )
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": mock_gov_users,
        },
    )

    response = authorized_client.post(notes_and_timelines_url, data=data)
    assert response.status_code == expected_status
    if expected_status == 302:
        assert response.url == notes_and_timelines_url
    else:
        assertTemplateUsed(response, template_used)


def test_notes_and_timelines_mentions(
    authorized_client, notes_and_timelines_url, mock_case_note_mentions, mentions_data, requests_mock, mock_gov_users
):
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": mock_gov_users,
        },
    )
    response = authorized_client.get(f"{notes_and_timelines_url}?mentions=True")
    assert response.context["mentions"][0]["id"] == mentions_data["results"][0]["id"]
    assert not response.context.get("activities")


def test_notes_and_timelines_mentions_template(
    authorized_client, notes_and_timelines_url, mock_case_note_mentions, requests_mock, mock_gov_users
):

    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": mock_gov_users,
        },
    )
    response = authorized_client.get(f"{notes_and_timelines_url}?mentions=True")
    soup = BeautifulSoup(response.content, "html.parser")

    assert soup.find("ul", {"class": "notes-and-timeline-nav__mentions"})


def test_notes_and_timelines_mentions_feature_flag(
    authorized_client, notes_and_timelines_url, mock_case_note_mentions, settings, requests_mock, mock_gov_users
):
    settings.FEATURE_MENTIONS_ENABLED = False
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/"),
        json={
            "results": mock_gov_users,
        },
    )
    response = authorized_client.get(f"{notes_and_timelines_url}?mentions=True")
    soup = BeautifulSoup(response.content, "html.parser")

    assert not soup.find("ul", {"class": "notes-and-timeline-nav__mentions"})
