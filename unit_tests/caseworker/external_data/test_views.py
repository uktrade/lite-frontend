import os

import pytest

from django.urls import reverse

from core import client


@pytest.fixture
def mock_denial_upload(requests_mock):
    url = client._build_absolute_uri("/external-data/denial/")
    yield requests_mock.post(url=url)


@pytest.fixture
def mock_denial_upload_validation_error(requests_mock):
    url = client._build_absolute_uri("/external-data/denial/")
    data = {"errors": {"csv_file": ['Error: [Row 2] {"denied_name": ["This field may not be blank."]}']}}
    yield requests_mock.post(url=url, status_code=400, json=data)


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
