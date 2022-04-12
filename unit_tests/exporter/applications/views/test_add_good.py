import pytest
import uuid

from unittest.mock import patch

from django.core.files.storage import Storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from core import client
from exporter.core.constants import AddGoodFormSteps
from exporter.goods.forms import (
    AddGoodsQuestionsForm,
    AttachFirearmsDealerCertificateForm,
    FirearmsActConfirmationForm,
    FirearmsCalibreDetailsForm,
    FirearmsCaptureSerialNumbersForm,
    FirearmsNumberOfItemsForm,
    FirearmsReplicaForm,
    FirearmsYearOfManufactureDetailsForm,
    GroupTwoProductTypeForm,
    IdentificationMarkingsForm,
    ProductCategoryForm,
    ProductComponentForm,
    ProductMilitaryUseForm,
    ProductUsesInformationSecurityForm,
    PvDetailsForm,
    RegisteredFirearmsDealerForm,
    SoftwareTechnologyDetailsForm,
)
from lite_content.lite_exporter_frontend.goods import CreateGoodForm, GoodGradingForm


ADD_GOOD_VIEW = "add_good"


@pytest.fixture(autouse=True)
def setup(no_op_storage, settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS = False


@pytest.fixture(autouse=True)
def application_url(requests_mock, data_standard_case):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=app_url, json=data_standard_case["case"])


@pytest.fixture(autouse=True)
def clc_url(requests_mock):
    clc_url = client._build_absolute_uri("/static/control-list-entries/")
    requests_mock.get(url=clc_url, json={"control_list_entries": [{"rating": "ML1"}, {"rating": "ML1a"}]})


@pytest.fixture(autouse=True)
def pv_gradings_url(requests_mock):
    clc_url = client._build_absolute_uri("/static/private-venture-gradings/")
    requests_mock.get(url=clc_url, json={"pv_gradings": [{"test": "test"}, {"test1": "test1"}]})


@pytest.fixture
def url(data_standard_case):
    return reverse("applications:new_good", kwargs={"pk": data_standard_case["case"]["id"]})


def test_add_good_start(url, authorized_client):
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductCategoryForm)
    assert CreateGoodForm.ProductCategory.TITLE.encode("utf-8") in response.content
    assert b"Step 1 of" not in response.content


def test_add_good_product_category(url, authorized_client):
    title = CreateGoodForm.ProductCategory.TITLE.encode("utf-8")
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.PRODUCT_CATEGORY})
    assert isinstance(response.context["form"], ProductCategoryForm)
    assert title in response.content
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.PRODUCT_CATEGORY,
            f"{AddGoodFormSteps.PRODUCT_CATEGORY}-item_category": "group2_firearms",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], GroupTwoProductTypeForm)
    assert title not in response.content


def test_add_good_product_type(url, authorized_client):
    title = CreateGoodForm.FirearmGood.ProductType.TITLE.encode("utf-8")
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE})
    assert isinstance(response.context["form"], GroupTwoProductTypeForm)
    assert title in response.content
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE,
            f"{AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE}-type": "firearms",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsNumberOfItemsForm)
    assert title not in response.content


def test_add_good_number_of_items(url, authorized_client):
    title = b"Number of items"
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS})
    assert isinstance(response.context["form"], FirearmsNumberOfItemsForm)
    assert title in response.content
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS,
            f"{AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS}-number_of_items": "3",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], IdentificationMarkingsForm)
    assert title not in response.content


