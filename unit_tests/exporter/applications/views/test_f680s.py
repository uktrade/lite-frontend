import pytest

from bs4 import BeautifulSoup
from django.urls import reverse

from core import client


@pytest.fixture
def authorized_client(authorized_client_factory, mock_exporter_user):
    return authorized_client_factory(mock_exporter_user["user"])


@pytest.fixture
def mock_f680_application_get(requests_mock, data_f680_case):  # PS-IGNORE
    application = data_f680_case["id"]  # PS-IGNORE
    url = client._build_absolute_uri(f"/exporter/f680/application/{application}/")  # PS-IGNORE
    return requests_mock.get(url=url, json=application)


@pytest.fixture(autouse=True)
def set_f680_fetaure_flag(settings):  # PS-IGNORE
    settings.FEATURE_FLAG_ALLOW_F680 = True  # PS-IGNORE


def test_apply_f680_view(authorized_client, settings):  # PS-IGNORE
    url = reverse("f680:apply")  # PS-IGNORE
    response = authorized_client.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert "Name of the application" in soup.find("h1").text


def test_f680_summary_view(
    authorized_client, data_f680_case, set_f680_fetaure_flag, mock_f680_application_get
):  # PS-IGNORE
    url = reverse("f680:summary", kwargs={"pk": data_f680_case["id"]})  # PS-IGNORE
    response = authorized_client.get(url)
    assert response.status_code == 200
