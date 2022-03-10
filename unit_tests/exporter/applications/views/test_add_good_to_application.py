import pytest
import uuid

from pytest_django.asserts import assertNotContains
from unittest.mock import patch

from django.core.files.storage import Storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from core import client
from exporter.applications.views.goods import AddGoodToApplicationFormSteps
from exporter.goods.forms import (
    AttachFirearmsDealerCertificateForm,
    ComponentOfAFirearmAmmunitionUnitQuantityValueForm,
    ComponentOfAFirearmUnitQuantityValueForm,
    FirearmsActConfirmationForm,
    FirearmsCaptureSerialNumbersForm,
    FirearmsNumberOfItemsForm,
    FirearmsUnitQuantityValueForm,
    FirearmsYearOfManufactureDetailsForm,
    IdentificationMarkingsForm,
    RegisteredFirearmsDealerForm,
    UnitQuantityValueForm,
)


ADD_GOOD_TO_APPLICATION_VIEW = "add_good_to_application"


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
        "exporter.applications.views.goods.AddGoodToApplication.file_storage", new=NoOpStorage()
    ):
        yield


@pytest.fixture
def case():
    return {
        "id": str(uuid.uuid4()),
        "case": {
            "id": str(uuid.uuid4()),
        },
    }


@pytest.fixture
def case_with_documents(case):
    case = case.copy()
    case["organisation"] = {
        "documents": [
            {
                "document_type": "section-five-certificate",
                "is_expired": False,
                "expiry_date": "01 January 2030",
                "reference_code": "12345",
            },
        ],
    }

    return case


@pytest.fixture
def case_without_documents(case):
    case = case.copy()
    case["organisation"] = {
        "documents": [],
    }

    return case


@pytest.fixture
def good_data():
    return {
        "id": str(uuid.uuid4()),
        "name": "good name",
        "description": "good description",
        "part_number": "12345",
        "firearm_details": {
            "type": {
                "key": "firearms",
            },
            "section_certificate_missing": "certification missing",
            "section_certificate_missing_reason": "missing reason",
        },
        "item_category": {
            "key": "group2_firearms",
        },
        "control_list_entries": [],
    }


@pytest.fixture
def good(good_data):
    return {
        "good": good_data,
    }


@pytest.fixture
def preexisting_url(case, good):
    url = reverse(
        "applications:add_good_to_application",
        kwargs={"pk": case["case"]["id"], "good_pk": good["good"]["id"]},
    )

    return f"{url}?preexisting=True"


@pytest.fixture
def not_preexisting_url(case, good):
    url = reverse(
        "applications:add_good_to_application",
        kwargs={"pk": case["case"]["id"], "good_pk": good["good"]["id"]},
    )

    return f"{url}?preexisting=False"


@pytest.fixture(autouse=True)
def mock_good_request(requests_mock, good):
    good_pk = good["good"]["id"]
    path = f"/goods/{good_pk}/?pk={good_pk}&full_detail=False"
    app_url = client._build_absolute_uri(path)
    return requests_mock.get(url=app_url, json=good)


@pytest.fixture
def mock_application_with_documents_request(requests_mock, case_with_documents):
    case_pk = case_with_documents["case"]["id"]
    path = f"/applications/{case_pk}/"
    app_url = client._build_absolute_uri(path)
    return requests_mock.get(url=app_url, json=case_with_documents)


@pytest.fixture
def mock_application_without_documents_request(requests_mock, case_without_documents):
    case_pk = case_without_documents["case"]["id"]
    path = f"/applications/{case_pk}/"
    app_url = client._build_absolute_uri(path)
    return requests_mock.get(url=app_url, json=case_without_documents)


@pytest.fixture()
def goto_step_preexisting(preexisting_url, authorized_client):
    def _goto_step(step_name):
        return authorized_client.post(
            preexisting_url,
            data={
                "wizard_goto_step": step_name,
            },
        )

    return _goto_step


@pytest.fixture()
def goto_step_not_preexisting(not_preexisting_url, authorized_client):
    def _goto_step(step_name):
        return authorized_client.post(
            not_preexisting_url,
            data={
                "wizard_goto_step": step_name,
            },
        )

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


