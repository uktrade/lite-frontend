import datetime
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from exporter.applications.views.goods.add_good_firearm.views.constants import AddGoodFirearmToApplicationSteps
from exporter.core.helpers import decompose_date
from exporter.goods.forms.firearms import (
    FirearmAttachFirearmCertificateForm,
    FirearmAttachShotgunCertificateForm,
    FirearmDeactivationDetailsForm,
    FirearmIsDeactivatedForm,
    FirearmOnwardExportedForm,
    FirearmOnwardAlteredProcessedForm,
    FirearmOnwardIncorporatedForm,
    FirearmQuantityAndValueForm,
    FirearmYearOfManufactureForm,
    FirearmSerialIdentificationMarkingsForm,
    FirearmSerialNumbersForm,
)


@pytest.fixture(autouse=True)
def setup(mock_application_get, mock_good_get, no_op_storage):
    pass


@pytest.fixture(autouse=True)
def application(data_standard_case):
    return data_standard_case["case"]["data"]


@pytest.fixture
def new_firearm_to_application_url(application):
    good = application["goods"][0]["good"]
    return reverse(
        "applications:new_good_firearm_to_application",
        kwargs={
            "pk": application["id"],
            "good_pk": good["id"],
        },
    )


@pytest.fixture
def expected_good_data(application):
    good = application["goods"][0]["good"]
    return good


@pytest.fixture(autouse=True)
def set_feature_flags(settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS = True
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.fixture
def goto_step(goto_step_factory, new_firearm_to_application_url):
    return goto_step_factory(new_firearm_to_application_url)


@pytest.fixture
def post_to_step(post_to_step_factory, new_firearm_to_application_url):
    return post_to_step_factory(new_firearm_to_application_url)


@pytest.fixture(autouse=True)
def mock_get_document(requests_mock, expected_good_data):
    return requests_mock.get(
        f"/goods/{expected_good_data['id']}/documents/",
        json={},
    )


def test_add_firearm_to_application_product_made_before_1938_step(goto_step, post_to_step):
    goto_step(AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)


def test_add_firearm_to_application_product_not_made_before_1938_step(
    requests_mock, expected_good_data, goto_step, post_to_step
):
    goto_step(AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": False},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmOnwardExportedForm)


def test_add_firearm_to_application_year_of_manufacture_step(goto_step, post_to_step):
    goto_step(AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938)
    post_to_step(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE,
        {"year_of_manufacture": 1937},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmOnwardExportedForm)


def test_add_firearm_to_application_onward_exported_step_not_onward_export(goto_step, post_to_step):
    goto_step(AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": False},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmIsDeactivatedForm)


def test_add_firearm_to_application_is_deactivated_false(requests_mock, expected_good_data, goto_step, post_to_step):
    goto_step(AddGoodFirearmToApplicationSteps.IS_DEACTIVATED)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED,
        {"is_deactivated": False},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmQuantityAndValueForm)


def test_add_firearm_to_application_is_deactivated_true(requests_mock, expected_good_data, goto_step, post_to_step):
    goto_step(AddGoodFirearmToApplicationSteps.IS_DEACTIVATED)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED,
        {"is_deactivated": True},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmDeactivationDetailsForm)


def test_add_firearm_to_application_has_serial_numbers(requests_mock, expected_good_data, goto_step, post_to_step):
    goto_step(AddGoodFirearmToApplicationSteps.QUANTITY_AND_VALUE)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.QUANTITY_AND_VALUE,
        {"number_of_items": "1", "value": "12.34"},
    )
    goto_step(AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "AVAILABLE"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmSerialNumbersForm)


