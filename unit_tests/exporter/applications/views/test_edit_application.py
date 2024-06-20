from bs4 import BeautifulSoup
import uuid
import pytest


from django.urls import reverse
from core import client

from exporter.applications.forms.common import EditApplicationForm
from exporter.core.constants import APPLICANT_EDITING


@pytest.mark.parametrize(
    "url_name, form_class",
    (("edit_type", EditApplicationForm),),
)
def test_edit_application_view_exists(
    data_standard_case, mock_application_get, authorized_client, url_name, form_class, requests_mock
):
    application_id = data_standard_case["case"]["data"]["id"]

    url = reverse(f"applications:{url_name}", kwargs={"pk": application_id})
    response = authorized_client.get(url)
    assert response.status_code == 200

    form = response.context["form"]
    assert isinstance(form, form_class)


def test_edit_application_form_valid_major_edit(requests_mock, authorized_client, data_standard_case):
    application_id = data_standard_case["case"]["data"]["id"]
    url = reverse("applications:edit_type", kwargs={"pk": application_id})

    status_url = f"/applications/{application_id}/status/"
    requests_mock.put(status_url, json={}, status_code=200)
    form_data = {"edit_type": "major"}
    response = authorized_client.post(url, form_data)

    assert response.status_code == 302
    assert response.url == reverse("applications:task_list", kwargs={"pk": application_id})

    assert requests_mock.last_request.json() == {"status": "applicant_editing"}


def test_edit_application_form_valid_major_edit_by_copy(
    settings,
    requests_mock,
    authorized_client,
    data_standard_case,
    data_organisation,
):
    settings.FEATURE_AMENDMENT_BY_COPY_EXPORTER_IDS = [data_organisation["id"]]
    application_id = data_standard_case["case"]["data"]["id"]
    url = reverse("applications:edit_type", kwargs={"pk": application_id})

    amendment_url = f"/applications/{application_id}/amendment/"
    synthetic_amendment_id = str(uuid.uuid4())
    requests_mock.post(amendment_url, json={"id": synthetic_amendment_id}, status_code=201)
    response = authorized_client.post(url, {"edit_type": "major"})

    assert response.status_code == 302
    assert response.url == reverse("applications:task_list", kwargs={"pk": synthetic_amendment_id})
    assert requests_mock.last_request.json() == {}


def test_edit_application_form_valid_major_edit_by_copy_bad_api_response(
    settings,
    requests_mock,
    authorized_client,
    data_standard_case,
    data_organisation,
):
    settings.FEATURE_AMENDMENT_BY_COPY_EXPORTER_IDS = [data_organisation["id"]]
    application_id = data_standard_case["case"]["data"]["id"]
    url = reverse("applications:edit_type", kwargs={"pk": application_id})

    amendment_url = f"/applications/{application_id}/amendment/"
    synthetic_amendment_id = str(uuid.uuid4())
    requests_mock.post(amendment_url, json={"error": "some whoops"}, status_code=500)
    response = authorized_client.post(url, {"edit_type": "major"})
    response_body = BeautifulSoup(response.content, "html.parser")

    assert response.status_code == 200
    assert "An error occurred" in response_body.text
