import pytest

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(
    mock_application_get,
    mock_good_get,
    mock_good_put,
    settings,
):
    settings.FEATURE_FLAG_NON_FIREARMS_ENABLED = True


@pytest.fixture
def good_on_application(data_standard_case):
    return data_standard_case["case"]["data"]["goods"][0]["good"]


@pytest.fixture
def platform_summary_url(application, good_on_application):
    return reverse(
        "applications:platform_summary",
        kwargs={
            "pk": application["id"],
            "good_pk": good_on_application["id"],
        },
    )


@pytest.mark.parametrize(
    "url_name, form_data, expected",
    (
        (
            "platform_edit_name",
            {"name": "new good"},
            {"name": "new good"},
        ),
    ),
)
def test_edit_platform(
    authorized_client,
    requests_mock,
    application,
    good_on_application,
    url_name,
    form_data,
    expected,
    platform_summary_url,
):
    url = reverse(f"applications:{url_name}", kwargs={"pk": application["id"], "good_pk": good_on_application["id"]})

    response = authorized_client.post(
        url,
        data=form_data,
    )

    assert response.status_code == 302
    assert response.url == platform_summary_url
    assert requests_mock.last_request.json() == expected
