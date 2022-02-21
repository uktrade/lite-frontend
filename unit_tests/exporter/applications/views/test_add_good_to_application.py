import datetime
import pytest
import uuid

from pytest_django.asserts import assertNotContains
from unittest.mock import patch

from django.core.files.storage import Storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from core import client
from exporter.applications.views.goods import AddGoodToApplicationFormSteps
from exporter.goods.forms import (
    AttachFirearmsDealerCertificateForm,
    FirearmsActConfirmationForm,
    FirearmsCaptureSerialNumbersForm,
    FirearmsNumberOfItemsForm,
    FirearmsUnitQuantityValueForm,
    FirearmsYearOfManufactureDetailsForm,
    IdentificationMarkingsForm,
    RegisteredFirearmsDealerForm,
)


ADD_GOOD_TO_APPLICATION_VIEW = "add_good_to_application2"


@pytest.fixture(autouse=True)
def setup():
    class NoOpStorage(Storage):
        def save(self, name, content, max_length=None):
            return name

        def open(self, name, mode="rb"):
            return None

        def delete(self, name):
            pass

    with override_settings(FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS=False), patch(
        "exporter.applications.views.goods.AddGoodToApplication2.file_storage", new=NoOpStorage()
    ):
        yield


@pytest.fixture
def case():
    return {
        "id": str(uuid.uuid4()),
        "case": {"id": str(uuid.uuid4()),},
        "organisation": {
            "documents": [
                {
                    "document_type": "section-five-certificate",
                    "is_expired": False,
                    "expiry_date": (datetime.date.today() + datetime.timedelta(weeks=1)).strftime("%d %B %Y"),
                    "reference_code": "12345",
                },
            ],
        },
    }


@pytest.fixture
def good():
    return {
        "good": {
            "id": str(uuid.uuid4()),
            "name": "good name",
            "description": "good description",
            "part_number": "12345",
            "firearm_details": {
                "type": {"key": "firearms",},
                "section_certificate_missing": "certification missing",
                "section_certificate_missing_reason": "missing reason",
            },
            "item_category": {"key": "group2_firearms",},
            "control_list_entries": [],
        },
    }


@pytest.fixture
def preexisting_url(case, good):
    url = reverse(
        "applications:add_good_to_application2", kwargs={"pk": case["case"]["id"], "good_pk": good["good"]["id"]},
    )

    return f"{url}?preexisting=True"


@pytest.fixture(autouse=True)
def mock_good_request(requests_mock, good):
    good_pk = good["good"]["id"]
    path = f"/goods/{good_pk}/?pk={good_pk}&full_detail=False"
    app_url = client._build_absolute_uri(path)
    return requests_mock.get(url=app_url, json=good)


@pytest.fixture(autouse=True)
def mock_application_request(requests_mock, case):
    case_pk = case["case"]["id"]
    path = f"/applications/{case_pk}/"
    app_url = client._build_absolute_uri(path)
    return requests_mock.get(url=app_url, json=case)


@pytest.fixture()
def goto_step_preexisting(preexisting_url, authorized_client):
    def _goto_step(step_name):
        return authorized_client.post(preexisting_url, data={"wizard_goto_step": step_name,},)

    return _goto_step


@pytest.fixture()
def post_to_step_preexisting(preexisting_url, authorized_client):
    def _post_to_step(step_name, data):
        return authorized_client.post(
            preexisting_url,
            data={
                f"{ADD_GOOD_TO_APPLICATION_VIEW}-current_step": step_name,
                **{f"{step_name}-{key}": value for key, value in data.items()},
            },
        )

    return _post_to_step


def test_add_good_to_application_preexisting_start(preexisting_url, authorized_client):
    response = authorized_client.get(preexisting_url)

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsNumberOfItemsForm)
    assertNotContains(response, "Step 1 of", html=True)


def test_add_number_of_items_preexisting(goto_step_preexisting, post_to_step_preexisting):
    response = goto_step_preexisting(AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS)
    assert isinstance(response.context["form"], FirearmsNumberOfItemsForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS, {"number_of_items": "3"},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], IdentificationMarkingsForm)


def test_identification_markings_preexisting(goto_step_preexisting, post_to_step_preexisting):
    response = goto_step_preexisting(AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS)
    assert isinstance(response.context["form"], IdentificationMarkingsForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS, {"has_identification_markings": True},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsCaptureSerialNumbersForm)


def test_firearms_capture_serial_numbers_preexisting(goto_step_preexisting, post_to_step_preexisting):
    goto_step_preexisting(AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS)
    post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS, {"number_of_items": "3"},
    )

    goto_step_preexisting(AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS)
    post_to_step_preexisting(
        AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS, {"has_identification_markings": True},
    )

    response = goto_step_preexisting(AddGoodToApplicationFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS)
    assert isinstance(response.context["form"], FirearmsCaptureSerialNumbersForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS,
        {"serial_number_input_0": "abcdef", "serial_number_input_1": "abcdef", "serial_number_input_2": "abcdef",},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsYearOfManufactureDetailsForm)


def test_firearms_year_of_manufacture_details_preexisting(goto_step_preexisting, post_to_step_preexisting):
    response = goto_step_preexisting(AddGoodToApplicationFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS)
    assert isinstance(response.context["form"], FirearmsYearOfManufactureDetailsForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS, {"year_of_manufacture": 2020,},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsUnitQuantityValueForm)


