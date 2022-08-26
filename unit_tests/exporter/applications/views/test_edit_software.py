import pytest

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(
    mock_application_get,
    mock_good_get,
    mock_good_put,
    mock_control_list_entries_get,
    settings,
):
    settings.FEATURE_FLAG_NON_FIREARMS_SOFTWARE_ENABLED = True


@pytest.fixture
def good_on_application(data_standard_case):
    return data_standard_case["case"]["data"]["goods"][0]["good"]


@pytest.mark.parametrize(
    "url_name, form_data, expected",
    (
        (
            "software_edit_name",
            {"name": "new good"},
            {"name": "new good"},
        ),
        (
            "software_edit_control_list_entries",
            {"is_good_controlled": False},
            {"is_good_controlled": False, "control_list_entries": []},
        ),
        (
            "software_edit_control_list_entries",
            {"is_good_controlled": True, "control_list_entries": ["ML1a", "ML22b"]},
            {"is_good_controlled": True, "control_list_entries": ["ML1a", "ML22b"]},
        ),
    ),
)
def test_edit_software_post(
    authorized_client,
    requests_mock,
    application,
    good_on_application,
    url_name,
    form_data,
    expected,
    software_product_summary_url,
):
    url = reverse(f"applications:{url_name}", kwargs={"pk": application["id"], "good_pk": good_on_application["id"]})

    response = authorized_client.post(
        url,
        data=form_data,
    )

    assert response.status_code == 302
    assert response.url == software_product_summary_url
    assert requests_mock.last_request.json() == expected


@pytest.mark.parametrize(
    "url_name,good_on_application_data,initial",
    (
        (
            "software_edit_name",
            {},
            {"name": "p1"},
        ),
        (
            "software_edit_control_list_entries",
            {},
            {"control_list_entries": ["ML1a", "ML22b"], "is_good_controlled": "True"},
        ),
    ),
)
def test_edit_software_initial(
    authorized_client,
    application,
    good_on_application,
    url_name,
    good_on_application_data,
    initial,
):
    good_on_application.update(good_on_application_data)

    url = reverse(f"applications:{url_name}", kwargs={"pk": application["id"], "good_pk": good_on_application["id"]})
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert response.context["form"].initial == initial