@pytest.mark.parametrize(
    "data, expected_next_form",
    [
        (
            {
                "serial_numbers_available": "AVAILABLE",
            },
            FirearmsCaptureSerialNumbersForm,
        ),
        (
            {
                "serial_numbers_available": "LATER",
            },
            AddGoodsQuestionsForm,
        ),
        (
            {
                "serial_numbers_available": "NOT_AVAILABLE",
                "no_identification_markings_details": "reasons",
            },
            AddGoodsQuestionsForm,
        ),
    ],
)
def test_add_good_identification_markings(url, authorized_client, data, expected_next_form):
    title = CreateGoodForm.FirearmGood.IdentificationMarkings.TITLE.encode("utf-8")
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.IDENTIFICATION_MARKINGS})
    assert isinstance(response.context["form"], IdentificationMarkingsForm)
    assert title in response.content
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.IDENTIFICATION_MARKINGS,
            **{f"{AddGoodFormSteps.IDENTIFICATION_MARKINGS}-{key}": value for key, value in data.items()},
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], expected_next_form)
    assert title not in response.content


def test_add_good_capture_serial_numbers(url, authorized_client):
    authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.PRODUCT_CATEGORY})
    authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.PRODUCT_CATEGORY,
            f"{AddGoodFormSteps.PRODUCT_CATEGORY}-item_category": "group1_platform",
        },
    )
    authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS})
    authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS,
            f"{AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS}-number_of_items": "3",
        },
    )
    authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.IDENTIFICATION_MARKINGS})
    authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.IDENTIFICATION_MARKINGS,
            f"{AddGoodFormSteps.IDENTIFICATION_MARKINGS}-serial_numbers_available": "AVAILABLE",
        },
    )

    title = b"Enter the serial numbers for this product"
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS})
    assert isinstance(response.context["form"], FirearmsCaptureSerialNumbersForm)
    assert title in response.content
    assert b"serial_numbers_0" in response.content
    assert b"serial_numbers_1" in response.content
    assert b"serial_numbers_2" in response.content

    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS,
            f"{AddGoodFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS}-serial_numbers_0": "abcdef",
            f"{AddGoodFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS}-serial_numbers_1": "abcdef",
            f"{AddGoodFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS}-serial_numbers_2": "abcdef",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductMilitaryUseForm)
    assert title not in response.content


def test_add_good_product_military_use(url, authorized_client):
    authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.PRODUCT_CATEGORY})
    authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.PRODUCT_CATEGORY,
            f"{AddGoodFormSteps.PRODUCT_CATEGORY}-item_category": "group1_device",
        },
    )

    title = CreateGoodForm.MilitaryUse.TITLE.encode("utf-8")
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.PRODUCT_MILITARY_USE})
    assert isinstance(response.context["form"], ProductMilitaryUseForm)
    assert title in response.content
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.PRODUCT_MILITARY_USE,
            f"{AddGoodFormSteps.PRODUCT_MILITARY_USE}-is_military_use": "yes_designed",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductUsesInformationSecurityForm)
    assert title not in response.content


def test_add_good_product_uses_information_security(url, authorized_client):
    authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.PRODUCT_CATEGORY})
    authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.PRODUCT_CATEGORY,
            f"{AddGoodFormSteps.PRODUCT_CATEGORY}-item_category": "group1_device",
        },
    )

    title = CreateGoodForm.ProductInformationSecurity.TITLE.encode("utf-8")
    response = authorized_client.post(
        url, data={"wizard_goto_step": AddGoodFormSteps.PRODUCT_USES_INFORMATION_SECURITY}
    )
    assert title in response.content
    assert isinstance(response.context["form"], ProductUsesInformationSecurityForm)
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.PRODUCT_USES_INFORMATION_SECURITY,
            f"{AddGoodFormSteps.PRODUCT_USES_INFORMATION_SECURITY}-uses_information_security": "True",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], AddGoodsQuestionsForm)
    assert title not in response.content


