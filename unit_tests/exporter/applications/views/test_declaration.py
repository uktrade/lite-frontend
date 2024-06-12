import pytest
from bs4 import BeautifulSoup
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from requests.exceptions import HTTPError

from core import client


@pytest.fixture
def application_pk(data_standard_case):
    return data_standard_case["case"]["id"]


@pytest.fixture
def declaration_url(application_pk):
    return reverse("applications:declaration", kwargs={"pk": application_pk})


@pytest.fixture
def summary_url(application_pk):
    return reverse("applications:summary", kwargs={"pk": application_pk})


@pytest.fixture
def mock_get_application(requests_mock, data_standard_case):
    applications_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=applications_url, json=data_standard_case["case"]["data"])


@pytest.fixture
def mock_get_case_notes(application, requests_mock):
    return requests_mock.get(
        f"/cases/{application['id']}/case-notes/",
        json={"case_notes": []},
    )


def test_declaration_view(authorized_client, declaration_url, summary_url, mock_get_application):
    response = authorized_client.get(declaration_url)

    assert response.status_code == 200
    assertTemplateUsed(response, "core/form.html")

    soup = BeautifulSoup(response.content, "html.parser")

    assert soup.find("title").string.strip() == "Submit your application - LITE - GOV.UK"
    assert soup.find("h1").string.strip() == "Submit your application"
    assert soup.find("a", class_="govuk-back-link")["href"] == summary_url
    assert soup.find("a", class_="govuk-back-link").string.strip() == "Back to check your answers"
    assert [h2.string.strip() for h2 in soup.find_all("h2", class_="govuk-heading-m")] == [
        "Freedom of Information disclosure",
        "Declaration",
    ]
    p_contents = [[str(el) for el in p.contents] for p in soup.find_all("p", class_="govuk-body")]
    assert p_contents == [
        [
            "Any information you provide in this application may be made public under the Freedom of Information Act 2000."
        ],
        ["Do you agree to make the application details publicly available?"],
        [
            '<a class="govuk-link" href="https://ico.org.uk/for-organisations/guide-to-freedom-of-information/">Find out more about the Freedom of Information Act 2000 and exemptions at the Information Commissioner\'s Office</a>',
            ".",
        ],
        [
            "Making a misleading application is an offence as set out in the ",
            '<a class="govuk-link" href="https://www.legislation.gov.uk/uksi/2008/3231/contents/made">Export Control Order 2008</a>',
            ".",
        ],
        [
            "The licensee must comply with the licence conditions even, where relevant, after completing the activity authorised by the licence. Failure to do so is an offence."
        ],
        [
            "Information provided in this application may be passed to international organisations or other governments in accordance with commitments entered into by His Majesty's Government."
        ],
        [
            "If ECJU staff have completed this application on your behalf, they based it on the information you provided. You as the exporter are responsible for the accuracy of the information."
        ],
    ]
    assert soup.find("input", id="submit-id-submit")["value"] == "Accept and submit"


def test_summary_post_redirects_to_declaration(
    authorized_client, summary_url, declaration_url, mock_get_application, mock_get_case_notes
):
    response = authorized_client.get(summary_url)
    assert response.status_code == 200

    response = authorized_client.post(summary_url, data={})
    assert response.status_code == 302
    assert response.url == declaration_url


@pytest.fixture
def invalid_application_pk():
    return "82617c05-a050-428b-ae68-ed5dc985f4af"


@pytest.fixture
def mock_get_application_invalid_pk(requests_mock, invalid_application_pk):
    requests_mock.get(
        client._build_absolute_uri(f"/applications/{invalid_application_pk}/"),
        json={},
        status_code=404,
    )


def test_declaration_application_not_found_raises_404(
    authorized_client, declaration_url, invalid_application_pk, mock_get_application_invalid_pk
):
    declaration_url_invalid_pk = reverse("applications:declaration", kwargs={"pk": invalid_application_pk})

    response = authorized_client.get(declaration_url_invalid_pk)
    assert response.status_code == 404
