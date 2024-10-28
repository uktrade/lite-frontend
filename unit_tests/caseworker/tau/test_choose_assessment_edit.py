import pytest

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case,
    mock_regime_entries,
    mock_application_good_documents,
    mock_good_precedent_endpoint_empty,
    mock_mtcr_entries_get,
    mock_wassenaar_entries_get,
    mock_nsg_entries_get,
    mock_cwc_entries_get,
    mock_ag_entries_get,
):
    yield


@pytest.fixture
def choose_edit_assessments_url(data_standard_case):
    return reverse(
        "cases:tau:choose_multiple_edit",
        kwargs={"queue_pk": "1b926457-5c9e-4916-8497-51886e51863a", "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def multiple_edit_assessments_url(data_standard_case):
    return reverse(
        "cases:tau:multiple_edit",
        kwargs={"queue_pk": "1b926457-5c9e-4916-8497-51886e51863a", "pk": data_standard_case["case"]["id"]},
    )


def test_choose_edit_assessments_GET(
    authorized_client,
    choose_edit_assessments_url,
):
    # Get raises a NotImplemented error, this view is POST only
    with pytest.raises(NotImplementedError):
        authorized_client.get(choose_edit_assessments_url)


@pytest.mark.parametrize(
    "data, form_count, expected_querystring",
    (
        ({"form-0-selected": True, "form-0-good_on_application_id": "GOA1"}, 1, "line_numbers=1"),
        ({"form-0-selected": False, "form-0-good_on_application_id": "GOA1"}, 1, ""),
        (
            {
                "form-0-selected": True,
                "form-0-good_on_application_id": "GOA1",
                "form-1-selected": True,
                "form-1-good_on_application_id": "GOA2",
            },
            2,
            "line_numbers=1&line_numbers=2",
        ),
        (
            {
                "form-0-selected": False,
                "form-0-good_on_application_id": "GOA1",
                "form-1-selected": True,
                "form-1-good_on_application_id": "GOA2",
            },
            2,
            "line_numbers=2",
        ),
    ),
)
def test_choose_edit_assessments_POST(
    authorized_client,
    choose_edit_assessments_url,
    multiple_edit_assessments_url,
    data_queue,
    data_standard_case,
    mock_control_list_entries,
    mock_gov_user,
    data,
    form_count,
    expected_querystring,
):
    good_on_application_1 = data_standard_case["case"]["data"]["goods"][0]
    good_on_application_2 = data_standard_case["case"]["data"]["goods"][1]

    post_data = {
        "form-TOTAL_FORMS": form_count,
        "form-INITIAL_FORMS": form_count,
        "form-MIN_NUM_FORMS": 0,
        "form-MAX_NUM_FORMS": 1000,
        "form-TOTAL_FORMS": form_count,
    }
    for key, value in data.items():
        if value == "GOA1":
            value = good_on_application_1["id"]
        if value == "GOA2":
            value = good_on_application_2["id"]
        post_data[key] = value

    response = authorized_client.post(choose_edit_assessments_url, post_data, follow=True)
    assert response.status_code == 200
    redirect_location = response.redirect_chain[-1][0]
    assert multiple_edit_assessments_url in redirect_location
    assert redirect_location.split("?")[1] == expected_querystring
