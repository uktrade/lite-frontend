import pytest
from bs4 import BeautifulSoup
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.fixture
def application_pk(data_standard_case):
    return data_standard_case["case"]["id"]


@pytest.fixture
def declaration_url(application_pk):
    return reverse("applications:declaration", kwargs={"pk": application_pk})


@pytest.fixture
def summary_url(application_pk):
    return reverse("applications:summary", kwargs={"pk": application_pk})


def test_declaration_view(authorized_client, declaration_url, summary_url):
    response = authorized_client.get(declaration_url)

    assert response.status_code == 200
    assertTemplateUsed(response, "form.html")

    soup = BeautifulSoup(response.content, "html.parser")

    assert soup.find("title").string.strip() == "Declaration - LITE - GOV.UK"
    assert soup.find("h1").string.strip() == "Declaration"
    assert soup.find("a", class_="govuk-back-link")["href"] == summary_url
    assert (
        soup.find("label", class_="govuk-checkboxes__label").find("span").string.strip()
        == "The disclosure of information on this application form would be harmful to my/our interests"
    )
    assert (
        soup.find("div", id="pane_agreed_to_declaration_text").find("label").string.strip()
        == "Confirm that you agree to the above by typing 'I AGREE' in this box"
    )
