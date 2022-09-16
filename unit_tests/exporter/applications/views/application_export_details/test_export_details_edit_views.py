import pytest
from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(
    mock_application_put,
    mock_application_get,
    settings,
    no_op_storage,
):
    settings.FEATURE_FLAG_F680_SECURITY_CLASSIFIED_ENABLED = True


@pytest.fixture
def application_export_details_summary_url(data_standard_case):
    application_id = data_standard_case["case"]["data"]["id"]
    return reverse(
        "applications:application_export_details_summary",
        kwargs={
            "pk": application_id,
        },
    )


@pytest.mark.parametrize(
    "url_name, form_data, expected",
    (
        (
            "edit_export_details_f680_reference_number",
            {"f680_reference_number": "new ref number"},
            {"f680_reference_number": "new ref number"},
        ),
    ),
)
def test_edit_export_details_post(
    authorized_client,
    requests_mock,
    application,
    url_name,
    form_data,
    expected,
    application_export_details_summary_url,
):
    url = reverse(f"applications:{url_name}", kwargs={"pk": application["id"]})

    response = authorized_client.post(
        url,
        data=form_data,
    )
    assert response.status_code == 302
    assert response.url == application_export_details_summary_url
    assert requests_mock.last_request.json() == expected
