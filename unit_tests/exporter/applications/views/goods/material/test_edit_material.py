import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from exporter.applications.views.goods.material.views.constants import AddGoodMaterialSteps
from exporter.goods.forms.common import ProductDescriptionForm


@pytest.fixture(autouse=True)
def setup(
    mock_application_get,
    mock_good_get,
    mock_good_put,
    mock_exporter_control_list_entries_get,
    mock_good_document_post,
    mock_good_document_delete,
    no_op_storage,
):
    yield


@pytest.fixture
def good_on_application(data_standard_case):
    good_on_application = data_standard_case["case"]["data"]["goods"][0]["good"]
    good_on_application.update(
        {
            "product_description": "Product description",
        }
    )
    return good_on_application


@pytest.fixture
def product_document():
    return {
        "product_document": SimpleUploadedFile("data sheet", b"This is a detailed spec of this Rifle"),
        "description": "product data sheet",
    }


@pytest.fixture(autouse=True)
def edit_pv_grading_url(application, good_on_application):
    return reverse(
        "applications:material_edit_pv_grading",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )


@pytest.fixture
def goto_step_pv_grading(goto_step_factory, edit_pv_grading_url):
    return goto_step_factory(edit_pv_grading_url)


@pytest.fixture
def post_to_step_pv_grading(post_to_step_factory, edit_pv_grading_url):
    return post_to_step_factory(edit_pv_grading_url)


@pytest.mark.parametrize(
    "url_name, form_data, expected",
    (
        (
            "material_edit_name",
            {"name": "new good"},
            {"name": "new good"},
        ),
        (
            "material_edit_control_list_entries",
            {"is_good_controlled": False},
            {"is_good_controlled": False, "control_list_entries": []},
        ),
        (
            "material_edit_control_list_entries",
            {"is_good_controlled": True, "control_list_entries": ["ML1a", "ML22b"]},
            {"is_good_controlled": True, "control_list_entries": ["ML1a", "ML22b"]},
        ),
        (
            "material_edit_part_number",
            {
                "part_number": "12345",
            },
            {
                "no_part_number_comments": "",
                "part_number": "12345",
            },
        ),
        (
            "material_edit_part_number",
            {
                "part_number_missing": True,
                "no_part_number_comments": "No part number",
            },
            {
                "no_part_number_comments": "No part number",
                "part_number": "",
            },
        ),
        (
            "material_edit_military_use",
            {
                "is_military_use": "yes_designed",
            },
            {
                "is_military_use": "yes_designed",
                "modified_military_use_details": "",
            },
        ),
        (
            "material_edit_military_use",
            {"is_military_use": "yes_modified", "modified_military_use_details": "Modified details"},
            {
                "is_military_use": "yes_modified",
                "modified_military_use_details": "Modified details",
            },
        ),
        (
            "material_edit_product_description",
            {"product_description": "Product description"},
            {"product_description": "Product description"},
        ),
    ),
)
def test_edit_material_post(
    authorized_client,
    requests_mock,
    application,
    good_on_application,
    url_name,
    form_data,
    expected,
    material_product_summary_url,
):
    url = reverse(f"applications:{url_name}", kwargs={"pk": application["id"], "good_pk": good_on_application["id"]})

    response = authorized_client.post(
        url,
        data=form_data,
    )
    assert response.status_code == 302
    assert response.url == material_product_summary_url
    assert requests_mock.last_request.json() == expected


