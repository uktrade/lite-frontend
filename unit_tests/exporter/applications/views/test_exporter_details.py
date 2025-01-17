import pytest

from django.urls import reverse


@pytest.fixture
def application_pk(data_standard_case):
    return data_standard_case["case"]["data"]["id"]


@pytest.fixture
def application_export_details_url(application_pk):
    return reverse(
        "applications:export_details",
        kwargs={
            "pk": application_pk,
        },
    )


def test_application_export_details_return_date(
    authorized_client,
    mock_application_get,
    application_export_details_url,
    requests_mock,
    application_pk,
    beautiful_soup,
):

    requests_mock.put(
        f"/applications/{application_pk}/temporary-export-details/",
        json={},
    )

    response = authorized_client.post(
        application_export_details_url,
        data={
            "_action": "submit",
            "goods_starting_point": "GB",
            "export_type": "temporary",
            "form_pk": "3",
        },
    )

    soup = beautiful_soup(response.content)
    assert soup.find("legend").label.text.strip() == "Proposed date the products will return to the UK"
    assert "For example, 12 11" in soup.find(id="proposed_return_date-hint").text.strip()
