import pytest
import uuid

from django.urls import reverse
from bs4 import BeautifulSoup
from core import client
from pytest_django.asserts import assertTemplateUsed
from requests.exceptions import HTTPError

from caseworker.core.constants import (
    ADMIN_TEAM_ID,
    SUPER_USER_ROLE_ID,
)
from unit_tests.caseworker.conftest import GOV_USER_ID


@pytest.fixture(autouse=True)
def setup(
    settings,
    mock_queue,
    mock_case,
    mock_standard_case_activity_filters,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
):
    yield


@pytest.mark.parametrize(
    "data, count",
    (
        ({"count": 1}, 1),
        ({"count": 3}, 3),
        ({"count": 0}, 0),
    ),
)
def test_user_case_note_mention_count(data, count, authorized_client, requests_mock):
    requests_mock.get(
        client._build_absolute_uri("/cases/user-case-note-mentions-new-count/"),
        json=data,
    )
    response = authorized_client.get(
        reverse("teams:teams"),
    )
    assert response.status_code == 200
    assert response.context["NEW_MENTIONS_COUNT"] == count


def test_user_case_note_mention_count_error(authorized_client, requests_mock, data_queue, data_standard_case):
    data = {}
    requests_mock.get(
        client._build_absolute_uri("/cases/user-case-note-mentions-new-count/"),
        status_code=500,
        json=data,
    )

    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    with pytest.raises(HTTPError) as exc_info:
        response = authorized_client.get(url)
    exception = exc_info.value
    assert exception.response.status_code == 500


def test_user_case_note_mentions(authorized_client, requests_mock):
    mentions_data = {
        "results": [
            {
                "case_queue_id": "f65fbf49-c14b-482b-833f-fe39bb26a51d",  # /PS-IGNORE
                "case_id": "4966212d-5b52-4a6d-9e06-e589ab9dc221",  # /PS-IGNORE
                "id": "f65fbf49-c14b-482b-833f-hdkwhdke79",  # /PS-IGNORE
                "is_accessed": True,
                "user": {"id": 123},
            }
        ]
    }
    requests_mock.get(
        client._build_absolute_uri("/cases/user-case-note-mentions/"),
        json=mentions_data,
    )

    url = reverse("users:user_case_note_mentions")
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert response.context["data"] == mentions_data

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("table", {"class": "govuk-table"}).find("tr", {"id": "mentions-row-1"})


def test_user_case_note_mentions_update_is_accessed(authorized_client, requests_mock):
    mentions_data = {
        "results": [
            {
                "case_queue_id": "f65fbf49-c14b-482b-833f-fe39bb26a51d",  # /PS-IGNORE
                "case_id": "4966212d-5b52-4a6d-9e06-e589ab9dc221",  # /PS-IGNORE
                "id": "f65fbf49-c14b-482b-833f-hdkwhdke79",  # /PS-IGNORE
                "is_accessed": False,
                "user": {"id": 123},
            }
        ]
    }
    requests_mock.get(
        client._build_absolute_uri("/cases/user-case-note-mentions/"),
        json=mentions_data,
    )

    mock_case_note_mention_update = requests_mock.put(client._build_absolute_uri("/cases/case-note-mentions/"), json={})

    url = reverse("users:user_case_note_mentions")
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert mock_case_note_mention_update.called_once
    last_request = mock_case_note_mention_update.last_request
    assert last_request.json() == [{"id": "f65fbf49-c14b-482b-833f-hdkwhdke79", "is_accessed": True}]  # /PS-IGNORE


def test_view_user(authorized_client, requests_mock):
    user_id = str(uuid.uuid4())

    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/{user_id}/"),
        json={
            "user": {
                "id": user_id,
                "role": {
                    "id": str(uuid.uuid4()),
                },
                "team": {
                    "id": str(uuid.uuid4()),
                },
            },
        },
    )

    url = reverse("users:user", kwargs={"pk": user_id})
    response = authorized_client.get(url)

    assert response.status_code == 200
    assertTemplateUsed("users/profile.html")


NON_SUPER_USER_ROLE_ID = str(uuid.uuid4())
NON_ADMIN_TEAM_ID = str(uuid.uuid4())


