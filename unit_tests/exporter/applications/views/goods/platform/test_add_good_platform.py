import pytest

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.applications.views.goods.platform.views.constants import AddGoodCompleteItemSteps

from exporter.goods.forms.common import (
    ProductControlListEntryForm,
    ProductDescriptionForm,
    ProductDocumentAvailabilityForm,
    ProductDocumentSensitivityForm,
    ProductDocumentUploadForm,
    ProductMilitaryUseForm,
    ProductPVGradingDetailsForm,
    ProductPVGradingForm,
    ProductPartNumberForm,
    ProductUsesInformationSecurityForm,
)


@pytest.fixture(autouse=True)
def setup(no_op_storage):
    yield


@pytest.fixture
def new_good_complete_item_url(data_standard_case):
    application_id = data_standard_case["case"]["data"]["id"]
    return reverse(
        "applications:new_good_complete_item",
        kwargs={
            "pk": application_id,
        },
    )


@pytest.fixture
def post_goods_matcher(requests_mock, good_id):
    return requests_mock.post(
        f"/goods/",
        status_code=201,
        json={
            "good": {
                "id": good_id,
                "name": "p1",
            },
        },
    )


@pytest.fixture
def post_good_document_matcher(requests_mock, good_id):
    return requests_mock.post(
        f"/goods/{good_id}/documents/",
        status_code=201,
        json={},
    )


@pytest.fixture
def goto_step(goto_step_factory, new_good_complete_item_url):
    return goto_step_factory(new_good_complete_item_url)


@pytest.fixture
def post_to_step(post_to_step_factory, new_good_complete_item_url):
    return post_to_step_factory(new_good_complete_item_url)


def test_add_good_complete_item_end_to_end(
    authorized_client,
    data_standard_case,
    good_id,
    new_good_complete_item_url,
    mock_application_get,
    control_list_entries,
    pv_gradings,
    post_to_step,
    post_goods_matcher,
    post_good_document_matcher,
):
    authorized_client.get(new_good_complete_item_url)

    response = post_to_step(
        AddGoodCompleteItemSteps.NAME,
        {"name": "product_1"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductControlListEntryForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductPartNumberForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PART_NUMBER,
        {
            "part_number_missing": False,
            "part_number": "abc12345",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductPVGradingForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PV_GRADING,
        {"is_pv_graded": True},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductPVGradingDetailsForm)
    response = post_to_step(
        AddGoodCompleteItemSteps.PV_GRADING_DETAILS,
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

    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductUsesInformationSecurityForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_USES_INFORMATION_SECURITY,
        {"uses_information_security": True, "information_security_details": "secure encrypt"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductDocumentAvailabilityForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": True},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductDocumentSensitivityForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        {"is_document_sensitive": False},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductDocumentUploadForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_UPLOAD,
        {"product_document": SimpleUploadedFile("data sheet", b"This is a detailed spec of this Rifle")},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductMilitaryUseForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_MILITARY_USE,
        {"is_military_use": "yes_modified", "modified_military_use_details": "extra power"},
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "applications:complete_item_product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "item_category": "group1_platform",
        "name": "product_1",
        "is_good_controlled": True,
        "control_list_entries": ["ML1", "ML1a"],
        "is_pv_graded": "yes",
        "pv_grading_details": {
            "prefix": "NATO",
            "grading": "official",
            "suffix": "",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue": "2020-02-20",
        },
        "uses_information_security": True,
        "information_security_details": "secure encrypt",
        "is_document_available": True,
        "no_document_comments": "",
        "is_document_sensitive": False,
        "is_military_use": "yes_modified",
        "modified_military_use_details": "extra power",
        "part_number": "abc12345",
        "no_part_number_comments": "",
    }

    assert post_good_document_matcher.called_once
    assert post_good_document_matcher.last_request.json() == [
        {"name": "data sheet", "s3_key": "data sheet", "size": 0, "description": ""}
    ]


def test_add_good_complete_item_no_pv(
    authorized_client,
    data_standard_case,
    good_id,
    new_good_complete_item_url,
    mock_application_get,
    control_list_entries,
    pv_gradings,
    post_to_step,
    post_goods_matcher,
    post_good_document_matcher,
):
    authorized_client.get(new_good_complete_item_url)

    post_to_step(
        AddGoodCompleteItemSteps.NAME,
        {"name": "product_1"},
    )

    post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": False,
        },
    )
    post_to_step(
        AddGoodCompleteItemSteps.PART_NUMBER,
        {
            "part_number_missing": True,
            "no_part_number_comments": "no part number",
        },
    )
    post_to_step(
        AddGoodCompleteItemSteps.PV_GRADING,
        {"is_pv_graded": False},
    )
    post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_USES_INFORMATION_SECURITY,
        {
            "uses_information_security": False,
        },
    )
    post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": True},
    )
    post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        {"is_document_sensitive": False},
    )
    post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_UPLOAD,
        {"product_document": SimpleUploadedFile("data sheet", b"This is a detailed spec of this Rifle")},
    )
    response = post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_MILITARY_USE,
        {"is_military_use": "no"},
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "applications:complete_item_product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "item_category": "group1_platform",
        "name": "product_1",
        "is_good_controlled": False,
        "control_list_entries": [],
        "is_pv_graded": "no",
        "uses_information_security": False,
        "information_security_details": "",
        "is_document_available": True,
        "is_document_sensitive": False,
        "no_document_comments": "",
        "is_military_use": "no",
        "modified_military_use_details": "",
        "no_part_number_comments": "no part number",
        "part_number": "",
    }


def test_add_good_complete_item_no_product_document(
    authorized_client,
    data_standard_case,
    good_id,
    new_good_complete_item_url,
    mock_application_get,
    control_list_entries,
    pv_gradings,
    post_to_step,
    post_goods_matcher,
):
    authorized_client.get(new_good_complete_item_url)

    response = post_to_step(
        AddGoodCompleteItemSteps.NAME,
        {"name": "product_1"},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductControlListEntryForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": False,
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductPartNumberForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PART_NUMBER,
        {
            "part_number_missing": True,
            "no_part_number_comments": "no part number",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductPVGradingForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PV_GRADING,
        {"is_pv_graded": False},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductUsesInformationSecurityForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_USES_INFORMATION_SECURITY,
        {
            "uses_information_security": False,
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductDocumentAvailabilityForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": False, "no_document_comments": "no document available"},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductDescriptionForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_DESCRIPTION,
        {"product_description": "This is the product description"},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductMilitaryUseForm)

    response = post_to_step(
        AddGoodCompleteItemSteps.PRODUCT_MILITARY_USE,
        {"is_military_use": "no"},
    )
    assert response.status_code == 302
    assert response.url == reverse(
        "applications:complete_item_product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "item_category": "group1_platform",
        "name": "product_1",
        "is_good_controlled": False,
        "control_list_entries": [],
        "is_pv_graded": "no",
        "uses_information_security": False,
        "information_security_details": "",
        "is_document_available": False,
        "no_document_comments": "no document available",
        "is_military_use": "no",
        "modified_military_use_details": "",
        "no_part_number_comments": "no part number",
        "part_number": "",
        "product_description": "This is the product description",
    }