def test_add_good_goods_questions(url, authorized_client):
    title = CreateGoodForm.TITLE_APPLICATION.encode("utf-8")
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.ADD_GOODS_QUESTIONS})
    assert title in response.content
    assert isinstance(response.context["form"], AddGoodsQuestionsForm)
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.ADD_GOODS_QUESTIONS,
            f"{AddGoodFormSteps.ADD_GOODS_QUESTIONS}-name": "test",
            f"{AddGoodFormSteps.ADD_GOODS_QUESTIONS}-is_good_controlled": "True",
            f"{AddGoodFormSteps.ADD_GOODS_QUESTIONS}-control_list_entries": "ML1a",
            f"{AddGoodFormSteps.ADD_GOODS_QUESTIONS}-is_pv_graded": "yes",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], PvDetailsForm)
    assert title not in response.content


def test_add_good_pv_details(url, authorized_client):
    authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.ADD_GOODS_QUESTIONS})
    authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.ADD_GOODS_QUESTIONS,
            f"{AddGoodFormSteps.ADD_GOODS_QUESTIONS}-name": "test",
            f"{AddGoodFormSteps.ADD_GOODS_QUESTIONS}-is_good_controlled": "True",
            f"{AddGoodFormSteps.ADD_GOODS_QUESTIONS}-control_list_entries": "ML1a",
            f"{AddGoodFormSteps.ADD_GOODS_QUESTIONS}-is_pv_graded": "yes",
        },
    )

    title = GoodGradingForm.TITLE.encode("utf-8")
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.PV_DETAILS})
    assert title in response.content
    assert isinstance(response.context["form"], PvDetailsForm)
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.PV_DETAILS,
            f"{AddGoodFormSteps.PV_DETAILS}-grading": "test",
            f"{AddGoodFormSteps.PV_DETAILS}-issuing_authority": "test_authority",
            f"{AddGoodFormSteps.PV_DETAILS}-reference": "test_ref",
            f"{AddGoodFormSteps.PV_DETAILS}-date_of_issue_0": "1",
            f"{AddGoodFormSteps.PV_DETAILS}-date_of_issue_1": "1",
            f"{AddGoodFormSteps.PV_DETAILS}-date_of_issue_2": "2020",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsYearOfManufactureDetailsForm)
    assert title not in response.content


def test_add_good_firearms_year_of_manufacture(url, authorized_client):
    title = b"What is the year of manufacture of the firearm?"
    response = authorized_client.post(
        url, data={"wizard_goto_step": AddGoodFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS}
    )
    assert title in response.content
    assert isinstance(response.context["form"], FirearmsYearOfManufactureDetailsForm)
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS,
            f"{AddGoodFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS}-year_of_manufacture": "2000",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsReplicaForm)
    assert title not in response.content


def test_add_good_firearms_replica(url, authorized_client):
    title = CreateGoodForm.FirearmGood.FirearmsReplica.TITLE.encode("utf-8")
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.FIREARMS_REPLICA})
    assert title in response.content
    assert isinstance(response.context["form"], FirearmsReplicaForm)
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_REPLICA,
            f"{AddGoodFormSteps.FIREARMS_REPLICA}-is_replica": "False",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsCalibreDetailsForm)
    assert title not in response.content


def test_add_good_firearms_calibre(url, authorized_client):
    title = b"What is the calibre of the product?"
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.FIREARMS_CALIBRE_DETAILS})
    assert title in response.content
    assert isinstance(response.context["form"], FirearmsCalibreDetailsForm)
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_CALIBRE_DETAILS,
            f"{AddGoodFormSteps.FIREARMS_CALIBRE_DETAILS}-calibre": "22",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], RegisteredFirearmsDealerForm)
    assert title not in response.content


def test_add_good_registered_firearms_dealer(url, authorized_client):
    title = b"Are you a registered firearms dealer?"
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.REGISTERED_FIREARMS_DEALER})
    assert title in response.content
    assert isinstance(response.context["form"], RegisteredFirearmsDealerForm)
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.REGISTERED_FIREARMS_DEALER,
            f"{AddGoodFormSteps.REGISTERED_FIREARMS_DEALER}-is_registered_firearm_dealer": "True",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], AttachFirearmsDealerCertificateForm)
    assert title not in response.content


