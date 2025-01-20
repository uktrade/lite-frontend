import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from exporter.applications.views.goods.component.views.constants import AddGoodComponentSteps
from exporter.goods.forms.common import ProductDescriptionForm
from exporter.goods.forms.goods import ProductComponentDetailsForm


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
        "product_document": SimpleUploadedFile("data_sheet.pdf", b"This is a detailed spec of this Rifle"),
        "description": "product data sheet",
    }


@pytest.mark.parametrize(
    "url_name, form_data, expected",
    (
        (
            "component_accessory_edit_name",
            {"name": "new good"},
            {"name": "new good"},
        ),
        (
            "component_accessory_edit_control_list_entries",
            {"is_good_controlled": False},
            {"is_good_controlled": False, "control_list_entries": []},
        ),
        (
            "component_accessory_edit_control_list_entries",
            {"is_good_controlled": True, "control_list_entries": ["ML1a", "ML22b"]},
            {"is_good_controlled": True, "control_list_entries": ["ML1a", "ML22b"]},
        ),
        (
            "component_accessory_edit_uses_information_security",
            {
                "uses_information_security": True,
                "information_security_details": "Uses information security details",
            },
            {
                "uses_information_security": True,
                "information_security_details": "Uses information security details",
            },
        ),
        (
            "component_accessory_edit_part_number",
            {
                "part_number": "12345",
            },
            {
                "no_part_number_comments": "",
                "part_number": "12345",
            },
        ),
        (
            "component_accessory_edit_part_number",
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
            "component_accessory_edit_military_use",
            {
                "is_military_use": "yes_designed",
            },
            {
                "is_military_use": "yes_designed",
                "modified_military_use_details": "",
            },
        ),
        (
            "component_accessory_edit_military_use",
            {"is_military_use": "yes_modified", "modified_military_use_details": "Modified details"},
            {
                "is_military_use": "yes_modified",
                "modified_military_use_details": "Modified details",
            },
        ),
        (
            "component_accessory_edit_product_description",
            {"product_description": "Product description"},
            {"product_description": "Product description"},
        ),
    ),
)
def test_edit_component_accessory_post(
    authorized_client,
    requests_mock,
    application,
    good_on_application,
    url_name,
    form_data,
    expected,
    component_accessory_product_summary_url,
):
    url = reverse(f"applications:{url_name}", kwargs={"pk": application["id"], "good_pk": good_on_application["id"]})

    response = authorized_client.post(
        url,
        data=form_data,
    )
    assert response.status_code == 302
    assert response.url == component_accessory_product_summary_url
    assert requests_mock.last_request.json() == expected


@pytest.mark.parametrize(
    "url_name,good_on_application_data,initial",
    (
        (
            "component_accessory_edit_name",
            {},
            {"name": "p1"},
        ),
        (
            "component_accessory_edit_component_details",
            {"is_component": {"key": "yes_modified"}, "component_accessory_details": "modified"},
            {"is_component": True},
        ),
        (
            "component_accessory_edit_component_details",
            {"is_component": {"key": "no"}},
            {"is_component": False},
        ),
        (
            "component_accessory_edit_control_list_entries",
            {},
            {"control_list_entries": ["ML1a", "ML22b"], "is_good_controlled": "True"},
        ),
        (
            "component_accessory_edit_uses_information_security",
            {},
            {"uses_information_security": False},
        ),
        (
            "component_accessory_edit_uses_information_security",
            {"uses_information_security": True, "information_security_details": "Details"},
            {"uses_information_security": True, "information_security_details": "Details"},
        ),
        (
            "component_accessory_edit_part_number",
            {},
            {"part_number": "44"},
        ),
        (
            "component_accessory_edit_part_number",
            {"no_part_number_comments": "No part number"},
            {"no_part_number_comments": "No part number", "part_number_missing": True},
        ),
        (
            "component_accessory_edit_military_use",
            {
                "is_military_use": {"key": "yes_designed"},
            },
            {
                "is_military_use": "yes_designed",
                "modified_military_use_details": None,
            },
        ),
        (
            "component_accessory_edit_military_use",
            {"is_military_use": {"key": "yes_modified"}, "modified_military_use_details": "Modified details"},
            {
                "is_military_use": "yes_modified",
                "modified_military_use_details": "Modified details",
            },
        ),
        (
            "component_accessory_edit_product_description",
            {"product_description": "Product description"},
            {"product_description": "Product description"},
        ),
    ),
)
def test_edit_component_accessory_initial(
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
        "applications:component_accessory_edit_pv_grading",
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
    component_accessory_product_summary_url,
):
    response = goto_step_pv_grading(AddGoodComponentSteps.PV_GRADING)
    assert response.status_code == 200

    response = post_to_step_pv_grading(
        AddGoodComponentSteps.PV_GRADING,
        {"is_pv_graded": True},
    )

    assert response.status_code == 200

    response = post_to_step_pv_grading(
        AddGoodComponentSteps.PV_GRADING_DETAILS,
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
    assert response.url == component_accessory_product_summary_url
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
    component_accessory_product_summary_url,
):
    url = reverse(
        "applications:component_accessory_edit_pv_grading_details",
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
    assert response.url == component_accessory_product_summary_url
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


@pytest.fixture(autouse=True)
def edit_component_accessory_details_url(application, good_on_application):
    return reverse(
        "applications:component_accessory_edit_component_details",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )


@pytest.fixture
def goto_step_component_accessory_details(goto_step_factory, edit_component_accessory_details_url):
    return goto_step_factory(edit_component_accessory_details_url)


@pytest.fixture
def post_to_step_component_accessory_details(post_to_step_factory, edit_component_accessory_details_url):
    return post_to_step_factory(edit_component_accessory_details_url)


def test_edit_component_accessory_details(
    requests_mock,
    goto_step_component_accessory_details,
    post_to_step_component_accessory_details,
    component_accessory_product_summary_url,
):
    response = goto_step_component_accessory_details(AddGoodComponentSteps.IS_COMPONENT)
    assert response.status_code == 200

    response = post_to_step_component_accessory_details(
        AddGoodComponentSteps.IS_COMPONENT,
        {"is_component": True},
    )

    assert response.status_code == 200

    assert isinstance(response.context["form"], ProductComponentDetailsForm)

    response = post_to_step_component_accessory_details(
        AddGoodComponentSteps.COMPONENT_DETAILS,
        {
            "component_type": "yes_modified",
            "modified_details": "modified component",
        },
    )

    assert response.status_code == 302
    assert response.url == component_accessory_product_summary_url
    assert requests_mock.last_request.json() == {
        "is_component": "yes_modified",
        "modified_details": "modified component",
    }


@pytest.fixture
def edit_product_availability_url(application, good_on_application):
    return reverse(
        "applications:component_accessory_edit_product_document_availability",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )


@pytest.fixture
def post_to_step_edit_product_document_availability(post_to_step_factory, edit_product_availability_url):
    return post_to_step_factory(edit_product_availability_url)


def test_edit_product_document_availability_select_not_available(
    requests_mock, post_to_step_edit_product_document_availability, component_accessory_product_summary_url
):
    response = post_to_step_edit_product_document_availability(
        AddGoodComponentSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        data={"is_document_available": False, "no_document_comments": "Product not manufactured yet"},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductDescriptionForm)

    response = post_to_step_edit_product_document_availability(
        AddGoodComponentSteps.PRODUCT_DESCRIPTION,
        data={"product_description": "This is the product description"},
    )

    assert response.status_code == 302
    assert response.url == component_accessory_product_summary_url

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
    component_accessory_product_summary_url,
):
    response = post_to_step_edit_product_document_availability(
        AddGoodComponentSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        data={"is_document_available": True},
    )
    response = post_to_step_edit_product_document_availability(
        AddGoodComponentSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        data={"is_document_sensitive": True},
    )

    assert response.status_code == 302
    assert response.url == component_accessory_product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.request_history.pop().json() == {
        "is_document_available": True,
        "no_document_comments": "",
        "is_document_sensitive": True,
    }


