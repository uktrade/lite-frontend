import pytest

from bs4 import BeautifulSoup
from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from exporter.applications.forms.appeal import AppealForm


@pytest.fixture
def application_url(data_standard_case):
    case_pk = data_standard_case["case"]["id"]

    return reverse("applications:application", kwargs={"pk": case_pk})


@pytest.fixture
def appeal_url(data_standard_case):
    case_pk = data_standard_case["case"]["id"]

    return reverse("applications:appeal", kwargs={"case_pk": case_pk})


def test_appeal_view(authorized_client, appeal_url, application_url):
    response = authorized_client.get(appeal_url)

    assert response.status_code == 200

    assert isinstance(response.context["form"], AppealForm)
    assertTemplateUsed(response, "core/form.html")

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1").string == "Appeal refusal decision"
    assert soup.title.string.strip() == "Appeal refusal decision - LITE - GOV.UK"
    assert soup.find("a", {"id": "back-link"})["href"] == application_url
    assert soup.find("input", {"id": "submit-id-submit"})["value"] == "Submit appeal request"
    assert soup.find("a", {"id": "cancel-id-cancel"})["href"] == application_url


def test_post_appeal(authorized_client, appeal_url, application_url):
    response = authorized_client.post(
        appeal_url,
        data={"grounds_for_appeal": "These are my grounds for appeal"},
    )

    assert response.status_code == 302
    assert response.url == application_url
