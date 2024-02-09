from bs4 import BeautifulSoup
from django.urls import reverse
from django.conf import settings
from pytest_django.asserts import assertTemplateUsed
import pytest

from core import client


def test_register_name(authorized_client):
    session = authorized_client.session
    session["first_name"] = None
    session["last_name"] = None
    session.save()
    url = reverse("core:register_name")
    response = authorized_client.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "What is your name? - LITE - GOV.UK"


def test_register_name_save(authorized_client, requests_mock, mock_get_profile):
    session = authorized_client.session
    session["first_name"] = None
    session["last_name"] = None
    session.save()

    mock_save_user = requests_mock.post(client._build_absolute_uri("/users/authenticate/"), json={})
    url = reverse("core:register_name")
    response = authorized_client.post(url, data={"first_name": "Joe", "last_name": "Blogs"})

    assert mock_save_user.call_count == 1
    assert mock_get_profile.call_count == 1
    assert mock_save_user.last_request.json() == {
        "email": "foo@example.com",
        "user_profile": {"first_name": "Joe", "last_name": "Blogs"},
        "sub": "123456789xyzqpr",
    }

    assert response.status_code == 302
    assert response.url == settings.LOGIN_URL


def test_register_name_redirects_name_known(authorized_client):
    session = authorized_client.session
    url = reverse("core:register_name")
    response = authorized_client.get(url)
    assert response.status_code == 302
    assert session["first_name"]
    assert session["last_name"]
    assert response.url == settings.LOGIN_URL


@pytest.fixture
def home_url():
    return reverse("core:home")


def test_home_no_logged_in_go_uk_user_start_page_template_used(client, home_url):
    response = client.get(home_url)
    assert response.status_code == 200
    assertTemplateUsed(response, "core/start-gov-uk.html")


@pytest.fixture
def mock_require_serial_numbers(requests_mock):
    requests_mock.get(
        "/applications/require-serial-numbers/?page=1",
        json={
            "results": [],
        },
    )


def test_survey_alert_displayed(authorized_client, settings, home_url, mock_require_serial_numbers):
    settings.SURVEY_URL = "http://example.com"

    response = authorized_client.get(home_url)
    assertTemplateUsed(response, "core/hub.html")

    soup = BeautifulSoup(response.content, "html.parser")

    banner = soup.select("#survey-notification-banner")
    assert banner

    links = soup.select("#survey-notification-banner .govuk-notification-banner__link")
    assert len(links) == 1
    link = links[0]
    assert link.attrs["href"] == "http://example.com"


def test_survey_alert_not_displayed(authorized_client, settings, home_url, mock_require_serial_numbers):
    settings.SURVEY_URL = ""

    response = authorized_client.get(home_url)
    assertTemplateUsed(response, "core/hub.html")

    soup = BeautifulSoup(response.content, "html.parser")

    banner = soup.select("#survey-notification-banner")
    assert not banner


def test_privacy_notice_view(authorized_client):
    response = authorized_client.get(reverse("core:privacy_notice"))

    assert response.status_code == 200
    assertTemplateUsed(response, "core/privacy_notice.html")

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1").string.strip() == "Privacy notice"
    assert soup.title.string.strip() == "Privacy notice - LITE - GOV.UK"


def test_exporter_accessibility_statement_view(authorized_client):
    response = authorized_client.get(reverse("exporter-accessibility-statement"))

    assert response.status_code == 200
    assertTemplateUsed(response, "accessibility/accessibility.html")

    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("h1").string.strip() == "Accessibility statement"
    assert soup.title.string.strip() == "Accessibility statement - LITE - GOV.UK"

    expected_back_url = reverse("core:home")
    assert response.context["back_url"] == expected_back_url