def test_firearms_unit_quantity_value_preexisting(goto_step_preexisting, post_to_step_preexisting):
    response = goto_step_preexisting(AddGoodToApplicationFormSteps.FIREARM_UNIT_QUANTITY_VALUE)
    assert isinstance(response.context["form"], FirearmsUnitQuantityValueForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARM_UNIT_QUANTITY_VALUE,
        {"value": "120", "is_good_incorporated": True, "is_deactivated": False, "has_proof_mark": True,},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], RegisteredFirearmsDealerForm)


def test_registered_firearms_dealer_preexisting(goto_step_preexisting, post_to_step_preexisting):
    response = goto_step_preexisting(AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER)
    assert isinstance(response.context["form"], RegisteredFirearmsDealerForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER, {"is_registered_firearm_dealer": True,},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], AttachFirearmsDealerCertificateForm)


def test_attach_firearms_dealer_certificate_preexisting(goto_step_preexisting, post_to_step_preexisting):
    goto_step_preexisting(AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER)
    post_to_step_preexisting(
        AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER, {"is_registered_firearm_dealer": True,},
    )

    response = goto_step_preexisting(AddGoodToApplicationFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE)
    assert isinstance(response.context["form"], AttachFirearmsDealerCertificateForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE,
        {
            "expiry_date_0": 1,
            "expiry_date_1": 1,
            "expiry_date_2": timezone.now().year + 1,
            "reference_code": "12345",
            "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsActConfirmationForm)


def test_firearms_act_confirmation_preexisting(goto_step_preexisting, post_to_step_preexisting):
    response = goto_step_preexisting(AddGoodToApplicationFormSteps.FIREARMS_ACT_CONFIRMATION)
    assert isinstance(response.context["form"], FirearmsActConfirmationForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_ACT_CONFIRMATION,
        {"is_covered_by_firearm_act_section_one_two_or_five": "No",},
    )
    assert response.status_code == 200
    assert not isinstance(response.context["form"], FirearmsActConfirmationForm)


def _submit_good_to_application(prexisting_url, authorized_client, post_to_step_preexisting, case):
    authorized_client.get(prexisting_url)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS, {"number_of_items": "3"},
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS, {"has_identification_markings": True},
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS,
        {"serial_number_input_0": "abcdef", "serial_number_input_1": "abcdef", "serial_number_input_2": "abcdef",},
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS, {"year_of_manufacture": 2020,},
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARM_UNIT_QUANTITY_VALUE,
        {"value": "120", "is_good_incorporated": True, "is_deactivated": False, "has_proof_mark": True,},
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER, {"is_registered_firearm_dealer": True,},
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE,
        {
            "expiry_date_0": 1,
            "expiry_date_1": 1,
            "expiry_date_2": timezone.now().year + 1,
            "reference_code": "12345",
            "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        },
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_ACT_CONFIRMATION,
        {"is_covered_by_firearm_act_section_one_two_or_five": "Yes", "firearms_act_section": "firearms_act_section5",},
    )
    assert response.status_code == 302
    assert response.url == f"/applications/{case['case']['id']}/goods/"


def test_add_good_to_application_api_submission_preexisting(
    preexisting_url, authorized_client, post_to_step_preexisting, requests_mock, case, good,
):
    requests_mock.post(f"/applications/{case['id']}/goods/", status_code=201, json={})
    requests_mock.post(f"/applications/{case['case']['id']}/documents/", status_code=201, json={})

    _submit_good_to_application(preexisting_url, authorized_client, post_to_step_preexisting, case)

    rfd_cert_data = requests_mock.request_history.pop().json()
    assert rfd_cert_data == {
        "name": f'{rfd_cert_data["name"]}',
        "s3_key": f'{rfd_cert_data["s3_key"]}',
        "size": 0,
        "document_on_organisation": {
            "expiry_date": "2023-01-01",
            "reference_code": "12345",
            "document_type": "rfd-certificate",
        },
    }

    good_to_application_data = requests_mock.request_history.pop().json()
    assert good_to_application_data == {
        "number_of_items": 3,
        "number_of_items_step": True,
        "has_identification_markings": "True",
        "identification_markings_step": True,
        "serial_number_input_0": "abcdef",
        "serial_number_input_1": "abcdef",
        "serial_number_input_2": "abcdef",
        "capture_serial_numbers_step": True,
        "firearm_year_of_manufacture_step": True,
        "value": "120",
        "is_good_incorporated": True,
        "is_registered_firearm_dealer": "True",
        "reference_code": "12345",
        "expiry_date": "2023-01-01",
        "expiry_date_day": "1",
        "expiry_date_month": "1",
        "expiry_date_year": "2023",
        "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        "firearms_act_section": "firearms_act_section5",
        "section_certificate_step": True,
        "pk": case["case"]["id"],
        "good_id": good["good"]["id"],
        "type": "firearms",
        "section_certificate_missing": "certification missing",
        "section_certificate_missing_reason": "missing reason",
        "section_certificate_number": "12345",
        "section_certificate_date_of_expiryday": "28",
        "section_certificate_date_of_expirymonth": "02",
        "section_certificate_date_of_expiryyear": "2022",
        "firearms_certificate_uploaded": True,
        "firearm_details": {
            "number_of_items": 3,
            "has_identification_markings": "True",
            "no_identification_markings_details": "",
            "serial_numbers": ["abcdef", "abcdef", "abcdef"],
            "year_of_manufacture": "2020",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section5",
            "section_certificate_missing": True,
            "section_certificate_missing_reason": "missing reason",
            "section_certificate_number": "",
            "date_of_deactivation": None,
            "has_proof_mark": True,
            "no_proof_mark_details": "",
            "is_deactivated": False,
            "deactivation_standard": "",
            "deactivation_standard_other": "",
            "is_deactivated_to_standard": "",
        },
        "quantity": 3,
        "unit": "NAR",
    }