@pytest.mark.parametrize(
    "role_id, team_id, can_edit_team",
    (
        (SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, True),
        (NON_SUPER_USER_ROLE_ID, NON_ADMIN_TEAM_ID, False),
        (SUPER_USER_ROLE_ID, NON_ADMIN_TEAM_ID, True),
        (NON_SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, True),
        (SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, True),
    ),
)
def test_view_user_edit_team_permissions(
    authorized_client,
    requests_mock,
    mock_gov_user,
    role_id,
    team_id,
    can_edit_team,
):
    user_id = str(uuid.uuid4())

    mock_gov_user["user"] = {
        "id": user_id,
        "role": {
            "id": role_id,
            "permissions": {},
        },
        "team": {
            "id": team_id,
        },
    }
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/{user_id}/"),
        json={
            "user": {
                "id": user_id,
                "role": {
                    "id": role_id,
                },
                "team": {
                    "id": team_id,
                },
            },
        },
    )

    url = reverse("users:user", kwargs={"pk": user_id})
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    assert (soup.find("a", {"id": "link-edit-team"}) is not None) == can_edit_team


@pytest.mark.parametrize(
    "role_id, team_id, can_edit_team, team_payload",
    (
        (SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, True, {"team": "00000000-0000-0000-0000-000000000001"}),
        (NON_SUPER_USER_ROLE_ID, NON_ADMIN_TEAM_ID, False, {}),
        (SUPER_USER_ROLE_ID, NON_ADMIN_TEAM_ID, True, {"team": "00000000-0000-0000-0000-000000000001"}),
        (NON_SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, True, {"team": "00000000-0000-0000-0000-000000000001"}),
        (SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, True, {"team": "00000000-0000-0000-0000-000000000001"}),
    ),
)
def test_edit_user_edit_team_permissions(
    authorized_client,
    requests_mock,
    mock_gov_user,
    role_id,
    team_id,
    team_payload,
    can_edit_team,
    mock_roles,
    mock_queues_list,
):
    user_id = str(uuid.uuid4())

    mock_gov_user["user"] = {
        "id": user_id,
        "role": {
            "id": role_id,
            "permissions": {},
        },
        "team": {
            "id": team_id,
        },
    }
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/{user_id}/"),
        json={
            "user": {
                "id": user_id,
                "role": {
                    "id": role_id,
                },
                "team": {
                    "id": team_id,
                },
                "first_name": "Test",
                "last_name": "User",
            },
        },
    )

    url = reverse("users:edit", kwargs={"pk": user_id})
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    assert (soup.find("select", {"name": "team"}) is not None) == can_edit_team

    mock_put = requests_mock.put(client._build_absolute_uri(f"/gov-users/{user_id}/"), json={})
    response = authorized_client.post(
        url,
        data={
            "email": "test@example.com",  # /PS-IGNORE
            "team": "00000000-0000-0000-0000-000000000001",
            "default_queue": "00000000-0000-0000-0000-000000000001",
        },
    )
    assert mock_put.last_request.json() == {
        "email": "test@example.com",  # /PS-IGNORE
        "default_queue": "00000000-0000-0000-0000-000000000001",
        **team_payload,
    }


@pytest.mark.parametrize(
    "user_id, can_edit_role, role_payload",
    (
        (GOV_USER_ID, False, {}),
        (str(uuid.uuid4()), True, {"role": "00000000-0000-0000-0000-000000000001"}),
    ),
)
def test_edit_user_edit_role_permissions(
    authorized_client,
    requests_mock,
    mock_gov_user,
    user_id,
    can_edit_role,
    role_payload,
    mock_roles,
    mock_queues_list,
):
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/{user_id}/"),
        json={
            "user": {
                "id": user_id,
                "role": {
                    "id": str(uuid.uuid4()),
                },
                "team": {
                    "id": str(uuid.uuid4()),
                },
                "first_name": "Test",
                "last_name": "User",
                "gov_user_id": GOV_USER_ID,
            },
        },
    )

    url = reverse("users:edit", kwargs={"pk": user_id})
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    assert (soup.find("select", {"name": "role"}) is not None) == can_edit_role

    mock_put = requests_mock.put(
        client._build_absolute_uri(f"/gov-users/{user_id}/"),
        json={
            "gov_user": {
                "default_queue": str(uuid.uuid4()),
            },
        },
    )
    response = authorized_client.post(
        url,
        data={
            "email": "test@example.com",  # /PS-IGNORE
            "role": "00000000-0000-0000-0000-000000000001",
            "default_queue": "00000000-0000-0000-0000-000000000001",
        },
    )
    assert mock_put.last_request.json() == {
        "email": "test@example.com",  # /PS-IGNORE
        "default_queue": "00000000-0000-0000-0000-000000000001",
        **role_payload,
    }
