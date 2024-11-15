import pytest
import uuid
from bs4 import BeautifulSoup
from unittest.mock import patch

from pytest_django.asserts import assertTemplateUsed
from django.urls import reverse
from requests.exceptions import HTTPError
from django.contrib.messages import constants, get_messages

from core import client
from core.exceptions import ServiceError
from caseworker.users.manage.forms import EditCaseworkerUser
from caseworker.core.constants import (
    ADMIN_TEAM_ID,
    ALL_CASES_QUEUE_ID,
    SUPER_USER_ROLE_ID,
)


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


@pytest.fixture()
def edit_user_data():
    user_id = str(uuid.uuid4())
    return {
        "user": {
            "id": user_id,
            "role": {
                "id": "00000000-0000-0000-0000-000000000002",
            },
            "team": {
                "id": "00000000-0000-0000-0000-000000000001",
            },
            "default_queue": {"id": ALL_CASES_QUEUE_ID},
            "email": "test@guygydu.com",
        },
    }


@pytest.fixture()
def user_static_data():
    roles = [{"id": "00000000-0000-0000-0000-000000000002", "name": "Super User"}]
    teams = [
        {"id": "00000000-0000-0000-0000-000000000001", "name": "Admin"},
        {"id": "7d60e199-c64c-4863-bdd6-ac441f4fe806", "name": "Example team"},
    ]
    queues = [
        {"id": ALL_CASES_QUEUE_ID, "name": "Queue A", "team": {"id": "00000000-0000-0000-0000-000000000001"}},
        {
            "id": ALL_CASES_QUEUE_ID.replace("1", "2"),
            "name": "Queue B",
            "team": {"id": "00000000-0000-0000-0000-000000000001"},
        },
        {"id": ALL_CASES_QUEUE_ID.replace("1", "3"), "name": "Queue C", "team": None},
    ]
    return {"roles": roles, "teams": teams, "queues": queues}


@pytest.fixture
def mock_get_queues(requests_mock, user_static_data):
    url = client._build_absolute_uri(f"/queues/")
    yield requests_mock.get(url=url, json=user_static_data["queues"])


@pytest.fixture()
def edit_user_mock(edit_user_data, requests_mock):
    user_id = edit_user_data["user"]["id"]
    yield requests_mock.get(client._build_absolute_uri(f"/gov-users/{user_id}/"), json=edit_user_data)


@pytest.fixture
def edit_user_url(edit_user_data):
    user_id = edit_user_data["user"]["id"]
    return reverse("users:edit", kwargs={"pk": user_id})


@pytest.fixture
def mock_edit_users_failure(requests_mock, edit_user_data):
    url = client._build_absolute_uri(f"/caseworker/organisations/{organisation_pk}/exporter-users/")
    yield requests_mock.post(url=url, json={}, status_code=500)


@pytest.fixture
def edit_user_post_data(edit_user_data, user_static_data):
    return {
        "email": edit_user_data["user"]["email"],
        "role": user_static_data["roles"][0]["id"],
        "default_queue": user_static_data["queues"][0]["id"],
        "team": user_static_data["teams"][0]["id"],
    }


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
    "role_id, team_id, can_edit_user",
    (
        (SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, True),
        (NON_SUPER_USER_ROLE_ID, NON_ADMIN_TEAM_ID, False),
        (SUPER_USER_ROLE_ID, NON_ADMIN_TEAM_ID, True),
        (NON_SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, False),
    ),
)
def test_view_user_edit_team_permissions(
    authorized_client,
    requests_mock,
    mock_gov_user,
    role_id,
    team_id,
    can_edit_user,
):
    user_id = str(uuid.uuid4())

    mock_gov_user["user"] = {
        "id": user_id,
        "role": {
            "id": role_id,
            "permissions": {},
            "name": "Test Role",
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
    assert (soup.find("a", {"id": "link-edit-team"}) is not None) == can_edit_user
    assert (soup.find("a", {"id": "link-edit-role"}) is not None) == can_edit_user
    assert (soup.find("a", {"id": "link-edit-email"}) is not None) == can_edit_user


@pytest.mark.parametrize(
    "role_id, team_id, edit_user_id ,can_deactivate",
    (
        (SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, "2a43805b-c082-47e7-9188-c8b3e1a83cb0", False),
        (SUPER_USER_ROLE_ID, NON_ADMIN_TEAM_ID, "2a43805b-c082-47e7-9188-c8b3e1a83cb0", False),
        (NON_SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, "2a43805b-c082-47e7-9188-c8b3e1a83cb0", False),
        (SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, "4a43805b-c082-47e7-9188-c8b3e1a83cb1", True),
        (NON_SUPER_USER_ROLE_ID, NON_ADMIN_TEAM_ID, "4a43805b-c082-47e7-9188-c8b3e1a83cb1", False),
        (SUPER_USER_ROLE_ID, NON_ADMIN_TEAM_ID, "4a43805b-c082-47e7-9188-c8b3e1a83cb1", True),
        (NON_SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, "4a43805b-c082-47e7-9188-c8b3e1a83cb1", False),
        (SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, "4a43805b-c082-47e7-9188-c8b3e1a83cb1", True),
    ),
)
def test_view_user_deactivate_permissions(
    authorized_client,
    requests_mock,
    mock_gov_user,
    role_id,
    team_id,
    edit_user_id,
    can_deactivate,
):

    gov_user_id = mock_gov_user["user"]["id"]

    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/{gov_user_id}/"),
        json={
            "user": {
                "id": gov_user_id,
                "role": {
                    "id": role_id,
                },
                "team": {
                    "id": team_id,
                },
            },
        },
    )
    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/{edit_user_id}/"),
        json={
            "user": {
                "id": edit_user_id,
                "role": {
                    "id": role_id,
                },
                "team": {
                    "id": team_id,
                },
                "status": "Active",
            },
        },
    )

    url = reverse("users:user", kwargs={"pk": edit_user_id})
    response = authorized_client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    assert (soup.find("a", {"id": "button-deactivate-user"}) is not None) == can_deactivate


