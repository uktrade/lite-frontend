import pytest

from django.urls import reverse

from exporter.applications.views.goods.software.views.constants import AddGoodTechnologySteps


@pytest.fixture(autouse=True)
def setup(
    mock_application_get,
    mock_good_get,
    mock_good_put,
    mock_exporter_control_list_entries_get,
):
    yield


@pytest.fixture
def good_on_application(data_standard_case):
    return data_standard_case["case"]["data"]["goods"][0]["good"]


@pytest.mark.parametrize(
    "url_name, form_data, expected",
    (
        (
            "technology_edit_name",
            {"name": "new good"},
            {"name": "new good"},
        ),
        (
            "technology_edit_control_list_entries",
            {"is_good_controlled": False},
            {"is_good_controlled": False, "control_list_entries": []},
        ),
        (
            "technology_edit_control_list_entries",
            {"is_good_controlled": True, "control_list_entries": ["ML1a", "ML22b"]},
            {"is_good_controlled": True, "control_list_entries": ["ML1a", "ML22b"]},
        ),
    ),
)
def test_edit_technology_post(
    authorized_client,
    requests_mock,
    application,
    good_on_application,
    url_name,
    form_data,
    expected,
    technology_product_summary_url,
):
    url = reverse(f"applications:{url_name}", kwargs={"pk": application["id"], "good_pk": good_on_application["id"]})

    response = authorized_client.post(
        url,
        data=form_data,
    )

    assert response.status_code == 302
    assert response.url == technology_product_summary_url
    assert requests_mock.last_request.json() == expected


@pytest.mark.parametrize(
    "url_name,good_on_application_data,initial",
    (
        (
            "technology_edit_name",
            {},
            {"name": "p1"},
        ),
        (
            "technology_edit_control_list_entries",
            {},
            {"control_list_entries": ["ML1a", "ML22b"], "is_good_controlled": "True"},
        ),
    ),
)
def test_edit_technology_initial(
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


@pytest.fixture(autouse=True)
def edit_pv_grading_url(application, good_on_application):
    return reverse(
        "applications:technology_edit_pv_grading",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )


@pytest.fixture
def goto_step_pv_grading(goto_step_factory, edit_pv_grading_url):
    return goto_step_factory(edit_pv_grading_url)


@pytest.fixture
def post_to_step_pv_grading(post_to_step_factory, edit_pv_grading_url):
    return post_to_step_factory(edit_pv_grading_url)


def test_edit_pv_grading(
    requests_mock,
    pv_gradings,
    goto_step_pv_grading,
    post_to_step_pv_grading,
    technology_product_summary_url,
):
    response = goto_step_pv_grading(AddGoodTechnologySteps.PV_GRADING)
    assert response.status_code == 200

    response = post_to_step_pv_grading(
        AddGoodTechnologySteps.PV_GRADING,
        {"is_pv_graded": True},
    )

    assert response.status_code == 200

    response = post_to_step_pv_grading(
        AddGoodTechnologySteps.PV_GRADING_DETAILS,
        {
            "prefix": "NATO",
            "grading": "official",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue_0": "20",
            "date_of_issue_1": "02",
            "date_of_issue_2": "2020",
        },
    )

    assert response.status_code == 302
    assert response.url == technology_product_summary_url
    assert requests_mock.last_request.json() == {
        "is_pv_graded": "yes",
        "pv_grading_details": {
            "prefix": "NATO",
            "grading": "official",
            "suffix": "",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue": "2020-02-20",
        },
    }


def test_edit_pv_grading_details(
    authorized_client,
    application,
    good_on_application,
    requests_mock,
    pv_gradings,
    technology_product_summary_url,
):
    url = reverse(
        "applications:technology_edit_pv_grading_details",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )

    response = authorized_client.post(
        url,
        data={
            "prefix": "NATO",
            "grading": "official",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue_0": "20",
            "date_of_issue_1": "02",
            "date_of_issue_2": "2020",
        },
    )

    assert response.status_code == 302
    assert response.url == technology_product_summary_url
    assert requests_mock.last_request.json() == {
        "is_pv_graded": "yes",
        "pv_grading_details": {
            "prefix": "NATO",
            "grading": "official",
            "suffix": "",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue": "2020-02-20",
        },
    }