@pytest.fixture()
def post_to_step_not_preexisting(not_preexisting_url, authorized_client):
    def _post_to_step(step_name, data):
        return authorized_client.post(
            not_preexisting_url,
            data={
                f"{ADD_GOOD_TO_APPLICATION_VIEW}-current_step": step_name,
                **{f"{step_name}-{key}": value for key, value in data.items()},
            },
        )

    return _post_to_step


def test_add_good_to_application_preexisting_start(
    mock_application_with_documents_request, preexisting_url, authorized_client
):
    response = authorized_client.get(preexisting_url)

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsNumberOfItemsForm)
    assertNotContains(response, "Step 1 of", html=True)


def test_add_number_of_items_preexisting(
    mock_application_with_documents_request, goto_step_preexisting, post_to_step_preexisting
):
    response = goto_step_preexisting(AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS)
    assert isinstance(response.context["form"], FirearmsNumberOfItemsForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS,
        {"number_of_items": "3"},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], IdentificationMarkingsForm)


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
            FirearmsYearOfManufactureDetailsForm,
        ),
        (
            {
                "serial_numbers_available": "NOT_AVAILABLE",
                "no_identification_markings_details": "reasons",
            },
            FirearmsYearOfManufactureDetailsForm,
        ),
    ],
)
def test_identification_markings_preexisting(
    mock_application_with_documents_request,
    goto_step_preexisting,
    post_to_step_preexisting,
    data,
    expected_next_form,
):
    response = goto_step_preexisting(AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS)
    assert isinstance(response.context["form"], IdentificationMarkingsForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS,
        data,
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], expected_next_form)


