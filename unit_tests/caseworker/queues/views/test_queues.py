import pytest

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(
    authorized_client,
    mock_queue,
    mock_queues_list,
):
    yield


def test_queues_cannot_be_created_and_modified(authorized_client, reset_config_users_list):
    url = reverse("queues:manage")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["can_change_config"] == False


def test_queues_can_be_created_and_modified(authorized_client, specify_config_users_list):
    url = reverse("queues:manage")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["can_change_config"] == True


@pytest.mark.parametrize(
    "url",
    (
        (reverse("queues:add")),
        (reverse("queues:edit", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234"})),
    ),
)
def test_queues_add_view_returns_unauthorized_user_not_on_config_admin_list(
    authorized_client, reset_config_users_list, url
):
    response = authorized_client.get(url)
    assert response.status_code == 403
    assert response.context["title"] == "Sorry, unauthorized"
    assert response.context["description"] == "You don't have authorisation to view this page"


@pytest.mark.parametrize(
    "url",
    (
        (reverse("queues:add")),
        (reverse("queues:edit", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234"})),
    ),
)
def test_queues_add_view_returns_ok_user_on_config_admin_list(authorized_client, specify_config_users_list, url):
    response = authorized_client.get(url)
    assert response.status_code == 200
