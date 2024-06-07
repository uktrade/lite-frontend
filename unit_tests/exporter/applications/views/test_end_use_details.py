import pytest

from django.urls import reverse

from lite_content.lite_exporter_frontend.applications import EndUseDetails


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
    assert response.context["back_link_text"] == EndUseDetails.EndUseDetailsSummaryList.BACK_LINK_TEXT
    assert response.context["instruction_text"] == EndUseDetails.EndUseDetailsSummaryList.INSTRUCTION_TEXT
