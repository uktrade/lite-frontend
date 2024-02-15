from bs4 import BeautifulSoup
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test_caseworker_accessibility_statement_view(authorized_client):
    response = authorized_client.get(reverse("caseworker-accessibility-statement"))

    assert response.status_code == 200
    assertTemplateUsed(response, "accessibility/accessibility.html")

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1").string.strip() == "Accessibility statement"
    assert soup.title.string.strip() == "Accessibility statement - LITE Internal"

    expected_back_url = reverse("core:index")
    assert response.context["back_url"] == expected_back_url