def test_add_good_attach_firearm_dealer_certificate(url, authorized_client):
    authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.REGISTERED_FIREARMS_DEALER})
    authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.REGISTERED_FIREARMS_DEALER,
            f"{AddGoodFormSteps.REGISTERED_FIREARMS_DEALER}-is_registered_firearm_dealer": "True",
        },
    )

    title = b"Attach your registered firearms dealer certificate"
    response = authorized_client.post(
        url, data={"wizard_goto_step": AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE}
    )
    assert title in response.content
    assert isinstance(response.context["form"], AttachFirearmsDealerCertificateForm)
    certificate = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE,
            f"{AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE}-file": certificate,
            f"{AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE}-reference_code": "12345",
            f"{AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE}-expiry_date_0": "1",
            f"{AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE}-expiry_date_1": "1",
            f"{AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE}-expiry_date_2": "2030",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsActConfirmationForm)
    assert title not in response.content


def test_add_good_firearms_act_confirmation(url, authorized_client):
    authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.REGISTERED_FIREARMS_DEALER})
    authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.REGISTERED_FIREARMS_DEALER,
            f"{AddGoodFormSteps.REGISTERED_FIREARMS_DEALER}-is_registered_firearm_dealer": "True",
        },
    )

    title = b"Is the product covered by section 5 of the Firearms Act 1968?"
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.FIREARMS_ACT_CONFIRMATION})
    assert title in response.content
    assert isinstance(response.context["form"], FirearmsActConfirmationForm)
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_ACT_CONFIRMATION,
            f"{AddGoodFormSteps.FIREARMS_ACT_CONFIRMATION}-is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], SoftwareTechnologyDetailsForm)
    assert title not in response.content


def test_add_good_software_technology_details(url, authorized_client):
    authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE})
    authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE,
            f"{AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE}-type": "software_related_to_firearms",
        },
    )

    title = (CreateGoodForm.TechnologySoftware.TITLE + "software").encode("utf-8")
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.SOFTWARE_TECHNOLOGY_DETAILS})
    assert title in response.content
    assert isinstance(response.context["form"], SoftwareTechnologyDetailsForm)
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.SOFTWARE_TECHNOLOGY_DETAILS,
            f"{AddGoodFormSteps.SOFTWARE_TECHNOLOGY_DETAILS}-software_or_technology_details": "Some purpose",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductMilitaryUseForm)
    assert title not in response.content


def test_add_good_product_component(url, authorized_client):
    title = CreateGoodForm.ProductComponent.TITLE.encode("utf-8")
    response = authorized_client.post(url, data={"wizard_goto_step": AddGoodFormSteps.PRODUCT_COMPONENT})
    assert title in response.content
    assert isinstance(response.context["form"], ProductComponentForm)
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.PRODUCT_COMPONENT,
            f"{AddGoodFormSteps.PRODUCT_COMPONENT}-is_component": "yes_designed",
            f"{AddGoodFormSteps.PRODUCT_COMPONENT}-designed_details": "Test details",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], ProductUsesInformationSecurityForm)
    assert title not in response.content