def test_firearms_capture_serial_numbers_preexisting(
    mock_application_with_documents_request, goto_step_preexisting, post_to_step_preexisting
):
    goto_step_preexisting(AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS)
    post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS,
        {"number_of_items": "3"},
    )

    goto_step_preexisting(AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS)
    post_to_step_preexisting(
        AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS,
        {"serial_numbers_available": "AVAILABLE"},
    )

    response = goto_step_preexisting(AddGoodToApplicationFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS)
    assert isinstance(response.context["form"], FirearmsCaptureSerialNumbersForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS,
        {
            "serial_numbers_0": "abcdef",
            "serial_numbers_1": "abcdef",
            "serial_numbers_2": "abcdef",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsYearOfManufactureDetailsForm)


def test_firearms_year_of_manufacture_details_preexisting(
    mock_application_with_documents_request, goto_step_preexisting, post_to_step_preexisting
):
    response = goto_step_preexisting(AddGoodToApplicationFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS)
    assert isinstance(response.context["form"], FirearmsYearOfManufactureDetailsForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS,
        {
            "year_of_manufacture": 2020,
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsUnitQuantityValueForm)


def test_firearms_unit_quantity_value_preexisting(
    mock_application_with_documents_request, goto_step_preexisting, post_to_step_preexisting
):
    response = goto_step_preexisting(AddGoodToApplicationFormSteps.FIREARM_UNIT_QUANTITY_VALUE)
    assert isinstance(response.context["form"], FirearmsUnitQuantityValueForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARM_UNIT_QUANTITY_VALUE,
        {
            "value": "120",
            "is_good_incorporated": True,
            "is_deactivated": False,
            "has_proof_mark": True,
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], RegisteredFirearmsDealerForm)


def test_registered_firearms_dealer_preexisting(
    mock_application_with_documents_request, goto_step_preexisting, post_to_step_preexisting
):
    response = goto_step_preexisting(AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER)
    assert isinstance(response.context["form"], RegisteredFirearmsDealerForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER,
        {
            "is_registered_firearm_dealer": True,
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], AttachFirearmsDealerCertificateForm)


def test_attach_firearms_dealer_certificate_preexisting(
    mock_application_with_documents_request, goto_step_preexisting, post_to_step_preexisting
):
    goto_step_preexisting(AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER)
    post_to_step_preexisting(
        AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER,
        {
            "is_registered_firearm_dealer": True,
        },
    )

    response = goto_step_preexisting(AddGoodToApplicationFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE)
    assert isinstance(response.context["form"], AttachFirearmsDealerCertificateForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE,
        {
            "expiry_date_0": 1,
            "expiry_date_1": 1,
            "expiry_date_2": 2030,
            "reference_code": "12345",
            "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsActConfirmationForm)


def test_firearms_act_confirmation_preexisting(
    mock_application_with_documents_request, goto_step_preexisting, post_to_step_preexisting
):
    response = goto_step_preexisting(AddGoodToApplicationFormSteps.FIREARMS_ACT_CONFIRMATION)
    assert isinstance(response.context["form"], FirearmsActConfirmationForm)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_ACT_CONFIRMATION,
        {
            "is_covered_by_firearm_act_section_one_two_or_five": "No",
        },
    )
    assert response.status_code == 200
    assert not isinstance(response.context["form"], FirearmsActConfirmationForm)


def _submit_good_to_application(preexisting_url, authorized_client, post_to_step_preexisting, case):
    authorized_client.get(preexisting_url)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS,
        {"number_of_items": "3"},
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS,
        {"serial_numbers_available": "AVAILABLE"},
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS,
        {
            "serial_numbers_0": "abcdef",
            "serial_numbers_1": "abcdef",
            "serial_numbers_2": "abcdef",
        },
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS,
        {
            "year_of_manufacture": 2020,
        },
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARM_UNIT_QUANTITY_VALUE,
        {
            "value": "120",
            "is_good_incorporated": True,
            "is_deactivated": False,
            "has_proof_mark": True,
        },
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER,
        {
            "is_registered_firearm_dealer": True,
        },
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE,
        {
            "expiry_date_0": 1,
            "expiry_date_1": 1,
            "expiry_date_2": 2030,
            "reference_code": "12345",
            "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        },
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_ACT_CONFIRMATION,
        {
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section5",
        },
    )
    assert response.status_code == 302

    return response


def test_add_good_to_application_api_submission_with_documents_preexisting(
    mock_application_with_documents_request,
    preexisting_url,
    authorized_client,
    post_to_step_preexisting,
    requests_mock,
    case,
    good,
):
    goods_matcher = requests_mock.post(f"/applications/{case['id']}/goods/", status_code=201, json={})
    documents_matcher = requests_mock.post(f"/applications/{case['case']['id']}/documents/", status_code=201, json={})

    response = _submit_good_to_application(preexisting_url, authorized_client, post_to_step_preexisting, case)
    assert response.url == f"/applications/{case['case']['id']}/goods/"

    assert goods_matcher.called_once
    assert documents_matcher.called_once

    good_to_application_data = goods_matcher.last_request.json()
    assert good_to_application_data == {
        "number_of_items": 3,
        "number_of_items_step": True,
        "identification_markings_step": True,
        "serial_number_input_0": "abcdef",
        "serial_number_input_1": "abcdef",
        "serial_number_input_2": "abcdef",
        "serial_numbers_available": "AVAILABLE",
        "capture_serial_numbers_step": True,
        "firearm_year_of_manufacture_step": True,
        "value": "120",
        "is_good_incorporated": True,
        "is_registered_firearm_dealer": "True",
        "reference_code": "12345",
        "expiry_date": "2030-01-01",
        "expiry_date_day": "1",
        "expiry_date_month": "1",
        "expiry_date_year": "2030",
        "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        "firearms_act_section": "firearms_act_section5",
        "section_certificate_step": True,
        "pk": case["case"]["id"],
        "good_id": good["good"]["id"],
        "type": "firearms",
        "section_certificate_missing": "certification missing",
        "section_certificate_missing_reason": "missing reason",
        "section_certificate_number": "12345",
        "section_certificate_date_of_expiryday": "01",
        "section_certificate_date_of_expirymonth": "01",
        "section_certificate_date_of_expiryyear": "2030",
        "firearms_certificate_uploaded": True,
        "firearm_details": {
            "number_of_items": 3,
            "serial_numbers_available": "AVAILABLE",
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

    rfd_cert_data = documents_matcher.last_request.json()
    assert rfd_cert_data == {
        "name": f'{rfd_cert_data["name"]}',
        "s3_key": f'{rfd_cert_data["s3_key"]}',
        "size": 0,
        "document_on_organisation": {
            "expiry_date": "2030-01-01",
            "reference_code": "12345",
            "document_type": "rfd-certificate",
        },
    }


def test_add_good_to_application_api_submission_with_deferred_serial_numbers_with_documents_preexisting(
    mock_application_with_documents_request,
    preexisting_url,
    authorized_client,
    post_to_step_preexisting,
    requests_mock,
    case,
    good,
):
    goods_matcher = requests_mock.post(f"/applications/{case['id']}/goods/", status_code=201, json={})
    documents_matcher = requests_mock.post(f"/applications/{case['case']['id']}/documents/", status_code=201, json={})

    authorized_client.get(preexisting_url)

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS,
        {"number_of_items": "3"},
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS,
        {"serial_numbers_available": "LATER"},
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS,
        {
            "year_of_manufacture": 2020,
        },
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARM_UNIT_QUANTITY_VALUE,
        {
            "value": "120",
            "is_good_incorporated": True,
            "is_deactivated": False,
            "has_proof_mark": True,
        },
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER,
        {
            "is_registered_firearm_dealer": True,
        },
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE,
        {
            "expiry_date_0": 1,
            "expiry_date_1": 1,
            "expiry_date_2": 2030,
            "reference_code": "12345",
            "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
        },
    )
    assert not response.context["form"].errors

    response = post_to_step_preexisting(
        AddGoodToApplicationFormSteps.FIREARMS_ACT_CONFIRMATION,
        {
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section5",
        },
    )
    assert response.status_code == 302

    assert response.url == f"/applications/{case['case']['id']}/goods/"

    assert goods_matcher.called_once
    assert documents_matcher.called_once

    good_to_application_data = goods_matcher.last_request.json()
    assert good_to_application_data == {
        "number_of_items": 3,
        "number_of_items_step": True,
        "identification_markings_step": True,
        "serial_numbers_available": "LATER",
        "firearm_year_of_manufacture_step": True,
        "value": "120",
        "is_good_incorporated": True,
        "is_registered_firearm_dealer": "True",
        "reference_code": "12345",
        "expiry_date": "2030-01-01",
        "expiry_date_day": "1",
        "expiry_date_month": "1",
        "expiry_date_year": "2030",
        "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        "firearms_act_section": "firearms_act_section5",
        "section_certificate_step": True,
        "pk": case["case"]["id"],
        "good_id": good["good"]["id"],
        "type": "firearms",
        "section_certificate_missing": "certification missing",
        "section_certificate_missing_reason": "missing reason",
        "section_certificate_number": "12345",
        "section_certificate_date_of_expiryday": "01",
        "section_certificate_date_of_expirymonth": "01",
        "section_certificate_date_of_expiryyear": "2030",
        "firearms_certificate_uploaded": True,
        "firearm_details": {
            "number_of_items": 3,
            "serial_numbers_available": "LATER",
            "no_identification_markings_details": "",
            "serial_numbers": [],
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

    rfd_cert_data = documents_matcher.last_request.json()
    assert rfd_cert_data == {
        "name": f'{rfd_cert_data["name"]}',
        "s3_key": f'{rfd_cert_data["s3_key"]}',
        "size": 0,
        "document_on_organisation": {
            "expiry_date": "2030-01-01",
            "reference_code": "12345",
            "document_type": "rfd-certificate",
        },
    }


def test_add_good_to_application_api_submission_without_documents_preexisting(
    mock_application_without_documents_request,
    preexisting_url,
    authorized_client,
    post_to_step_preexisting,
    requests_mock,
    case,
    good,
    lite_api_user_id,
):
    goods_matcher = requests_mock.post(f"/applications/{case['id']}/goods/", status_code=201, json={})
    documents_matcher = requests_mock.post(f"/applications/{case['case']['id']}/documents/", status_code=201, json={})

    response = _submit_good_to_application(preexisting_url, authorized_client, post_to_step_preexisting, case)
    assert response.url == f'/applications/{case["case"]["id"]}/goods/{good["good"]["id"]}/add-firearms-certificate/'

    assert not goods_matcher.called

    assert documents_matcher.called_once
    rfd_cert_data = documents_matcher.last_request.json()
    assert rfd_cert_data == {
        "name": f'{rfd_cert_data["name"]}',
        "s3_key": f'{rfd_cert_data["s3_key"]}',
        "size": 0,
        "document_on_organisation": {
            "expiry_date": "2030-01-01",
            "reference_code": "12345",
            "document_type": "rfd-certificate",
        },
    }

    stored_data = authorized_client.session[f"post_{lite_api_user_id}_{case['case']['id']}_{good['good']['id']}"]
    assert stored_data == {
        "capture_serial_numbers_step": True,
        "date_of_deactivation": None,
        "deactivation_standard": "",
        "deactivation_standard_other": "",
        "expiry_date": "2030-01-01",
        "expiry_date_day": "1",
        "expiry_date_month": "1",
        "expiry_date_year": "2030",
        "firearm_year_of_manufacture_step": True,
        "firearms_act_section": "firearms_act_section5",
        "form_pk": 1,
        "good_id": good["good"]["id"],
        "has_proof_mark": True,
        "identification_markings_step": True,
        "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        "is_deactivated": False,
        "is_deactivated_to_standard": "",
        "is_good_incorporated": True,
        "is_registered_firearm_dealer": "True",
        "no_identification_markings_details": "",
        "no_proof_mark_details": "",
        "number_of_items": 3,
        "number_of_items_step": True,
        "pk": case["case"]["id"],
        "reference_code": "12345",
        "section_certificate_step": True,
        "serial_number_input_0": "abcdef",
        "serial_number_input_1": "abcdef",
        "serial_number_input_2": "abcdef",
        "serial_numbers_available": "AVAILABLE",
        "type": "firearms",
        "value": "120",
        "year_of_manufacture": "2020",
        "wizard_goto_step": "FIREARMS_ACT_CONFIRMATION",
    }


def test_add_good_to_application_not_preexisting_start(
    mock_application_with_documents_request, not_preexisting_url, authorized_client
):
    response = authorized_client.get(not_preexisting_url)

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmsUnitQuantityValueForm)
    assertNotContains(response, "Step 1 of", html=True)


def test_add_good_to_application_component_of_a_firearm_not_preexisting_start(
    mock_application_with_documents_request,
    requests_mock,
    good_data,
    not_preexisting_url,
    authorized_client,
):
    good = {"good": good_data.copy()}
    good["good"]["firearm_details"]["type"]["key"] = "components_for_firearms"

    good_pk = good["good"]["id"]
    path = f"/goods/{good_pk}/?pk={good_pk}&full_detail=False"
    app_url = client._build_absolute_uri(path)
    requests_mock.get(url=app_url, json=good)

    response = authorized_client.get(not_preexisting_url)

    assert response.status_code == 200
    assert isinstance(response.context["form"], ComponentOfAFirearmUnitQuantityValueForm)
    assertNotContains(response, "Step 1 of", html=True)


def test_add_good_to_application_component_of_a_firearm_ammunition_not_preexisting_start(
    mock_application_with_documents_request,
    requests_mock,
    good_data,
    not_preexisting_url,
    authorized_client,
):
    good = {"good": good_data.copy()}
    good["good"]["firearm_details"]["type"]["key"] = "components_for_ammunition"

    good_pk = good["good"]["id"]
    path = f"/goods/{good_pk}/?pk={good_pk}&full_detail=False"
    app_url = client._build_absolute_uri(path)
    requests_mock.get(url=app_url, json=good)

    response = authorized_client.get(not_preexisting_url)

    assert response.status_code == 200
    assert isinstance(response.context["form"], ComponentOfAFirearmAmmunitionUnitQuantityValueForm)
    assertNotContains(response, "Step 1 of", html=True)


def test_add_good_to_application_software_not_preexisting_start(
    mock_application_with_documents_request,
    requests_mock,
    good_data,
    not_preexisting_url,
    authorized_client,
    mock_units,
):
    good = {"good": good_data.copy()}
    good["good"]["firearm_details"]["type"]["key"] = "software_related_to_firearms"

    good_pk = good["good"]["id"]
    path = f"/goods/{good_pk}/?pk={good_pk}&full_detail=False"
    app_url = client._build_absolute_uri(path)
    requests_mock.get(url=app_url, json=good)

    response = authorized_client.get(not_preexisting_url)

    assert response.status_code == 200
    assert isinstance(response.context["form"], UnitQuantityValueForm)
    assertNotContains(response, "Step 1 of", html=True)
