import pytest
import uuid

from django.core.files.uploadedfile import SimpleUploadedFile
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
def setup(no_op_storage):
    yield


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


@pytest.fixture
def goods_url(data_standard_case):
    return reverse("applications:goods", kwargs={"pk": data_standard_case["case"]["id"]})


@pytest.fixture
def is_good_firearm_url(data_standard_case):
    return reverse("applications:is_good_firearm", kwargs={"pk": data_standard_case["case"]["id"]})


@pytest.fixture
def add_new_firearm_url(data_standard_case):
    return reverse("applications:new_good_firearm", kwargs={"pk": data_standard_case["case"]["id"]})


def test_add_good_start(url, authorized_client, goods_url):
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], GroupTwoProductTypeForm)
    assert CreateGoodForm.FirearmGood.ProductType.TITLE.encode("utf-8") in response.content
    assert response.context["back_link_url"] == goods_url


def test_add_good_firearm_redirects_to_firearm_wizard(url, authorized_client, add_new_firearm_url):
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
    assert response.status_code == 302
    assert response.url == add_new_firearm_url


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
    label = b"Upload a DOCX, DOC, PDF, PNG, JPEG or ODT file."
    response = authorized_client.post(
        url, data={"wizard_goto_step": AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE}
    )
    assert title in response.content
    assert label in response.content
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
    good_id = str(uuid.uuid4())

    # The final API submission we expect
    mock_goods_post = requests_mock.post("/goods/", status_code=201, json={"good": {"id": good_id}})

    response = authorized_client.get(url)
    assert not response.context["form"].errors

    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE,
            f"{AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE}-type": "ammunition",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsNumberOfItemsForm)
    assert not response.context["form"].errors

    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS,
            f"{AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS}-number_of_items": "3",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], IdentificationMarkingsForm)
    assert not response.context["form"].errors

    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.IDENTIFICATION_MARKINGS,
            f"{AddGoodFormSteps.IDENTIFICATION_MARKINGS}-serial_numbers_available": "LATER",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], AddGoodsQuestionsForm)
    assert not response.context["form"].errors

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
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsCalibreDetailsForm)
    assert not response.context["form"].errors

    # Post calibre, return registered firearms dealer
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_CALIBRE_DETAILS,
            f"{AddGoodFormSteps.FIREARMS_CALIBRE_DETAILS}-calibre": "22",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], RegisteredFirearmsDealerForm)
    assert not response.context["form"].errors

    # Post registered firearms dealer, return attach dealer certificate
    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.REGISTERED_FIREARMS_DEALER,
            f"{AddGoodFormSteps.REGISTERED_FIREARMS_DEALER}-is_registered_firearm_dealer": "False",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsActConfirmationForm)
    assert not response.context["form"].errors

    response = authorized_client.post(
        url,
        data={
            f"{ADD_GOOD_VIEW}-current_step": AddGoodFormSteps.FIREARMS_ACT_CONFIRMATION,
            f"{AddGoodFormSteps.FIREARMS_ACT_CONFIRMATION}-is_covered_by_firearm_act_section_one_two_or_five": "No",
        },
    )
    assert response.status_code == 302
    assert response.url == reverse(
        "applications:add_good_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )

    # Assert good submission data
    good_data = mock_goods_post.last_request.json()
    assert good_data == {
        "control_list_entries": ["ML1a"],
        "custom_grading": "",
        "date_of_issue": "2020-01-01",
        "date_of_issueday": "1",
        "date_of_issuemonth": "1",
        "date_of_issueyear": "2020",
        "description": "",
        "firearm_calibre_step": True,
        "firearm_details": {
            "calibre": "22",
            "firearms_act_section": "",
            "is_covered_by_firearm_act_section_one_two_or_five": "No",
            "no_identification_markings_details": "",
            "number_of_items": 3,
            "serial_numbers": [],
            "serial_numbers_available": "LATER",
            "type": "ammunition",
            "year_of_manufacture": 0,
        },
        "firearms_act_section": "",
        "grading": "test",
        "identification_markings_step": True,
        "is_covered_by_firearm_act_section_one_two_or_five": "No",
        "is_good_controlled": "True",
        "is_pv_graded": "yes",
        "is_registered_firearm_dealer": "False",
        "issuing_authority": "test_authority",
        "item_category": "group2_firearms",
        "name": "test",
        "number_of_items": 3,
        "number_of_items_step": True,
        "part_number": "",
        "prefix": "",
        "product_type_step": True,
        "pv_grading_details": {
            "custom_grading": "",
            "date_of_issue": "2020-01-01",
            "grading": "test",
            "issuing_authority": "test_authority",
            "prefix": "",
            "reference": "test_ref",
            "suffix": "",
        },
        "reference": "test_ref",
        "section_certificate_step": True,
        "serial_numbers_available": "LATER",
        "suffix": "",
        "type": "ammunition",
    }
