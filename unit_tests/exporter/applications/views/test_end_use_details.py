import pytest

from django.urls import reverse
from lite_forms.views import ensure_redirect_destination_relative, UnsafeRedirectDestination


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


def test_ensure_redirect_destination_relative_valid():
    try:
        ensure_redirect_destination_relative("/valid/path")
    except UnsafeRedirectDestination:
        pytest.fail("UnsafeRedirectDestination was raised unexpectedly!")


def test_ensure_redirect_destination_relative_backslashes_valid():
    try:
        ensure_redirect_destination_relative("\\valid\path")
    except UnsafeRedirectDestination:
        pytest.fail("UnsafeRedirectDestination was raised unexpectedly!")


def test_ensure_redirect_destination_relative_invalid():
    with pytest.raises(UnsafeRedirectDestination) as error:
        ensure_redirect_destination_relative("https://malicious.com/invalid/path")


def test_ensure_redirect_destination_relative_backslashes_invalid():
    with pytest.raises(UnsafeRedirectDestination):
        ensure_redirect_destination_relative("https:/malicious.com")
