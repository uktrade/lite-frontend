import pytest

from django.urls import reverse


@pytest.fixture()
def delete_url(application_id):
    return reverse("applications:delete", kwargs={"pk": application_id})


def parse_summary(summary_element):
    summary = []
    for row in summary_element.select(".govuk-summary-list__row"):
        summary.append(
            (
                row.select_one(".govuk-summary-list__key").text.strip(),
                row.select_one(".govuk-summary-list__value").text.strip(),
            )
        )
    return summary


@pytest.mark.parametrize(
    "application_json, expected_summary",
    (
        (
            {
                "name": "SIEL Application",
                "case_type": {
                    "type": {"key": "application", "value": "Application"},
                    "sub_type": {"key": "standard", "value": "Standard Licence"},
                    "reference": {"key": "siel", "value": "Standard Individual Export Licence"},
                },
                "created_at": "2024-01-01",
            },
            [
                ("Reference", "SIEL Application"),
                ("Licence type", "Standard Individual Export Licence"),
                ("Created", "12:00am 01 January 2024"),
            ],
        ),
        (
            {
                "name": "Export Licence Application",
                "case_type": {
                    "type": {"key": "application", "value": "Application"},
                    "reference": {"key": "export_licence", "value": "Export Licence"},
                },
                "created_at": "2024-01-01",
            },
            [
                ("Reference", "Export Licence Application"),
                ("Licence type", "Export Licence"),
                ("Created", "12:00am 01 January 2024"),
            ],
        ),
    ),
)
def test_delete_application_GET(
    authorized_client,
    delete_url,
    requests_mock,
    api_url,
    application_id,
    application_json,
    beautiful_soup,
    expected_summary,
):
    application_api_url = api_url(f"/applications/{application_id}/")
    requests_mock.get(
        application_api_url,
        json=application_json,
    )
    response = authorized_client.get(delete_url)

    assert response.status_code == 200

    soup = beautiful_soup(response.content)
    summary = soup.select_one(".govuk-summary-list")
    assert parse_summary(summary) == expected_summary
