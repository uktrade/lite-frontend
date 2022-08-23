import pytest

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(
    mock_routing_rules,
    mock_queues_list,
    mock_users_team_queues_list,
    mock_routing_rule_get,
    mock_team_queues_get,
    mock_case_types_get,
    mock_countries,
    mock_users_by_team_get,
):
    yield


def test_routing_rules_cannot_be_created_and_modified(authorized_client, reset_config_users_list):

    url = reverse("routing_rules:list")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["can_change_config"] == False


def test_routing_rules_can_be_created_and_modified(authorized_client, specify_config_users_list):

    url = reverse("routing_rules:list")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["can_change_config"] == True


@pytest.mark.parametrize(
    "url",
    (
        (reverse("routing_rules:create")),
        (reverse("routing_rules:edit", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234"})),
        (
            reverse(
                "routing_rules:change_status", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234", "status": "Active"}
            )
        ),
    ),
)
def test_routing_rules_manage_view_returns_unauthorized_user_not_on_config_admin_list(
    authorized_client, reset_config_users_list, url
):

    response = authorized_client.get(url)
    assert response.status_code == 403
    assert response.context["title"] == "Sorry, unauthorized"
    assert response.context["description"] == "You don't have authorisation to view this page"


@pytest.mark.parametrize(
    "url",
    (
        (reverse("routing_rules:create")),
        (reverse("routing_rules:edit", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234"})),
        (
            reverse(
                "routing_rules:change_status",
                kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234", "status": "deactivate"},
            )
        ),
    ),
)
def test_routing_rules_manage_view_returns_ok_user_not_on_config_admin_list(
    authorized_client, specify_config_users_list, url
):

    response = authorized_client.get(url)
    assert response.status_code == 200
