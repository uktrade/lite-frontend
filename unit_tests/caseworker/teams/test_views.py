import pytest
import uuid

from django.urls import reverse
from core import client
from caseworker.core.constants import ADMIN_TEAM_ID, SUPER_USER_ROLE_ID


pk = "67b9a4a3-6f3d-4511-8a19-23ccff221a74"
NON_SUPER_USER_ROLE_ID = str(uuid.uuid4())
NON_ADMIN_TEAM_ID = str(uuid.uuid4())


def test_teams_cannot_be_created_and_modified(authorized_client, reset_config_users_list):

    url = reverse("teams:teams")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["can_change_config"] == False


def test_teams_can_be_created_and_modified(authorized_client, specify_config_users_list):

    url = reverse("teams:teams")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["can_change_config"] == True


@pytest.mark.parametrize(
    "url",
    (
        (reverse("teams:add")),
        (reverse("teams:edit", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234"})),
    ),
)
def test_teams_add_view_returns_unauthorized_user_not_on_config_admin_list(
    authorized_client, reset_config_users_list, url
):

    response = authorized_client.get(url)
    assert response.status_code == 403
    assert response.context["title"] == "Sorry, unauthorized"
    assert response.context["description"] == "You don't have authorisation to view this page"


@pytest.mark.parametrize(
    "url",
    (
        (reverse("teams:add")),
        (reverse("teams:edit", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234"})),
    ),
)
def test_teams_add_view_returns_ok_user_on_config_admin_list(
    authorized_client, mock_team_get, specify_config_users_list, url
):

    response = authorized_client.get(url)
    assert response.status_code == 200


def test_edit_team_view(authorized_client, form_team_data, requests_mock, specify_config_users_list):
    mock_data = {
        "team": {
            "id": "67b9a4a3-6f3d-4511-8a19-23ccff221a74",
            "name": "FCDO",
            "part_of_ecju": True,
            "is_ogd": True,
            "alias": "FCO",
            "department": "3b637abd-283c-4e80-b87e-30c23b0edbec",
        }
    }
    url = reverse("teams:edit", kwargs={"pk": pk})

    requests_mock.get(f"/teams/{pk}/", status_code=200, json=mock_data)
    requests_mock.put(f"/teams/{pk}/", json=form_team_data)

    response = authorized_client.post(url, data=form_team_data)
    assert response.status_code == 302
    history = requests_mock.request_history.pop()
    assert history.method == "PUT"
    assert history.json() == {"is_ogd": True, "name": "Test", "part_of_ecju": True}


@pytest.mark.parametrize(
    "role_id, team_id, can_add_user",
    (
        (SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, True),
        (NON_SUPER_USER_ROLE_ID, NON_ADMIN_TEAM_ID, False),
        (SUPER_USER_ROLE_ID, NON_ADMIN_TEAM_ID, True),
        (NON_SUPER_USER_ROLE_ID, ADMIN_TEAM_ID, False),
    ),
)
def test_teams_view_add_user_permissions(
    authorized_client,
    requests_mock,
    mock_gov_user,
    role_id,
    team_id,
    can_add_user,
    beautiful_soup,
):

    user_id = str(uuid.uuid4())

    requests_mock.get(
        client._build_absolute_uri(f"/teams/{team_id}/"),
        json={"team": {"id": team_id}},
    )
    requests_mock.get(
        client._build_absolute_uri(f"/teams/{team_id}/users/"),
        json={"users": []},
    )

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
        "email": mock_gov_user["user"]["email"],
    }

    url = reverse("teams:team", kwargs={"pk": team_id})
    response = authorized_client.get(url)

    soup = beautiful_soup(response.content)
    assert (soup.find("a", {"id": "button-add-user"}) is not None) == can_add_user
