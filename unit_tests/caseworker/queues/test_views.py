import pytest

from bs4 import BeautifulSoup

from django.conf import settings
from django.urls import reverse

import os

from core import client

queue_pk = "59ef49f4-cf0c-4085-87b1-9ac6817b4ba6"


@pytest.fixture(autouse=True)
def setup(
    mock_cases_search,
    authorized_client,
    queue_pk,
    mock_queue,
    mock_countries,
    mock_queues_list,
    mock_control_list_entries,
    mock_regime_entries,
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


@pytest.mark.parametrize(
    "url",
    [
        reverse("core:index"),
        reverse("queues:cases"),
        reverse("queues:cases", kwargs={"queue_pk": "00000000-0000-0000-0000-000000000001"}),
    ],
)
def test_cases_view(url, authorized_client):
    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.fixture
def mock_enforcement_xml_upload(requests_mock):
    url = client._build_absolute_uri(f"/cases/enforcement-check/{queue_pk}/")
    yield requests_mock.post(url=url)


@pytest.fixture
def mock_enforcement_xml_validation_error(requests_mock):
    url = client._build_absolute_uri(f"/cases/enforcement-check/{queue_pk}/")
    data = {"errors": {"file": ["Invalid XML format received"]}}
    yield requests_mock.post(url=url, status_code=400, json=data)


def test_upload_enforcement_xml_valid_file(authorized_client, mock_enforcement_xml_upload, settings):
    url = reverse("queues:enforcement_xml_import", kwargs={"pk": queue_pk})

    file_path = os.path.join(settings.BASE_DIR, "unit_tests/caseworker/queues/example.xml")
    data = {"file": open(file_path, "rb")}

    response = authorized_client.post(url, data, format="multipart")

    assert response.status_code == 302

    with open(file_path, "r") as f:
        assert mock_enforcement_xml_upload.last_request.json() == {"file": f.read()}


def test_upload_enforcement_xml_invalid_file(authorized_client, mock_enforcement_xml_validation_error, settings):
    url = reverse("queues:enforcement_xml_import", kwargs={"pk": queue_pk})

    file_path = os.path.join(settings.BASE_DIR, "unit_tests/caseworker/queues/example.xml")
    data = {"file": open(file_path, "rb")}

    response = authorized_client.post(url, data, format="multipart")

    assert response.status_code == 200
    assert response.context_data["form"].errors == {"file": ["Invalid XML format received"]}


def test_cases_home_page_view_context(authorized_client):
    context_keys = [
        "sla_radius",
        "sla_circumference",
        "data",
        "queue",
        "filters",
        "is_all_cases_queue",
        "enforcement_check",
        "updated_cases_banner_queue_id",
    ]
    response = authorized_client.get(reverse("queues:cases"))
    assert len(response.context["filters"].filters) == 6
    assert len(response.context["filters"].advanced_filters) == 22
    for context_key in context_keys:
        assert response.context[context_key]
    assert response.status_code == 200


def test_cases_home_page_nca_applicable_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?is_nca_applicable=True"
    authorized_client.get(url)
    assert mock_cases_search.last_request.qs == {
        "queue_id": ["00000000-0000-0000-0000-000000000001"],
        "page": ["1"],
        "is_nca_applicable": ["true"],
    }


def test_cases_home_page_trigger_list_search(authorized_client, mock_cases_search):
    url = reverse("queues:cases") + "?is_trigger_list=True"
    authorized_client.get(url)
    assert mock_cases_search.last_request.qs == {
        "queue_id": ["00000000-0000-0000-0000-000000000001"],
        "page": ["1"],
        "is_trigger_list": ["true"],
    }


def test_trigger_list_checkbox_visible_unchecked(authorized_client):
    response = authorized_client.get(reverse("core:index"))
    html = BeautifulSoup(response.content, "html.parser")
    checkbox = html.find(id="is-trigger-list")
    assert "checked" not in checkbox.attrs


def test_trigger_list_checkbox_visible_checked(authorized_client):
    response = authorized_client.get(reverse("core:index") + "/?is_trigger_list=True")
    html = BeautifulSoup(response.content, "html.parser")
    checkbox = html.find(id="is-trigger-list")
    assert "checked" in checkbox.attrs
