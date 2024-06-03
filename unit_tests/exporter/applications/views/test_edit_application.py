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
