import os

import pytest

from django.urls import reverse

from core import client


denial_pk = "0a7dd9e1-f469-4dba-bff0-26f3786361fd"


@pytest.fixture
def mock_denial_upload(requests_mock):
    url = client._build_absolute_uri("/external-data/denial/")
    yield requests_mock.post(url=url)


@pytest.fixture
def mock_denial_upload_validation_error(requests_mock):
    url = client._build_absolute_uri("/external-data/denial/")
    data = {"errors": {"csv_file": ['Error: [Row 2] {"denied_name": ["This field may not be blank."]}']}}
    yield requests_mock.post(url=url, status_code=400, json=data)


@pytest.fixture
def mock_denial_detail(requests_mock):
    url = client._build_absolute_uri(f"/external-data/denial/{denial_pk}/")
    yield requests_mock.post(url=url, json={})


@pytest.fixture
def mock_denial_retrieve(requests_mock):
    url = client._build_absolute_uri(f"/external-data/denial/{denial_pk}/")
    yield requests_mock.get(url=url, json={"id": denial_pk})


@pytest.fixture
def mock_denial_patch(requests_mock):
    url = client._build_absolute_uri(f"/external-data/denial/{denial_pk}/")
    yield requests_mock.patch(url=url, json={})


def test_upload_denial_valid_file(authorized_client, mock_denial_upload, settings):
    # given the case has activity from system user
    url = reverse("external_data:denials-upload")

    file_path = os.path.join(settings.BASE_DIR, "caseworker/external_data/example.csv")
    data = {"csv_file": open(file_path, "rb")}

    # when the case is viewed
    response = authorized_client.post(url, data, format="multipart")

    # then it does not error
    assert response.status_code == 302
    # and the upstream endpoint was posted
    with open(file_path, "r") as f:
        assert mock_denial_upload.last_request.json() == {"csv_file": f.read()}


def test_upload_denial_invalid_file(authorized_client, mock_denial_upload_validation_error, settings):
    # given the case has activity from system user
    url = reverse("external_data:denials-upload")

    file_path = os.path.join(settings.BASE_DIR, "caseworker/external_data/example.csv")
    data = {"csv_file": open(file_path, "rb")}

    # when the case is viewed
    response = authorized_client.post(url, data, format="multipart")

    # then it errors
    assert response.status_code == 200
    assert response.context_data["form"].errors == {
        "csv_file": ['Error: [Row 2] {"denied_name": ["This field may not be blank."]}']
    }


def test_denial_detail(authorized_client, mock_denial_retrieve):
    url = reverse("external_data:denial-detail", kwargs={"pk": denial_pk})

    # when the denial detail is verified
    response = authorized_client.get(url)

    # then the denial is added to the context
    assert response.status_code == 200
    assert response.context_data["denial"] == {"id": denial_pk}


def test_denial_revoke_view(authorized_client, mock_denial_retrieve, requests_mock):
    url = reverse("external_data:denial-revoke", kwargs={"pk": denial_pk})

    # when the denial revoke form is viewed
    response = authorized_client.get(url)

    # then the denial is exposed to the template
    assert response.status_code == 200
    assert response.context_data["denial"] == {"id": denial_pk}


def test_denial_revoke_submit(authorized_client, mock_denial_detail, mock_denial_patch, requests_mock):
    url = reverse("external_data:denial-revoke", kwargs={"pk": denial_pk})

    # when the denial revoke form is submitted
    response = authorized_client.post(url, {"comment": "abc"})

    # then the denial is revoked
    assert requests_mock.request_history[3].json() == {"is_revoked": True, "is_revoked_comment": "abc"}

    # and the user is redirected back to denial detail
    assert response.status_code == 302
    assert response.url == reverse("external_data:denial-detail", kwargs={"pk": denial_pk})