def test_add_good_api_submission(url, authorized_client, requests_mock, data_standard_case):
    # The final API submission we expect
    requests_mock.post("/goods/", status_code=201, json={})
    # The request to post the rfd certificate
    requests_mock.post(f"/applications/{data_standard_case['case']['id']}/documents/", status_code=201, json={})

    resp = _submit_good(url, authorized_client)

    assert resp.status_code == 302
    assert resp.url == f"/applications/{data_standard_case['case']['id']}/goods/add-firearms-certificate/"

    # Assert rfd certificate data
    rfd_cert_data = requests_mock.request_history.pop().json()
    assert rfd_cert_data == {
        "document_on_organisation": {
            "document_type": "rfd-certificate",
            "expiry_date": "2030-01-01",
            "reference_code": "12345",
        },
        "name": f'{rfd_cert_data["name"]}',
        "s3_key": f'{rfd_cert_data["s3_key"]}',
        "size": 0,
    }

    # Assert good submission data
    good_data = requests_mock.request_history.pop().json()
    assert good_data == {
        "item_category": "group2_firearms",
        "type": "firearms",
        "product_type_step": True,
        "number_of_items": 3,
        "number_of_items_step": True,
        "identification_markings_step": True,
        "serial_number_input_0": "abcdef",
        "serial_number_input_1": "ghijkl",
        "serial_number_input_2": "mnopqr",
        "serial_numbers_available": "AVAILABLE",
        "capture_serial_numbers_step": True,
        "name": "test",
        "description": "",
        "part_number": "",
        "is_good_controlled": "True",
        "control_list_entries": ["ML1a"],
        "is_pv_graded": "yes",
        "prefix": "",
        "grading": "test",
        "suffix": "",
        "custom_grading": "",
        "issuing_authority": "test_authority",
        "reference": "test_ref",
        "date_of_issue": "2020-01-01",
        "date_of_issueday": "1",
        "date_of_issuemonth": "1",
        "date_of_issueyear": "2020",
        "firearm_year_of_manufacture_step": True,
        "is_replica": "False",
        "is_replica_step": True,
        "firearm_calibre_step": True,
        "is_registered_firearm_dealer": "True",
        "reference_code": "12345",
        "expiry_date": "2030-01-01",
        "expiry_date_day": "1",
        "expiry_date_month": "1",
        "expiry_date_year": "2030",
        "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        "firearms_act_section": "firearms_act_section5",
        "section_certificate_step": True,
        "pv_grading_details": {
            "grading": "test",
            "custom_grading": "",
            "prefix": "",
            "suffix": "",
            "issuing_authority": "test_authority",
            "reference": "test_ref",
            "date_of_issue": "2020-01-01",
        },
        "firearm_details": {
            "type": "firearms",
            "number_of_items": 3,
            "serial_numbers_available": "AVAILABLE",
            "no_identification_markings_details": "",
            "serial_numbers": ["abcdef", "ghijkl", "mnopqr"],
            "year_of_manufacture": "2000",
            "is_replica": "False",
            "replica_description": "",
            "calibre": "22",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section5",
        },
    }


def test_add_good_api_submission_no_firearms_certificate(url, authorized_client, requests_mock, data_standard_case):
    good_id = str(uuid.uuid4())
    requests_mock.post("/goods/", status_code=201, json={"good": {"id": good_id}})
    # The request to post the rfd certificate
    requests_mock.post(f"/applications/{data_standard_case['case']['id']}/documents/", status_code=201, json={})

    resp = _submit_good(url, authorized_client, firearms_act="No")

    assert resp.status_code == 302
    assert resp.url == f"/applications/{data_standard_case['case']['id']}/goods/add-new/{good_id}/good-detail-summary/"


def test_add_good_api_submission_no_rfd_certificate(url, authorized_client, requests_mock, data_standard_case):
    good_id = str(uuid.uuid4())
    # Note that there is *not* a separate API call to post the rfd certificate
    requests_mock.post("/goods/", status_code=201, json={"good": {"id": good_id}})

    resp = _submit_good(url, authorized_client, is_rfd=False, firearms_act="No")

    assert resp.status_code == 302
    assert resp.url == f"/applications/{data_standard_case['case']['id']}/goods/add-new/{good_id}/good-detail-summary/"


