import pytest

from django.urls import reverse


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


def test_application_end_use_summary_post_url_has_allowed_host_and_scheme(
    authorized_client, mock_application_get, application_end_use_summary_url, application_task_list_url
):
    response = authorized_client.post(
        application_end_use_summary_url,
        data={
            "_action": "submit",
        },
    )
    assert response.status_code == 302


def test_application_end_use_summary_get_next_form_url_has_allowed_host_and_scheme(
    authorized_client, mock_application_get, application_end_use_summary_url, application_task_list_url
):
    response = authorized_client.post(
        application_end_use_summary_url,
        data={
            "_action": "finish",
            "form_pk": "1",
        },
    )
    assert response.status_code == 302


# def test_application_end_use_summary_post_submit_url_has_allowed_host_and_scheme(
#     authorized_client, mock_application_get, application_end_use_summary_url, application_task_list_url
# ):
#     response = authorized_client.post(
#         application_end_use_summary_url,
#         data={
#             "_action": "submit",
#         },
#     )
#     assert response.status_code == 302