@pytest.mark.parametrize(
    "role_id, disabled_attribute",
    (
        (SUPER_USER_ROLE_ID, False),
        (NON_SUPER_USER_ROLE_ID, True),
    ),
)
def test_edit_user_get(
    authorized_client,
    edit_user_url,
    mock_gov_user,
    mock_roles,
    mock_get_queues,
    edit_user_mock,
    edit_user_data,
    user_static_data,
    beautiful_soup,
    requests_mock,
    role_id,
    disabled_attribute,
):

    gov_user_id = mock_gov_user["user"]["id"]

    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/{gov_user_id}/"),
        json={
            "user": {
                "id": gov_user_id,
                "role": {
                    "id": role_id,
                },
                "team": {
                    "id": NON_ADMIN_TEAM_ID,
                },
            },
        },
    )

    response = authorized_client.get(edit_user_url)

    assert isinstance(response.context["form"], EditCaseworkerUser)
    assert response.context["form"].initial == {
        "email": edit_user_data["user"]["email"],
        "team": edit_user_data["user"]["team"]["id"],
        "role": edit_user_data["user"]["role"]["id"],
        "default_queue": edit_user_data["user"]["default_queue"]["id"],
    }

    soup = beautiful_soup(response.content)

    teams_select = soup.find(id="team").find_all("option")

    assert soup.find(id="role").has_attr("disabled") == disabled_attribute

    for i, sel in enumerate(teams_select):
        assert sel["value"] == user_static_data["teams"][i]["id"]
        assert sel.text == user_static_data["teams"][i]["name"]

    roles_select = soup.find(id="role").find_all("option")
    for i, sel in enumerate(roles_select):
        assert sel["value"] == user_static_data["roles"][i]["id"]
        assert sel.text == user_static_data["roles"][i]["name"]

    except_default_queue_select = [
        {"value": "", "name": "Select", "data-attribute": None},
        {"value": ALL_CASES_QUEUE_ID, "name": "Queue A", "data-attribute": "00000000-0000-0000-0000-000000000001"},
        {
            "value": ALL_CASES_QUEUE_ID.replace("1", "2"),
            "name": "Queue B",
            "data-attribute": "00000000-0000-0000-0000-000000000001",
        },
        {"value": ALL_CASES_QUEUE_ID.replace("1", "3"), "name": "Queue C", "data-attribute": "None"},
    ]

    default_queue_select = soup.find(id="default_queue").find_all("option")
    for i, sel in enumerate(default_queue_select):
        assert sel["value"] == except_default_queue_select[i]["value"]
        assert sel.get("data-attribute", None) == except_default_queue_select[i]["data-attribute"]
        assert sel.text == except_default_queue_select[i]["name"]