def _submit_good(url, authorized_client, is_rfd=True, firearms_act="Yes"):
    # Enter the wizard at product category
    response = authorized_client.get(url)
    assert not response.context["form"].errors

    # Post product category, return product type
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.PRODUCT_CATEGORY,
            f"{AddGoodFormSteps.PRODUCT_CATEGORY}-item_category": "group2_firearms",
        },
    )
    assert not response.context["form"].errors

    # Post product type, return number of items
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE,
            f"{AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE}-type": "firearms",
        },
    )
    assert not response.context["form"].errors

    # Post number of items, return has identification markings
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS,
            f"{AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS}-number_of_items": "3",
        },
    )
    assert not response.context["form"].errors

    # Post has identification markings, return capture serial numbers
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.IDENTIFICATION_MARKINGS,
            f"{AddGoodFormSteps.IDENTIFICATION_MARKINGS}-serial_numbers_available": "AVAILABLE",
        },
    )
    assert not response.context["form"].errors

    # Post capture serial numbers, return goods questions
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS,
            f"{AddGoodFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS}-serial_numbers_0": "abcdef",
            f"{AddGoodFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS}-serial_numbers_1": "ghijkl",
            f"{AddGoodFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS}-serial_numbers_2": "mnopqr",
        },
    )
    assert not response.context["form"].errors

    # Post goods questions, return pv details
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.ADD_GOODS_QUESTIONS,
            f"{AddGoodFormSteps.ADD_GOODS_QUESTIONS}-name": "test",
            f"{AddGoodFormSteps.ADD_GOODS_QUESTIONS}-is_good_controlled": "True",
            f"{AddGoodFormSteps.ADD_GOODS_QUESTIONS}-control_list_entries": "ML1a",
            f"{AddGoodFormSteps.ADD_GOODS_QUESTIONS}-is_pv_graded": "yes",
        },
    )
    assert not response.context["form"].errors

    # Post pv details, return year of manufacture
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.PV_DETAILS,
            f"{AddGoodFormSteps.PV_DETAILS}-grading": "test",
            f"{AddGoodFormSteps.PV_DETAILS}-issuing_authority": "test_authority",
            f"{AddGoodFormSteps.PV_DETAILS}-reference": "test_ref",
            f"{AddGoodFormSteps.PV_DETAILS}-date_of_issue_0": "1",
            f"{AddGoodFormSteps.PV_DETAILS}-date_of_issue_1": "1",
            f"{AddGoodFormSteps.PV_DETAILS}-date_of_issue_2": "2020",
        },
    )
    assert not response.context["form"].errors

    # Post year of manufacture, return is replica
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS,
            f"{AddGoodFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS}-year_of_manufacture": "2000",
        },
    )
    assert not response.context["form"].errors

    # Post is replica, return calibre
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_REPLICA,
            f"{AddGoodFormSteps.FIREARMS_REPLICA}-is_replica": "False",
        },
    )
    assert not response.context["form"].errors

    # Post calibre, return registered firearms dealer
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_CALIBRE_DETAILS,
            f"{AddGoodFormSteps.FIREARMS_CALIBRE_DETAILS}-calibre": "22",
        },
    )
    assert not response.context["form"].errors

    # Post registered firearms dealer, return attach dealer certificate
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.REGISTERED_FIREARMS_DEALER,
            f"{AddGoodFormSteps.REGISTERED_FIREARMS_DEALER}-is_registered_firearm_dealer": str(is_rfd),
        },
    )
    assert not response.context["form"].errors

    if is_rfd:
        # Post attach dealer certificate, return firearms act confirmation
        certificate = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        response = authorized_client.post(
            url,
            data={
                f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE,
                f"{AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE}-file": certificate,
                f"{AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE}-reference_code": "12345",
                f"{AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE}-expiry_date_0": "1",
                f"{AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE}-expiry_date_1": "1",
                f"{AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE}-expiry_date_2": "2030",
            },
        )
        assert not response.context["form"].errors

    # Post firearms act confirmation, make final submission
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_ACT_CONFIRMATION,
            f"{AddGoodFormSteps.FIREARMS_ACT_CONFIRMATION}-is_covered_by_firearm_act_section_one_two_or_five": firearms_act,
        },
    )

    return response
