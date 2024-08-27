import pytest
import uuid

from bs4 import BeautifulSoup
from django.urls import reverse

from core import client

amended_application_id = str(uuid.uuid4())


@pytest.fixture(autouse=True)
def setup(
    mock_application_get,
):
    yield


@pytest.fixture
def application_detail_url(application_id):
    return reverse("applications:application", kwargs={"pk": application_id})


@pytest.fixture
def application_major_edit_cancel_url(application_id):
    return reverse("applications:edit_type", kwargs={"pk": application_id})


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


def test_edit_button_points_to_amend_by_copy(
    authorized_client,
    data_organisation,
    application_detail_url,
    application_major_edit_confirm_url,
    mock_status_properties,
):
    mock_status_properties["can_invoke_major_editable"] = True

    response = authorized_client.get(application_detail_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    edit_button = soup.find("a", {"id": "button-edit-application"})
    assert edit_button and edit_button["href"] == application_major_edit_confirm_url


def test_edit_button_presents_amend_by_copy(
    authorized_client,
    data_standard_case,
    data_organisation,
    application_detail_url,
    application_major_edit_confirm_url,
):

    response = authorized_client.get(application_major_edit_confirm_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")

    assert data_standard_case["case"]["data"]["name"] in response.content.decode("utf-8")

    submit_button = soup.find("input", {"id": "submit-id-submit"})
    assert submit_button and "Continue" in str(submit_button)

    cancel_url = soup.find("a", {"id": "cancel-id-cancel"})
    assert cancel_url and cancel_url["href"] == application_detail_url


def test_major_edit_cancel_from_whitelisted_exporter_goes_to_application_detail(
    authorized_client,
    data_organisation,
    application_major_edit_confirm_url,
    application_detail_url,
):
    response = authorized_client.get(application_major_edit_confirm_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    cancel_url = soup.find("a", {"id": "cancel-id-cancel"})
    assert cancel_url and cancel_url["href"] == application_detail_url


def test_major_edit_confirmation_from_whitelisted_exporter_goes_to_task_list(
    authorized_client,
    data_organisation,
    application_major_edit_confirm_url,
    amended_application_task_list_url,
    mock_application_amendment_post,
):
    response = authorized_client.post(application_major_edit_confirm_url)
    assert response.status_code == 302
    assert response.url == amended_application_task_list_url


def test_organisation_creates_amendment_by_copy(
    authorized_client,
    requests_mock,
    data_organisation,
    mock_application_amendment_post,
    application_major_edit_confirm_url,
    application_amendment_create_url,
    amended_application_task_list_url,
):
    response = authorized_client.post(application_major_edit_confirm_url)
    assert response.status_code == 302
    assert response.url == amended_application_task_list_url
    history = requests_mock.request_history.pop()
    assert history.method == "POST"
    assert history.url == application_amendment_create_url


def test_organisation_creates_amendment_by_copy_bad_response(
    settings,
    requests_mock,
    authorized_client,
    data_organisation,
    application_major_edit_confirm_url,
    application_amendment_create_url,
    mock_application_amendment_post_failure,
):
    response = authorized_client.post(application_major_edit_confirm_url)
    assert response.status_code == 200

    response_body = BeautifulSoup(response.content, "html.parser")
    assert "Unexpected error creating amendment" in response_body.text

    history = requests_mock.request_history.pop()
    assert history.method == "POST"
    assert history.url == application_amendment_create_url
