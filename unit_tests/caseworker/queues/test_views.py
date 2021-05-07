import pytest

from django.urls import reverse

import os

from core import client


queue_pk = "59ef49f4-cf0c-4085-87b1-9ac6817b4ba6"


@pytest.fixture(autouse=True)
def setup(mock_cases_search, authorized_client, queue_pk, mock_queue, mock_countries):
    yield


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

    file_path = os.path.join(settings.BASE_DIR, "caseworker/queues/example.xml")
    data = {"file": open(file_path, "rb")}

    response = authorized_client.post(url, data, format="multipart")

    assert response.status_code == 302

    with open(file_path, "r") as f:
        assert mock_enforcement_xml_upload.last_request.json() == {"file": f.read()}


def test_upload_enforcement_xml_invalid_file(authorized_client, mock_enforcement_xml_validation_error, settings):
    url = reverse("queues:enforcement_xml_import", kwargs={"pk": queue_pk})

    file_path = os.path.join(settings.BASE_DIR, "caseworker/queues/example.xml")
    data = {"file": open(file_path, "rb")}

    response = authorized_client.post(url, data, format="multipart")

    assert response.status_code == 200
    assert response.context_data["form"].errors == {"file": ["Invalid XML format received"]}
