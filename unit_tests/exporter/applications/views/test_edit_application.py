import pytest

from bs4 import BeautifulSoup
from django.urls import reverse

from exporter.core.constants import APPLICANT_EDITING
from exporter.applications.forms.common import EditApplicationForm


@pytest.mark.parametrize(
    "url_name, form_class",
    (("edit_type", EditApplicationForm),),
)
def test_edit_application_view_exists(
    application_id, mock_application_get, authorized_client, url_name, form_class, requests_mock
):
    url = reverse(f"applications:{url_name}", kwargs={"pk": application_id})
    response = authorized_client.get(url)
    assert response.status_code == 200

    form = response.context["form"]
    assert isinstance(form, form_class)


def test_edit_application_form_valid_major_edit(
    requests_mock,
    authorized_client,
    application_id,
    application_task_list_url,
    mock_application_status_post,
):
    url = reverse("applications:edit_type", kwargs={"pk": application_id})
    response = authorized_client.post(url, {})

    assert response.status_code == 302
    assert response.url == application_task_list_url

    history = requests_mock.request_history.pop()
    assert history.method == "POST"
    assert history.json() == {"status": APPLICANT_EDITING}


def test_edit_application_major_edit_change_status_fail(
    requests_mock,
    authorized_client,
    application_id,
    mock_application_status_post_failure,
):
    url = reverse("applications:edit_type", kwargs={"pk": application_id})
    response = authorized_client.post(url, {})

    assert response.status_code == 200

    response_body = BeautifulSoup(response.content, "html.parser")
    assert "Unexpected error changing application status to APPLICANT_EDITING" in response_body.text

    history = requests_mock.request_history.pop()
    assert history.method == "POST"
    assert history.json() == {"status": APPLICANT_EDITING}


def test_edit_application_form_valid_major_edit_by_copy(
    authorized_client,
    application_id,
    data_organisation,
    application_task_list_url,
    mock_application_status_post,
):
    url = reverse("applications:edit_type", kwargs={"pk": application_id})
    response = authorized_client.post(url, {})

    assert response.status_code == 302
    assert response.url == application_task_list_url
