import pytest

from django.urls import reverse
from django.test.utils import override_settings


@pytest.fixture
def application_pk(data_standard_case):
    return data_standard_case["case"]["data"]["id"]


@pytest.fixture
def application_end_use_summary_url(application_pk):
    return reverse(
        "applications:end_use_details",
        kwargs={
            "pk": application_pk,
        },
    )


@pytest.fixture
def application_task_list_url(application_pk):
    return reverse("applications:task_list", kwargs={"pk": application_pk})


def test_application_end_use_summary(
    authorized_client, mock_application_get, application_end_use_summary_url, application_task_list_url
):
    response = authorized_client.get(application_end_use_summary_url)
    assert response.context["back_url"] == application_task_list_url + "#end_use_details"
    assert response.context["back_link_text"] == "Back to application overview"
    assert (
        response.context["instruction_text"]
        == "Review your answers below and make any amends you need to. Click 'Save and continue' to save your progress."
    )


@override_settings(ALLOWED_HOSTS=None)
def test_application_end_use_summary_has_url_has_allowed_host_and_scheme_fail(
    authorized_client, mock_application_get, application_end_use_summary_url, application_task_list_url
):
    response = authorized_client.post(application_end_use_summary_url, data={})
    assert response.status_code == 403


@override_settings(ALLOWED_HOSTS="*")
def test_application_end_use_summary_has_url_has_allowed_host_and_scheme_success(
    authorized_client, mock_application_get, application_end_use_summary_url, application_task_list_url
):
    response = authorized_client.post(application_end_use_summary_url, data={})
    assert response.status_code == 200


# @override_settings(DEBUG=True)
# def test_application_end_use_summary_post(
#     authorized_client, mock_application_get, application_end_use_summary_url, application_task_list_url
# ):
#     response = authorized_client.post(application_end_use_summary_url, data={})
#     assert response.status_code == 200  # Assuming the form is invalid and re-renders the page
#     assert response.context["back_url"] == application_task_list_url + "#end_use_details"
#     assert response.context["back_link_text"] == "Back to application overview"
#     assert (
#         response.context["instruction_text"]
#         == "Review your answers below and make any amends you need to. Click 'Save and continue' to save your progress."
#     )
