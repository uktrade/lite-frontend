import pytest

from bs4 import BeautifulSoup
from django.urls import reverse

from core import client


@pytest.fixture
def authorized_client(authorized_client_factory, mock_exporter_user):
    return authorized_client_factory(mock_exporter_user["user"])


@pytest.fixture
def f680_summary_url_with_application(data_f680_case):
    return reverse("f680:summary", kwargs={"pk": data_f680_case["id"]})


@pytest.fixture
def mock_f680_application_get(requests_mock, data_f680_case):  # PS-IGNORE
    application_id = data_f680_case["id"]  # PS-IGNORE
    url = client._build_absolute_uri(f"/exporter/f680/application/{application_id}/")  # PS-IGNORE
    return requests_mock.get(url=url, json=data_f680_case)


@pytest.fixture(autouse=True)
def set_f680_fetaure_flag(settings):  # PS-IGNORE
    settings.FEATURE_FLAG_ALLOW_F680 = True  # PS-IGNORE


def test_apply_f680_view(authorized_client):  # PS-IGNORE
    url = reverse("f680:apply")  # PS-IGNORE
    response = authorized_client.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Name of the application" in soup.find("h1").text


def test_f680_summary_view_with_form(
    f680_summary_url_with_application, authorized_client, mock_f680_application_get, requests_mock
):

    response = application_flow(f680_summary_url_with_application, authorized_client, mock_f680_application_get)

    assert response.status_code == 302
    assert response.url == f680_summary_url_with_application


def application_flow(f680_summary_url_with_application, authorized_client, mock_f680_application_get):

    response = authorized_client.get(f680_summary_url_with_application)
    assert not response.context["form"].errors

    content = BeautifulSoup(response.content, "html.parser")
    heading_element = content.find("h1", class_="govuk-heading-l govuk-!-margin-bottom-2")
    assert heading_element.string.strip() == "F680 Application"

    response = authorized_client.post(
        f680_summary_url_with_application,
        data={"application": {"name": "F680 Test 3"}},
    )

    return response


def test_f680_summary_view(
    authorized_client,
    f680_summary_url_with_application,  # PS-IGNORE
    mock_f680_application_get,  # PS-IGNORE
):
    response = authorized_client.get(f680_summary_url_with_application)
    assert response.status_code == 200
