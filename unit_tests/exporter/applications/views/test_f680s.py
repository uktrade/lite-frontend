import pytest

from bs4 import BeautifulSoup
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from core import client
from exporter.f680.constants import (
    ApplicationFormSteps,
)
from exporter.f680.forms import (
    ApplicationNameForm,
    ApplicationSubmissionForm,
)


@pytest.fixture
def authorized_client(authorized_client_factory, mock_exporter_user):
    return authorized_client_factory(mock_exporter_user["user"])


@pytest.fixture
def f680_apply_url():
    return reverse("f680:apply")


@pytest.fixture
def f680_summary_url_with_application(data_f680_case):
    return reverse("f680:summary", kwargs={"pk": data_f680_case["id"]})


@pytest.fixture
def post_to_step(post_to_step_factory, f680_apply_url, mock_application_post):
    return post_to_step_factory(f680_apply_url)


@pytest.fixture
def mock_f680_application_get(requests_mock, data_f680_case):  # PS-IGNORE
    application_id = data_f680_case["id"]  # PS-IGNORE
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")  # PS-IGNORE
    return requests_mock.get(url=url, json=data_f680_case)


@pytest.fixture
def mock_application_post(requests_mock, data_f680_case):
    application = data_f680_case
    url = client._build_absolute_uri(f"/exporter/f680/application/")
    return requests_mock.post(url=url, json=application)


@pytest.fixture(autouse=True)
def set_f680_feature_flag(settings):  # PS-IGNORE
    settings.FEATURE_FLAG_ALLOW_F680 = True  # PS-IGNORE


def test_apply_f680_view(
    authorized_client, f680_apply_url, mock_f680_application_get, post_to_step, mock_application_post
):
    response = authorized_client.get(f680_apply_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Name of the application" in soup.find("h1").text

    # response = authorized_client.post(
    #     f680_summary_url_with_application,
    #     data={"application": {"name": "F680 Test 2"}},
    # )

    response = post_to_step(
        ApplicationFormSteps.APPLICATION_NAME,
        {"name": "F680 Test 2"},
    )

    assert response.status_code == 200
    # assert response.url == f680_summary_url_with_application


# def test_f680_summary_view_with_form(
#     f680_summary_url_with_application, authorized_client, mock_f680_application_get, requests_mock, post_to_step
# ):

#     response = application_flow(
#         f680_summary_url_with_application, authorized_client, mock_f680_application_get, post_to_step
#     )

#     assert response.status_code == 302
#     assert response.url == f680_summary_url_with_application


# def application_flow(
#     f680_summary_url_with_application, authorized_client, mock_f680_application_get, post_to_step, mock_application_post
# ):

#     response = authorized_client.get(f680_summary_url_with_application)
#     assert not response.context["form"].errors

#     content = BeautifulSoup(response.content, "html.parser")
#     heading_element = content.find("h1", class_="govuk-heading-l govuk-!-margin-bottom-2")
#     assert heading_element.string.strip() == "F680 Application"

#     response = post_to_step(
#         ApplicationFormSteps.APPLICATION_NAME,
#         {"application": {"name": "F680 Test 2"}},
#     )

#     return response


def test_f680_summary_view(
    authorized_client,
    f680_summary_url_with_application,  # PS-IGNORE
    mock_f680_application_get,  # PS-IGNORE
):
    response = authorized_client.get(f680_summary_url_with_application)
    assert response.status_code == 200
    assertTemplateUsed(response, "f680/summary.html")
