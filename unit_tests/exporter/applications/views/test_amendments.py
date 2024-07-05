import pytest
import uuid

from bs4 import BeautifulSoup
from django.conf import settings
from django.urls import reverse

from core import client
from exporter.applications.forms.common import EditApplicationForm

amended_application_id = str(uuid.uuid4())


@pytest.fixture
def application_major_edit_cancel_url(application_id):
    return reverse("applications:edit_type", kwargs={"pk": application_id})


@pytest.fixture
def application_amendment_create_url(application_id):
    return client._build_absolute_uri(f"/applications/{application_id}/amendment/")


@pytest.fixture
def amended_application_task_list_url():
    return reverse("applications:task_list", kwargs={"pk": amended_application_id})


@pytest.fixture
def mock_application_amendment_post(requests_mock, application_id):
    url = client._build_absolute_uri(f"/applications/{application_id}/amendment/")
    return requests_mock.post(url, json={"id": amended_application_id}, status_code=201)


@pytest.fixture
def mock_application_amendment_post_failure(requests_mock, application_id):
    url = client._build_absolute_uri(f"/applications/{application_id}/amendment/")
    return requests_mock.post(url, json={"error": "not allowed"}, status_code=500)


def test_major_edit_redirects_to_confirm_page_for_whitelisted_organisation(
    authorized_client,
    data_organisation,
    application_edit_type_url,
    application_major_edit_confirm_url,
):
    settings.FEATURE_AMENDMENT_BY_COPY_EXPORTER_IDS = [data_organisation["id"]]
    response = authorized_client.post(application_edit_type_url, {"edit_type": "major"})
    assert response.status_code == 302
    assert response.url == application_major_edit_confirm_url


def test_major_edit_cancel_redirects_to_edit_type_page(
    authorized_client,
    mock_application_get,
    application_major_edit_cancel_url,
):
    response = authorized_client.get(application_major_edit_cancel_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], EditApplicationForm)


def test_major_edit_confirmation_from_whitelisted_exporter_goes_to_task_list(
    authorized_client,
    data_organisation,
    application_major_edit_confirm_url,
    amended_application_task_list_url,
    mock_application_get,
    mock_application_amendment_post,
):
    settings.FEATURE_AMENDMENT_BY_COPY_EXPORTER_IDS = [data_organisation["id"]]
    response = authorized_client.post(application_major_edit_confirm_url)
    assert response.status_code == 302
    assert response.url == amended_application_task_list_url


def test_whitelisted_organisation_creates_amendment_by_copy(
    authorized_client,
    requests_mock,
    data_organisation,
    mock_application_get,
    mock_application_amendment_post,
    application_major_edit_confirm_url,
    application_amendment_create_url,
    amended_application_task_list_url,
):
    settings.FEATURE_AMENDMENT_BY_COPY_EXPORTER_IDS = [data_organisation["id"]]
    response = authorized_client.post(application_major_edit_confirm_url)
    assert response.status_code == 302
    assert response.url == amended_application_task_list_url
    history = requests_mock.request_history[-2]
    assert history.method == "POST"
    assert history.url == application_amendment_create_url


def test_whitelisted_organisation_creates_amendment_by_copy_bad_response(
    settings,
    requests_mock,
    authorized_client,
    data_organisation,
    application_major_edit_confirm_url,
    application_amendment_create_url,
    mock_application_get,
    mock_application_amendment_post_failure,
):
    settings.FEATURE_AMENDMENT_BY_COPY_EXPORTER_IDS = [data_organisation["id"]]
    response = authorized_client.post(application_major_edit_confirm_url)
    assert response.status_code == 200

    response_body = BeautifulSoup(response.content, "html.parser")
    assert "Unexpected error creating amendment" in response_body.text

    history = requests_mock.request_history.pop()
    assert history.method == "POST"
    assert history.url == application_amendment_create_url