def test_edit_product_document_availability_upload_new_document(
    requests_mock,
    post_to_step_edit_product_document_availability,
    product_document,
    component_accessory_product_summary_url,
):
    response = post_to_step_edit_product_document_availability(
        AddGoodComponentSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        data={"is_document_available": True},
    )
    response = post_to_step_edit_product_document_availability(
        AddGoodComponentSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        data={"is_document_sensitive": False},
    )
    response = post_to_step_edit_product_document_availability(
        AddGoodComponentSteps.PRODUCT_DOCUMENT_UPLOAD,
        data=product_document,
    )

    assert response.status_code == 302
    assert response.url == component_accessory_product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.request_history.pop().json() == [
        {"name": "data_sheet.pdf", "s3_key": "data_sheet.pdf", "size": 0, "description": "product data sheet"}
    ]

    assert requests_mock.request_history.pop().json() == {
        "is_document_available": True,
        "no_document_comments": "",
        "is_document_sensitive": False,
    }


@pytest.fixture
def edit_product_sensitivity_url(application, good_on_application):
    return reverse(
        "applications:component_accessory_edit_product_document_sensitivity",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )


@pytest.fixture
def post_to_step_edit_product_document_sensitivity(post_to_step_factory, edit_product_sensitivity_url):
    return post_to_step_factory(edit_product_sensitivity_url)


def test_upload_new_product_document_to_replace_existing_one(
    requests_mock,
    post_to_step_edit_product_document_sensitivity,
    product_document,
    component_accessory_product_summary_url,
):
    response = post_to_step_edit_product_document_sensitivity(
        AddGoodComponentSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        data={"is_document_sensitive": False},
    )
    response = post_to_step_edit_product_document_sensitivity(
        AddGoodComponentSteps.PRODUCT_DOCUMENT_UPLOAD,
        data=product_document,
    )

    assert response.status_code == 302
    assert response.url == component_accessory_product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.request_history.pop().json() == [
        {"name": "data_sheet.pdf", "s3_key": "data_sheet.pdf", "size": 0, "description": "product data sheet"}
    ]

    assert requests_mock.request_history.pop().json() == {"is_document_sensitive": False}


def test_edit_product_document_is_sensitive(
    requests_mock, post_to_step_edit_product_document_sensitivity, component_accessory_product_summary_url
):
    response = post_to_step_edit_product_document_sensitivity(
        AddGoodComponentSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        data={"is_document_sensitive": True},
    )

    assert response.status_code == 302
    assert response.url == component_accessory_product_summary_url

    # if any document exists then we delete that one
    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.last_request.json() == {"is_document_sensitive": True}


def test_edit_product_document_upload_form(
    authorized_client,
    requests_mock,
    application,
    good_on_application,
    product_document,
    component_accessory_product_summary_url,
):
    url = reverse(
        "applications:component_accessory_edit_product_document",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )
    response = authorized_client.post(url, data=product_document)

    assert response.status_code == 302
    assert response.url == component_accessory_product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.last_request.json() == [
        {"name": "data_sheet.pdf", "s3_key": "data_sheet.pdf", "size": 0, "description": "product data sheet"}
    ]