def test_add_firearm_to_application_end_to_end_no_firearm_certificate(
    requests_mock,
    expected_good_data,
    mock_good_on_application_post,
    application,
    good_on_application,
    goto_step,
    post_to_step,
):
    requests_mock.get(
        f"/goods/{expected_good_data['id']}/documents/",
        json={},
    )

    goto_step(AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938)
    response = post_to_step(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE,
        {"year_of_manufacture": 1937},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmOnwardExportedForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmOnwardAlteredProcessedForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmOnwardIncorporatedForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED,
        {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmIsDeactivatedForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED,
        {"is_deactivated": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmDeactivationDetailsForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD,
        {
            "date_of_deactivation_0": "12",
            "date_of_deactivation_1": "11",
            "date_of_deactivation_2": "2007",
            "is_deactivated_to_standard": True,
        },
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmQuantityAndValueForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.QUANTITY_AND_VALUE,
        {"number_of_items": "2", "value": "16.32"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialIdentificationMarkingsForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "AVAILABLE"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialNumbersForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS,
        {
            "serial_numbers_0": "s111",
            "serial_numbers_1": "s222",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "applications:product_on_application_summary",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["good"]["id"],
        },
    )

    assert mock_good_on_application_post.last_request.json() == {
        "firearm_details": {
            "is_made_before_1938": True,
            "year_of_manufacture": 1937,
            "is_onward_exported": True,
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "processed comments",
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "incorporated comments",
            "is_deactivated": True,
            "date_of_deactivation": "2007-11-12",
            "is_deactivated_to_standard": True,
            "not_deactivated_to_standard_comments": "",
            "number_of_items": 2,
            "serial_numbers_available": "AVAILABLE",
            "no_identification_markings_details": "",
            "serial_numbers": ["s111", "s222"],
        },
        "good_id": expected_good_data["id"],
        "is_good_incorporated": True,
        "quantity": 2,
        "unit": "NAR",
        "value": "16.32",
    }


@pytest.mark.parametrize(
    "firearms_act_section, firearms_certificate_step_name, firearms_certificate_form_class, firearm_certificate_document_type, document_description",
    (
        (
            "firearms_act_section1",
            AddGoodFirearmToApplicationSteps.ATTACH_FIREARM_CERTIFICATE,
            FirearmAttachFirearmCertificateForm,
            "section-one-certificate",
            "Firearm certificate for 'p1'",
        ),
        (
            "firearms_act_section2",
            AddGoodFirearmToApplicationSteps.ATTACH_SHOTGUN_CERTIFICATE,
            FirearmAttachShotgunCertificateForm,
            "section-two-certificate",
            "Shotgun certificate for 'p1'",
        ),
    ),
)
def test_add_firearm_to_application_end_to_end_firearm_certificate(
    authorized_client,
    requests_mock,
    mock_good_on_application_post,
    expected_good_data,
    application,
    data_standard_case,
    good_on_application,
    goto_step,
    post_to_step,
    new_firearm_to_application_url,
    firearms_act_section,
    firearms_certificate_step_name,
    firearms_certificate_form_class,
    firearm_certificate_document_type,
    document_description,
):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"]["firearm_details"]["firearms_act_section"] = firearms_act_section
    requests_mock.get(f'/goods/{good["good"]["id"]}/', json=good)

    requests_mock.get(
        f"/goods/{expected_good_data['id']}/documents/",
        json={},
    )

    post_good_on_application_document_matcher = requests_mock.post(
        f"/applications/{data_standard_case['case']['id']}/goods/{expected_good_data['id']}/documents/",
        status_code=201,
        json={},
    )

    post_application_document_matcher = requests_mock.post(
        f"/applications/{data_standard_case['case']['id']}/documents/",
        status_code=201,
        json={},
    )

    response = authorized_client.get(new_firearm_to_application_url)
    assert isinstance(response.context["form"], firearms_certificate_form_class)

    certificate_expiry_date = datetime.date.today() + datetime.timedelta(days=5)
    response = post_to_step(
        firearms_certificate_step_name,
        {
            "file": SimpleUploadedFile("certificate.pdf", b"This is the certificate"),
            "section_certificate_number": "12345",
            **decompose_date("section_certificate_date_of_expiry", certificate_expiry_date),
        },
    )

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE,
        {"year_of_manufacture": 1937},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmOnwardExportedForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmOnwardAlteredProcessedForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmOnwardIncorporatedForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED,
        {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmIsDeactivatedForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED,
        {"is_deactivated": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmDeactivationDetailsForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD,
        {
            "date_of_deactivation_0": "12",
            "date_of_deactivation_1": "11",
            "date_of_deactivation_2": "2007",
            "is_deactivated_to_standard": True,
        },
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmQuantityAndValueForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.QUANTITY_AND_VALUE,
        {"number_of_items": "2", "value": "16.32"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialIdentificationMarkingsForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "AVAILABLE"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialNumbersForm)

    response = post_to_step(
        AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS,
        {
            "serial_numbers_0": "s111",
            "serial_numbers_1": "s222",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "applications:product_on_application_summary",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["good"]["id"],
        },
    )

    assert mock_good_on_application_post.last_request.json() == {
        "firearm_details": {
            "is_made_before_1938": True,
            "year_of_manufacture": 1937,
            "is_onward_exported": True,
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "processed comments",
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "incorporated comments",
            "is_deactivated": True,
            "date_of_deactivation": "2007-11-12",
            "is_deactivated_to_standard": True,
            "not_deactivated_to_standard_comments": "",
            "number_of_items": 2,
            "section_certificate_date_of_expiry": certificate_expiry_date.isoformat(),
            "section_certificate_missing": False,
            "section_certificate_number": "12345",
            "serial_numbers_available": "AVAILABLE",
            "no_identification_markings_details": "",
            "serial_numbers": ["s111", "s222"],
        },
        "good_id": expected_good_data["id"],
        "is_good_incorporated": True,
        "quantity": 2,
        "unit": "NAR",
        "value": "16.32",
    }

    assert post_good_on_application_document_matcher.called_once
    assert post_good_on_application_document_matcher.last_request.json() == {
        "document_type": firearm_certificate_document_type,
        "good_on_application": good_on_application["good"]["id"],
        "name": "certificate.pdf",
        "s3_key": "certificate.pdf",
        "size": 0,
    }

    assert post_application_document_matcher.called_once
    assert post_application_document_matcher.last_request.json() == {
        "description": document_description,
        "document_type": firearm_certificate_document_type,
        "name": "certificate.pdf",
        "s3_key": "certificate.pdf",
        "size": 0,
    }
