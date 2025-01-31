import pytest

from bs4 import BeautifulSoup
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from core import client
from exporter.f680.constants import (
    ApplicationFormSteps,
)
from exporter.f680.forms import ApplicationNameForm, ApplicationSubmissionForm
from unit_tests.helpers import reload_urlconf


@pytest.fixture
def authorized_client(authorized_client_factory, mock_exporter_user):
    return authorized_client_factory(mock_exporter_user["user"])


@pytest.fixture
def f680_apply_url():  # PS-IGNORE
    return reverse("f680:apply")  # PS-IGNORE


@pytest.fixture
def f680_summary_url_with_application(data_f680_case):  # PS-IGNORE
    return reverse("f680:summary", kwargs={"pk": data_f680_case["id"]})  # PS-IGNORE


@pytest.fixture
def post_to_step(post_to_step_factory, f680_apply_url, mock_application_post):
    return post_to_step_factory(f680_apply_url)  # PS-IGNORE


@pytest.fixture
def mock_f680_application_get(requests_mock, data_f680_case):  # PS-IGNORE
    application_id = data_f680_case["id"]  # PS-IGNORE
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")  # PS-IGNORE
    return requests_mock.get(url=url, json=data_f680_case)  # PS-IGNORE


@pytest.fixture
def mock_application_post(requests_mock, data_f680_case):  # PS-IGNORE
    application = data_f680_case  # PS-IGNORE
    url = client._build_absolute_uri(f"/exporter/f680/application/")  # PS-IGNORE
    return requests_mock.post(url=url, json=application, status_code=201)


@pytest.fixture(autouse=True)
def set_f680_feature_flag(settings):  # PS-IGNORE
    settings.FEATURE_FLAG_ALLOW_F680 = True  # PS-IGNORE
    reload_urlconf(["exporter.f680.urls", settings.ROOT_URLCONF])
    reload_urlconf(["exporter.apply_for_a_licence.urls", settings.ROOT_URLCONF])


def test_triage_f680_apply_redirect(authorized_client, f680_apply_url):  # PS-IGNORE
    response = authorized_client.post(reverse("apply_for_a_licence:f680_questions"))  # PS-IGNORE
    assert response.status_code == 302
    assert response.url == f680_apply_url


def test_create_f680_view(
    authorized_client,
    f680_apply_url,  # PS-IGNORE
    mock_f680_application_get,  # PS-IGNORE
    post_to_step,
    mock_application_post,
    f680_summary_url_with_application,
):
    response = authorized_client.get(f680_apply_url)  # PS-IGNORE
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Name of the application" in soup.find("h1").text
    assert isinstance(response.context["form"], ApplicationNameForm)

    response = post_to_step(
        ApplicationFormSteps.APPLICATION_NAME,
        {"name": "F680 Test"},  # PS-IGNORE
    )

    assert response.status_code == 302
    assert response.url == f680_summary_url_with_application


def test_f680_summary_view(
    authorized_client,
    f680_summary_url_with_application,  # PS-IGNORE
    mock_f680_application_get,  # PS-IGNORE
):
    response = authorized_client.get(f680_summary_url_with_application)  # PS-IGNORE

    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ApplicationSubmissionForm)
    assertTemplateUsed(response, "f680/summary.html")  # PS-IGNORE

    response = authorized_client.get(f680_summary_url_with_application)  # PS-IGNORE
    assert not response.context["form"].errors

    content = BeautifulSoup(response.content, "html.parser")
    heading_element = content.find("h1", class_="govuk-heading-l govuk-!-margin-bottom-2")
    assert heading_element.string.strip() == "F680 Application"  # PS-IGNORE

    response = authorized_client.post(
        f680_summary_url_with_application,  # PS-IGNORE
    )

    assert response.status_code == 302
    assert response.url == f680_summary_url_with_application  # PS-IGNORE
