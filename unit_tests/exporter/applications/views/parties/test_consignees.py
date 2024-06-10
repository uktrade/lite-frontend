import pytest
from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def mock_get_application(requests_mock, data_standard_case):
    applications_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=applications_url, json=data_standard_case["case"]["data"])


@pytest.fixture
def application_pk(data_standard_case):
    return data_standard_case["case"]["id"]


@pytest.fixture
def application_parties_consignee_summary_url(application_pk):
    return reverse("applications:consignee", kwargs={"pk": application_pk})


def test_application_parties_consignee_summary(authorized_client, application_parties_consignee_summary_url):
    response = authorized_client.get(application_parties_consignee_summary_url)
    assertTemplateUsed(response, "applications/consignee.html")