@pytest.mark.parametrize(
    "role_id, update_payload",
    (
        [NON_SUPER_USER_ROLE_ID, {"default_queue": ALL_CASES_QUEUE_ID}],
        [
            SUPER_USER_ROLE_ID,
            {
                "email": "test@guygydu.com",
                "role": "00000000-0000-0000-0000-000000000002",
                "team": "00000000-0000-0000-0000-000000000001",
                "default_queue": ALL_CASES_QUEUE_ID,
            },
        ],
    ),
)
def test_edit_user_post(
    authorized_client,
    edit_user_post_data,
    edit_user_url,
    mock_gov_user,
    mock_roles,
    mock_get_queues,
    edit_user_mock,
    edit_user_data,
    requests_mock,
    role_id,
    update_payload,
):

    gov_user_id = mock_gov_user["user"]["id"]
    edit_user_id = edit_user_data["user"]["id"]

    requests_mock.get(
        client._build_absolute_uri(f"/gov-users/{gov_user_id}/"),
        json={
            "user": {
                "id": gov_user_id,
                "role": {
                    "id": role_id,
                },
                "team": {
                    "id": NON_ADMIN_TEAM_ID,
                },
            },
        },
    )

    mock_put = requests_mock.put(
        client._build_absolute_uri(f"/caseworker/gov_users/{edit_user_id}/update/"),
        json={"gov_user": edit_user_post_data},
    )

    response = authorized_client.post(edit_user_url, data=edit_user_post_data)
    assert response.status_code == 302
    assert response.url == f"/users/{edit_user_id}/"

    assert [(m.level, m.message) for m in get_messages(response.wsgi_request)] == [
        (constants.SUCCESS, "User updated successfully")
    ]

    assert mock_put.last_request.json() == update_payload


def test_edit_user_post_email_exists(
    authorized_client,
    edit_user_url,
    mock_gov_user,
    mock_roles,
    mock_get_queues,
    edit_user_mock,
    user_static_data,
    requests_mock,
):

    requests_mock.get(
        client._build_absolute_uri("/caseworker/gov_users/gov_users_list/?email=changed@changeemaild.com"),
        json={"count": 1},
    )

    data = {
        "email": "changed@changeemaild.com",  # /PS-IGNORE
        "role": user_static_data["roles"][0]["id"],
        "default_queue": user_static_data["queues"][0]["id"],
        "team": user_static_data["teams"][0]["id"],
    }

    response = authorized_client.post(edit_user_url, data=data)
    assert response.status_code == 200

    assert response.context["form"].errors == {"email": ["This email has already been registered"]}


@pytest.mark.parametrize(
    "existing_queue_id, new_queue_id, expected_queue_id, edit_user_id",
    (
        [ALL_CASES_QUEUE_ID, ALL_CASES_QUEUE_ID, ALL_CASES_QUEUE_ID, "00000000-0000-0000-0000-000000000001"],
        [
            ALL_CASES_QUEUE_ID,
            ALL_CASES_QUEUE_ID.replace("1", "2"),
            ALL_CASES_QUEUE_ID,
            "00000000-0000-0000-0000-000000000001",
        ],
        [ALL_CASES_QUEUE_ID, ALL_CASES_QUEUE_ID, ALL_CASES_QUEUE_ID, "2a43805b-c082-47e7-9188-c8b3e1a83cb0"],
        [
            ALL_CASES_QUEUE_ID,
            ALL_CASES_QUEUE_ID.replace("1", "2"),
            ALL_CASES_QUEUE_ID.replace("1", "2"),
            "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
        ],
    ),
)
def test_edit_user_post_default_queue_change(
    authorized_client,
    edit_user_post_data,
    mock_gov_user,
    mock_roles,
    mock_get_queues,
    edit_user_data,
    requests_mock,
    existing_queue_id,
    expected_queue_id,
    new_queue_id,
    edit_user_id,
):

    session = authorized_client.session
    session["default_queue"] = existing_queue_id
    session.save()

    requests_mock.get(client._build_absolute_uri(f"/gov-users/{edit_user_id}/"), json=edit_user_data)
    requests_mock.put(
        client._build_absolute_uri(f"/caseworker/gov_users/{edit_user_id}/update/"),
        json={},
    )

    url = reverse("users:edit", kwargs={"pk": edit_user_id})
    edit_user_post_data["default_queue"] = new_queue_id

    response = authorized_client.post(url, data=edit_user_post_data)
    session = authorized_client.session

    assert response.status_code == 302
    assert session["default_queue"] == expected_queue_id


@patch("caseworker.users.manage.views.get_gov_user")
def test_edit_caseworker_404_on_get_user_error(
    mock_get_gov_user,
    authorized_client,
    edit_user_url,
):
    mock_get_gov_user.side_effect = HTTPError()
    response = authorized_client.get(edit_user_url)
    assert response.status_code == 404


def test_edit_user_api_failed(
    authorized_client,
    mock_gov_user,
    edit_user_mock,
    mock_roles,
    mock_get_queues,
    edit_user_url,
    edit_user_post_data,
    requests_mock,
    edit_user_data,
):

    edit_user_id = edit_user_data["user"]["id"]
    requests_mock.put(
        client._build_absolute_uri(f"/caseworker/gov_users/{edit_user_id}/update/"),
        json={},
        status_code=500,
    )

    with pytest.raises(ServiceError) as ex:
        authorized_client.post(edit_user_url, data=edit_user_post_data)

    assert ex.value.status_code == 500
    assert ex.value.user_message == "Unexpected error editing user"
