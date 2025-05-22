import datetime
import pytest

from pytest_django.asserts import assertContains

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from core import client
from core.constants import OrganisationDocumentType
from core.helpers import decompose_date

from exporter.applications.views.goods.firearm.views.constants import AttachFirearmToApplicationSteps
from exporter.goods.forms.common import (
    ProductOnwardAlteredProcessedForm,
    ProductOnwardExportedForm,
    ProductOnwardIncorporatedForm,
    ProductQuantityAndValueForm,
)
from exporter.goods.forms.firearms import (
    FirearmAttachFirearmCertificateForm,
    FirearmAttachShotgunCertificateForm,
    FirearmCategoryForm,
    FirearmDeactivationDetailsForm,
    FirearmIsDeactivatedForm,
    FirearmMadeBefore1938Form,
    FirearmRFDInvalidForm,
    FirearmRFDValidityForm,
    FirearmSerialIdentificationMarkingsForm,
    FirearmSerialNumbersForm,
    FirearmYearOfManufactureForm,
)


@pytest.fixture(autouse=True)
def setup(mock_application_get, mock_good_get, no_op_storage):
    yield


@pytest.fixture(autouse=True)
def set_feature_flags(settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS = True


@pytest.fixture
def good(application):
    good = application["goods"][0]["good"]
    return good


@pytest.fixture
def mock_good_attaching_put(requests_mock, good):
    url = client._build_absolute_uri(f'/goods/{good["id"]}/attaching/')
    return requests_mock.put(url=url, json={})


@pytest.fixture
def good_no_category(data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"]["firearm_details"]["category"] = None

    return good


@pytest.fixture
def mock_good_no_category_get(requests_mock, good_no_category):
    url = client._build_absolute_uri(f'/goods/{good_no_category["good"]["id"]}/')
    return requests_mock.get(url=url, json=good_no_category)


@pytest.fixture
def attach_firearm_to_application_url(application, good):
    return reverse(
        "applications:attach_firearm_to_application",
        kwargs={
            "pk": application["id"],
            "good_pk": good["id"],
        },
    )


@pytest.fixture
def attach_product_on_application_summary_url(application, good_on_application):
    return reverse(
        "applications:attach_product_on_application_summary",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["good"]["id"],
        },
    )


@pytest.fixture
def post_to_step(post_to_step_factory, attach_firearm_to_application_url):
    return post_to_step_factory(attach_firearm_to_application_url)


def test_attach_firearm_to_application_view_displays_firearm_category_form_if_required(
    authorized_client,
    attach_firearm_to_application_url,
    good_no_category,
):
    response = authorized_client.get(attach_firearm_to_application_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmCategoryForm)


def test_attach_firearm_to_application_view_skips_firearm_category_form_if_required(
    authorized_client,
    attach_firearm_to_application_url,
    application_with_organisation_rfd_document,
):
    response = authorized_client.get(attach_firearm_to_application_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmRFDValidityForm)


def test_rfd_validity_invalid(
    post_to_step,
    application,
    application_with_organisation_rfd_document,
):
    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID,
        data={
            "is_rfd_certificate_valid": False,
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmRFDInvalidForm)


def test_rfd_validity_invalid_should_not_be_able_to_post(
    post_to_step,
    application,
    application_with_organisation_rfd_document,
    mock_good_attaching_put,
):
    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID,
        data={
            "is_rfd_certificate_valid": False,
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmRFDInvalidForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.RFD_CERTIFICATE_INVALID,
        data={},
    )
    assert response.status_code == 200
    assertContains(response, "RFD invalid. Cannot submit.")
    assert not mock_good_attaching_put.called


def test_attach_firearm_to_application_end_to_end_no_category_no_firearm_certificate(
    application,
    post_to_step,
    mock_good_no_category_get,
    good_no_category,
    mock_good_attaching_put,
    mock_good_on_application_post,
    good_on_application,
    attach_product_on_application_summary_url,
):
    response = post_to_step(
        AttachFirearmToApplicationSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmMadeBefore1938Form)

    response = post_to_step(
        AttachFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.YEAR_OF_MANUFACTURE,
        {"year_of_manufacture": 1937},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardExportedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardAlteredProcessedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardIncorporatedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_INCORPORATED,
        {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmIsDeactivatedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_DEACTIVATED,
        {"is_deactivated": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmDeactivationDetailsForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD,
        {
            "date_of_deactivation_0": "12",
            "date_of_deactivation_1": "11",
            "date_of_deactivation_2": "2007",
            "is_deactivated_to_standard": True,
        },
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductQuantityAndValueForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.QUANTITY_AND_VALUE,
        {"number_of_items": "2", "value": "16.32"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialIdentificationMarkingsForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "AVAILABLE"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialNumbersForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.SERIAL_NUMBERS,
        {
            "serial_numbers_0": "s111",
            "serial_numbers_1": "s222",
        },
    )

    assert response.status_code == 302
    assert response.url == f"{attach_product_on_application_summary_url}?added_firearm_category=True"

    assert mock_good_attaching_put.called_once
    assert mock_good_attaching_put.last_request.json() == {
        "firearm_details": {
            "category": ["NON_AUTOMATIC_SHOTGUN"],
        },
    }

    assert mock_good_on_application_post.last_request.json() == {
        "firearm_details": {
            "is_made_before_1938": True,
            "year_of_manufacture": 1937,
            "is_deactivated": True,
            "date_of_deactivation": "2007-11-12",
            "is_deactivated_to_standard": True,
            "not_deactivated_to_standard_comments": "",
            "number_of_items": "2",
            "serial_numbers_available": "AVAILABLE",
            "no_identification_markings_details": "",
            "serial_numbers": ["s111", "s222"],
        },
        "good_id": good_no_category["good"]["id"],
        "is_good_incorporated": True,
        "is_onward_exported": True,
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "processed comments",
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "incorporated comments",
        "quantity": "2",
        "unit": "NAR",
        "value": "16.32",
    }


def test_attach_firearm_to_application_end_to_end_rfd_valid(
    application,
    post_to_step,
    good,
    mock_good_attaching_put,
    mock_good_on_application_post,
    good_on_application,
    application_with_organisation_rfd_document,
    attach_product_on_application_summary_url,
    requests_mock,
):
    post_application_document_matcher = requests_mock.post(
        f"/applications/{application['id']}/documents/",
        status_code=201,
        json={},
    )

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID,
        data={
            "is_rfd_certificate_valid": True,
        },
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmMadeBefore1938Form)

    response = post_to_step(
        AttachFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.YEAR_OF_MANUFACTURE,
        {"year_of_manufacture": 1937},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardExportedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardAlteredProcessedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardIncorporatedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_INCORPORATED,
        {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmIsDeactivatedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_DEACTIVATED,
        {"is_deactivated": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmDeactivationDetailsForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD,
        {
            "date_of_deactivation_0": "12",
            "date_of_deactivation_1": "11",
            "date_of_deactivation_2": "2007",
            "is_deactivated_to_standard": True,
        },
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductQuantityAndValueForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.QUANTITY_AND_VALUE,
        {"number_of_items": "2", "value": "16.32"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialIdentificationMarkingsForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "AVAILABLE"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialNumbersForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.SERIAL_NUMBERS,
        {
            "serial_numbers_0": "s111",
            "serial_numbers_1": "s222",
        },
    )

    assert response.status_code == 302
    assert response.url == f"{attach_product_on_application_summary_url}?confirmed_rfd_validity=True"

    assert mock_good_attaching_put.called_once
    assert mock_good_attaching_put.last_request.json() == {
        "firearm_details": {
            "is_rfd_certificate_valid": True,
        },
    }

    assert mock_good_on_application_post.last_request.json() == {
        "firearm_details": {
            "is_made_before_1938": True,
            "year_of_manufacture": 1937,
            "is_deactivated": True,
            "date_of_deactivation": "2007-11-12",
            "is_deactivated_to_standard": True,
            "not_deactivated_to_standard_comments": "",
            "number_of_items": "2",
            "serial_numbers_available": "AVAILABLE",
            "no_identification_markings_details": "",
            "serial_numbers": ["s111", "s222"],
        },
        "good_id": good["id"],
        "is_good_incorporated": True,
        "is_onward_exported": True,
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "processed comments",
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "incorporated comments",
        "quantity": "2",
        "unit": "NAR",
        "value": "16.32",
    }

    assert post_application_document_matcher.called_once
    assert post_application_document_matcher.last_request.json() == {
        "description": "Registered firearm dealer certificate",
        "document_type": OrganisationDocumentType.RFD_CERTIFICATE,
        "name": "rfd_certificate.txt",
        "s3_key": "rfd_certificate.txt.s3_key",
        "safe": True,
        "size": 3,
    }


@pytest.mark.parametrize(
    "firearms_act_section, firearms_certificate_step_name, firearms_certificate_form_class, firearm_certificate_document_type, document_description",
    (
        (
            "firearms_act_section1",
            AttachFirearmToApplicationSteps.ATTACH_FIREARM_CERTIFICATE,
            FirearmAttachFirearmCertificateForm,
            "section-one-certificate",
            "Firearm certificate for 'p1'",
        ),
        (
            "firearms_act_section2",
            AttachFirearmToApplicationSteps.ATTACH_SHOTGUN_CERTIFICATE,
            FirearmAttachShotgunCertificateForm,
            "section-two-certificate",
            "Shotgun certificate for 'p1'",
        ),
    ),
)
def test_add_firearm_to_application_end_to_end_firearm_certificate(
    application,
    post_to_step,
    mock_good_no_category_get,
    good_no_category,
    mock_good_attaching_put,
    mock_good_on_application_post,
    good_on_application,
    firearms_act_section,
    firearms_certificate_step_name,
    firearms_certificate_form_class,
    firearm_certificate_document_type,
    document_description,
    requests_mock,
    attach_product_on_application_summary_url,
):
    good_no_category["good"]["firearm_details"]["firearms_act_section"] = firearms_act_section
    requests_mock.get(f'/goods/{good_no_category["good"]["id"]}/', json=good_no_category)

    requests_mock.get(
        f"/applications/{application['id']}/goods/{good_no_category['good']['id']}/documents/",
        json={"documents": []},
    )

    requests_mock.get(
        f"/goods/{good_no_category['id']}/documents/",
        json={},
    )

    post_good_on_application_document_matcher = requests_mock.post(
        f"/applications/{application['id']}/goods/{good_no_category['good']['id']}/documents/",
        status_code=201,
        json={},
    )

    post_application_document_matcher = requests_mock.post(
        f"/applications/{application['id']}/documents/",
        status_code=201,
        json={},
    )

    response = post_to_step(
        AttachFirearmToApplicationSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
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
        AttachFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.YEAR_OF_MANUFACTURE,
        {"year_of_manufacture": 1937},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardExportedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardAlteredProcessedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardIncorporatedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_INCORPORATED,
        {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmIsDeactivatedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_DEACTIVATED,
        {"is_deactivated": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmDeactivationDetailsForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD,
        {
            "date_of_deactivation_0": "12",
            "date_of_deactivation_1": "11",
            "date_of_deactivation_2": "2007",
            "is_deactivated_to_standard": True,
        },
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductQuantityAndValueForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.QUANTITY_AND_VALUE,
        {"number_of_items": "2", "value": "16.32"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialIdentificationMarkingsForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "AVAILABLE"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialNumbersForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.SERIAL_NUMBERS,
        {
            "serial_numbers_0": "s111",
            "serial_numbers_1": "s222",
        },
    )

    assert response.status_code == 302
    assert response.url == f"{attach_product_on_application_summary_url}?added_firearm_category=True"

    assert mock_good_attaching_put.called_once
    assert mock_good_attaching_put.last_request.json() == {
        "firearm_details": {
            "category": ["NON_AUTOMATIC_SHOTGUN"],
        },
    }

    assert mock_good_on_application_post.last_request.json() == {
        "firearm_details": {
            "is_made_before_1938": True,
            "year_of_manufacture": 1937,
            "is_deactivated": True,
            "date_of_deactivation": "2007-11-12",
            "is_deactivated_to_standard": True,
            "not_deactivated_to_standard_comments": "",
            "number_of_items": "2",
            "section_certificate_date_of_expiry": certificate_expiry_date.isoformat(),
            "section_certificate_missing": False,
            "section_certificate_number": "12345",
            "serial_numbers_available": "AVAILABLE",
            "no_identification_markings_details": "",
            "serial_numbers": ["s111", "s222"],
        },
        "good_id": good_no_category["good"]["id"],
        "is_good_incorporated": True,
        "is_onward_exported": True,
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "processed comments",
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "incorporated comments",
        "quantity": "2",
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


def test_attach_firearm_to_application_end_to_end_section_5_good_with_section_5_details(
    application,
    post_to_step,
    good,
    mock_good_attaching_put,
    mock_good_on_application_post,
    good_on_application,
    application_with_rfd_and_section_5_document,
    attach_product_on_application_summary_url,
    requests_mock,
    data_standard_case,
):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        }
    )
    good["good"]["firearm_details"].update(
        {
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "section_certificate_date_of_expiry": "2024-09-30",
            "section_certificate_missing": False,
            "section_certificate_missing_reason": "",
            "section_certificate_number": "5555",
        }
    )
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    requests_mock.get(url=url, json=good)

    post_application_document_matcher = requests_mock.post(
        f"/applications/{application['id']}/documents/",
        status_code=201,
        json={},
    )

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID,
        data={
            "is_rfd_certificate_valid": True,
        },
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmMadeBefore1938Form)

    response = post_to_step(
        AttachFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.YEAR_OF_MANUFACTURE,
        {"year_of_manufacture": 1937},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardExportedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardAlteredProcessedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardIncorporatedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_INCORPORATED,
        {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmIsDeactivatedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_DEACTIVATED,
        {"is_deactivated": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmDeactivationDetailsForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD,
        {
            "date_of_deactivation_0": "12",
            "date_of_deactivation_1": "11",
            "date_of_deactivation_2": "2007",
            "is_deactivated_to_standard": True,
        },
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductQuantityAndValueForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.QUANTITY_AND_VALUE,
        {"number_of_items": "2", "value": "16.32"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialIdentificationMarkingsForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "AVAILABLE"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialNumbersForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.SERIAL_NUMBERS,
        {
            "serial_numbers_0": "s111",
            "serial_numbers_1": "s222",
        },
    )

    assert response.status_code == 302
    assert response.url == f"{attach_product_on_application_summary_url}?confirmed_rfd_validity=True"

    assert mock_good_attaching_put.called_once
    assert mock_good_attaching_put.last_request.json() == {
        "firearm_details": {
            "is_rfd_certificate_valid": True,
        },
    }

    assert mock_good_on_application_post.last_request.json() == {
        "firearm_details": {
            "is_made_before_1938": True,
            "year_of_manufacture": 1937,
            "is_deactivated": True,
            "date_of_deactivation": "2007-11-12",
            "is_deactivated_to_standard": True,
            "not_deactivated_to_standard_comments": "",
            "number_of_items": "2",
            "serial_numbers_available": "AVAILABLE",
            "no_identification_markings_details": "",
            "serial_numbers": ["s111", "s222"],
        },
        "good_id": good["good"]["id"],
        "is_good_incorporated": True,
        "is_onward_exported": True,
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "processed comments",
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "incorporated comments",
        "quantity": "2",
        "unit": "NAR",
        "value": "16.32",
    }

    assert post_application_document_matcher.called_once
    assert post_application_document_matcher.last_request.json() == {
        "description": "Registered firearm dealer certificate",
        "document_type": OrganisationDocumentType.RFD_CERTIFICATE,
        "name": "rfd_certificate.txt",
        "s3_key": "rfd_certificate.txt.s3_key",
        "safe": True,
        "size": 3,
    }


def test_attach_firearm_to_application_end_to_end_section_5_good_without_section_5_details(
    application,
    post_to_step,
    good,
    mock_good_attaching_put,
    mock_good_on_application_post,
    good_on_application,
    application_with_rfd_and_section_5_document,
    attach_product_on_application_summary_url,
    requests_mock,
    data_standard_case,
):
    # There is a case where goods that were made prior to the firearm changes were saved without section 5 details.
    # In this case we will save the data back to the good to work around this.

    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        }
    )
    good["good"]["firearm_details"].update(
        {
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "section_certificate_date_of_expiry": None,
            "section_certificate_missing": None,
            "section_certificate_missing_reason": "",
            "section_certificate_number": None,
        }
    )
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    requests_mock.get(url=url, json=good)

    post_application_document_matcher = requests_mock.post(
        f"/applications/{application['id']}/documents/",
        status_code=201,
        json={},
    )

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID,
        data={
            "is_rfd_certificate_valid": True,
        },
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmMadeBefore1938Form)

    response = post_to_step(
        AttachFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.YEAR_OF_MANUFACTURE,
        {"year_of_manufacture": 1937},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardExportedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardAlteredProcessedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardIncorporatedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_INCORPORATED,
        {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmIsDeactivatedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_DEACTIVATED,
        {"is_deactivated": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmDeactivationDetailsForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD,
        {
            "date_of_deactivation_0": "12",
            "date_of_deactivation_1": "11",
            "date_of_deactivation_2": "2007",
            "is_deactivated_to_standard": True,
        },
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductQuantityAndValueForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.QUANTITY_AND_VALUE,
        {"number_of_items": "2", "value": "16.32"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialIdentificationMarkingsForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "AVAILABLE"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialNumbersForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.SERIAL_NUMBERS,
        {
            "serial_numbers_0": "s111",
            "serial_numbers_1": "s222",
        },
    )

    assert response.status_code == 302
    assert response.url == f"{attach_product_on_application_summary_url}?confirmed_rfd_validity=True"

    assert mock_good_attaching_put.called_once
    assert mock_good_attaching_put.last_request.json() == {
        "firearm_details": {
            "is_rfd_certificate_valid": True,
            "section_certificate_missing": False,
            "section_certificate_missing_reason": "",
            "section_certificate_number": "section 5 ref",
            "section_certificate_date_of_expiry": "2024-09-30",
        },
    }

    assert mock_good_on_application_post.last_request.json() == {
        "firearm_details": {
            "is_made_before_1938": True,
            "year_of_manufacture": 1937,
            "is_deactivated": True,
            "date_of_deactivation": "2007-11-12",
            "is_deactivated_to_standard": True,
            "not_deactivated_to_standard_comments": "",
            "number_of_items": "2",
            "serial_numbers_available": "AVAILABLE",
            "no_identification_markings_details": "",
            "serial_numbers": ["s111", "s222"],
        },
        "good_id": good["good"]["id"],
        "is_good_incorporated": True,
        "is_onward_exported": True,
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "processed comments",
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "incorporated comments",
        "quantity": "2",
        "unit": "NAR",
        "value": "16.32",
    }

    assert post_application_document_matcher.called_once
    assert post_application_document_matcher.last_request.json() == {
        "description": "Registered firearm dealer certificate",
        "document_type": OrganisationDocumentType.RFD_CERTIFICATE,
        "name": "rfd_certificate.txt",
        "s3_key": "rfd_certificate.txt.s3_key",
        "safe": True,
        "size": 3,
    }


def test_attach_firearm_to_application_end_to_end_section_5_good_without_section_5_details_and_without_section_5_certificate(
    application,
    post_to_step,
    good,
    mock_good_attaching_put,
    mock_good_on_application_post,
    good_on_application,
    application_with_organisation_rfd_document,
    attach_product_on_application_summary_url,
    requests_mock,
    data_standard_case,
):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        }
    )
    good["good"]["firearm_details"].update(
        {
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "section_certificate_date_of_expiry": None,
            "section_certificate_missing": None,
            "section_certificate_missing_reason": "",
            "section_certificate_number": None,
        }
    )
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    requests_mock.get(url=url, json=good)

    post_application_document_matcher = requests_mock.post(
        f"/applications/{application['id']}/documents/",
        status_code=201,
        json={},
    )

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_RFD_CERTIFICATE_VALID,
        data={
            "is_rfd_certificate_valid": True,
        },
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmMadeBefore1938Form)

    response = post_to_step(
        AttachFirearmToApplicationSteps.MADE_BEFORE_1938,
        {"is_made_before_1938": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.YEAR_OF_MANUFACTURE,
        {"year_of_manufacture": 1937},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardExportedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_EXPORTED,
        {"is_onward_exported": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardAlteredProcessedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        {"is_onward_altered_processed": True, "is_onward_altered_processed_comments": "processed comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductOnwardIncorporatedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.ONWARD_INCORPORATED,
        {"is_onward_incorporated": True, "is_onward_incorporated_comments": "incorporated comments"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmIsDeactivatedForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_DEACTIVATED,
        {"is_deactivated": True},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmDeactivationDetailsForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD,
        {
            "date_of_deactivation_0": "12",
            "date_of_deactivation_1": "11",
            "date_of_deactivation_2": "2007",
            "is_deactivated_to_standard": True,
        },
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], ProductQuantityAndValueForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.QUANTITY_AND_VALUE,
        {"number_of_items": "2", "value": "16.32"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialIdentificationMarkingsForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        {"serial_numbers_available": "AVAILABLE"},
    )
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert isinstance(response.context["form"], FirearmSerialNumbersForm)

    response = post_to_step(
        AttachFirearmToApplicationSteps.SERIAL_NUMBERS,
        {
            "serial_numbers_0": "s111",
            "serial_numbers_1": "s222",
        },
    )

    assert response.status_code == 302
    assert response.url == f"{attach_product_on_application_summary_url}?confirmed_rfd_validity=True"

    assert mock_good_attaching_put.called_once
    assert mock_good_attaching_put.last_request.json() == {
        "firearm_details": {
            "is_rfd_certificate_valid": True,
        },
    }

    assert mock_good_on_application_post.last_request.json() == {
        "firearm_details": {
            "is_made_before_1938": True,
            "year_of_manufacture": 1937,
            "is_deactivated": True,
            "date_of_deactivation": "2007-11-12",
            "is_deactivated_to_standard": True,
            "not_deactivated_to_standard_comments": "",
            "number_of_items": "2",
            "serial_numbers_available": "AVAILABLE",
            "no_identification_markings_details": "",
            "serial_numbers": ["s111", "s222"],
        },
        "good_id": good["good"]["id"],
        "is_good_incorporated": True,
        "is_onward_exported": True,
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "processed comments",
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "incorporated comments",
        "quantity": "2",
        "unit": "NAR",
        "value": "16.32",
    }

    assert post_application_document_matcher.called_once
    assert post_application_document_matcher.last_request.json() == {
        "description": "Registered firearm dealer certificate",
        "document_type": OrganisationDocumentType.RFD_CERTIFICATE,
        "name": "rfd_certificate.txt",
        "s3_key": "rfd_certificate.txt.s3_key",
        "safe": True,
        "size": 3,
    }