@pytest.mark.parametrize(
    "url_name,good_on_application_data,initial",
    (
        (
            "material_edit_name",
            {},
            {"name": "p1"},
        ),
        (
            "material_edit_control_list_entries",
            {},
            {"control_list_entries": ["ML1a", "ML22b"], "is_good_controlled": "True"},
        ),
        (
            "material_edit_part_number",
            {},
            {"part_number": "44"},
        ),
        (
            "material_edit_part_number",
            {"no_part_number_comments": "No part number"},
            {"no_part_number_comments": "No part number", "part_number_missing": True},
        ),
        (
            "material_edit_military_use",
            {
                "is_military_use": {"key": "yes_designed"},
            },
            {
                "is_military_use": "yes_designed",
                "modified_military_use_details": None,
            },
        ),
        (
            "material_edit_military_use",
            {"is_military_use": {"key": "yes_modified"}, "modified_military_use_details": "Modified details"},
            {
                "is_military_use": "yes_modified",
                "modified_military_use_details": "Modified details",
            },
        ),
        (
            "material_edit_product_description",
            {"product_description": "Product description"},
            {"product_description": "Product description"},
        ),
    ),
)
def test_edit_material_initial(
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


def test_edit_pv_grading(
    requests_mock,
    pv_gradings,
    goto_step_pv_grading,
    post_to_step_pv_grading,
    material_product_summary_url,
):
    response = goto_step_pv_grading(AddGoodMaterialSteps.PV_GRADING)
    assert response.status_code == 200

    response = post_to_step_pv_grading(
        AddGoodMaterialSteps.PV_GRADING,
        {"is_pv_graded": True},
    )

    assert response.status_code == 200

    response = post_to_step_pv_grading(
        AddGoodMaterialSteps.PV_GRADING_DETAILS,
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
    assert response.url == material_product_summary_url
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
    material_product_summary_url,
):
    url = reverse(
        "applications:material_edit_pv_grading_details",
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
    assert response.url == material_product_summary_url
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


@pytest.fixture
def edit_product_availability_url(application, good_on_application):
    return reverse(
        "applications:material_edit_product_document_availability",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )


@pytest.fixture
def post_to_step_edit_product_document_availability(post_to_step_factory, edit_product_availability_url):
    return post_to_step_factory(edit_product_availability_url)


def test_edit_product_document_availability_select_not_available(
    requests_mock, post_to_step_edit_product_document_availability, material_product_summary_url
):
    response = post_to_step_edit_product_document_availability(
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        data={"is_document_available": False, "no_document_comments": "Product not manufactured yet"},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductDescriptionForm)

    response = post_to_step_edit_product_document_availability(
        AddGoodMaterialSteps.PRODUCT_DESCRIPTION,
        data={"product_description": "This is the product description"},
    )

    assert response.status_code == 302
    assert response.url == material_product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.request_history.pop().json() == {
        "is_document_available": False,
        "no_document_comments": "Product not manufactured yet",
        "product_description": "This is the product description",
    }


def test_edit_product_document_availability_select_available_but_sensitive(
    requests_mock,
    post_to_step_edit_product_document_availability,
    material_product_summary_url,
):
    response = post_to_step_edit_product_document_availability(
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        data={"is_document_available": True},
    )
    response = post_to_step_edit_product_document_availability(
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        data={"is_document_sensitive": True},
    )

    assert response.status_code == 302
    assert response.url == material_product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.request_history.pop().json() == {
        "is_document_available": True,
        "no_document_comments": "",
        "is_document_sensitive": True,
    }


def test_edit_product_document_availability_upload_new_document(
    requests_mock, post_to_step_edit_product_document_availability, product_document, material_product_summary_url
):
    response = post_to_step_edit_product_document_availability(
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        data={"is_document_available": True},
    )
    response = post_to_step_edit_product_document_availability(
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        data={"is_document_sensitive": False},
    )
    response = post_to_step_edit_product_document_availability(
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_UPLOAD,
        data=product_document,
    )

    assert response.status_code == 302
    assert response.url == material_product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.request_history.pop().json() == [
        {"name": "data sheet", "s3_key": "data sheet", "size": 0, "description": "product data sheet"}
    ]

    assert requests_mock.request_history.pop().json() == {
        "is_document_available": True,
        "no_document_comments": "",
        "is_document_sensitive": False,
    }


@pytest.fixture
def edit_product_sensitivity_url(application, good_on_application):
    return reverse(
        "applications:material_edit_product_document_sensitivity",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )


@pytest.fixture
def post_to_step_edit_product_document_sensitivity(post_to_step_factory, edit_product_sensitivity_url):
    return post_to_step_factory(edit_product_sensitivity_url)


def test_upload_new_product_document_to_replace_existing_one(
    requests_mock,
    post_to_step_edit_product_document_sensitivity,
    product_document,
    material_product_summary_url,
):
    response = post_to_step_edit_product_document_sensitivity(
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        data={"is_document_sensitive": False},
    )
    response = post_to_step_edit_product_document_sensitivity(
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_UPLOAD,
        data=product_document,
    )

    assert response.status_code == 302
    assert response.url == material_product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.request_history.pop().json() == [
        {"name": "data sheet", "s3_key": "data sheet", "size": 0, "description": "product data sheet"}
    ]

    assert requests_mock.request_history.pop().json() == {"is_document_sensitive": False}


def test_edit_product_document_is_sensitive(
    requests_mock, post_to_step_edit_product_document_sensitivity, material_product_summary_url
):
    response = post_to_step_edit_product_document_sensitivity(
        AddGoodMaterialSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        data={"is_document_sensitive": True},
    )

    assert response.status_code == 302
    assert response.url == material_product_summary_url

    # if any document exists then we delete that one
    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.last_request.json() == {"is_document_sensitive": True}


def test_edit_product_document_upload_form(
    authorized_client, requests_mock, application, good_on_application, product_document, material_product_summary_url
):
    url = reverse(
        "applications:material_edit_product_document",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )
    response = authorized_client.post(url, data=product_document)

    assert response.status_code == 302
    assert response.url == material_product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.last_request.json() == [
        {"name": "data sheet", "s3_key": "data sheet", "size": 0, "description": "product data sheet"}
    ]
