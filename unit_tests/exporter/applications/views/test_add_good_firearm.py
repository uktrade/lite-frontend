import datetime
import pytest
import uuid

from pytest_django.asserts import assertContains

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from core import client
from exporter.core.constants import AddGoodFormSteps
from exporter.core.helpers import decompose_date
from exporter.applications.views.goods.add_good_firearm.views.constants import AddGoodFirearmSteps
from exporter.goods.forms.firearms import (
    FirearmAttachRFDCertificate,
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmCategoryForm,
    FirearmDocumentAvailability,
    FirearmDocumentSensitivityForm,
    FirearmDocumentUploadForm,
    FirearmFirearmAct1968Form,
    FirearmRegisteredFirearmsDealerForm,
    FirearmRFDValidityForm,
    FirearmSection5Form,
)


@pytest.fixture(autouse=True)
def setup(no_op_storage):
    pass


@pytest.fixture
def new_good_url(data_standard_case):
    return reverse("applications:new_good", kwargs={"pk": data_standard_case["case"]["id"]})


@pytest.fixture
def new_good_firearm_url(data_standard_case):
    return reverse(
        "applications:new_good_firearm",
        kwargs={
            "pk": data_standard_case["case"]["id"],
        },
    )


@pytest.fixture(autouse=True)
def set_feature_flags(settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS = True
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.fixture
def control_list_entries(requests_mock):
    clc_url = client._build_absolute_uri("/static/control-list-entries/")
    matcher = requests_mock.get(url=clc_url, json={"control_list_entries": [{"rating": "ML1"}, {"rating": "ML1a"}]})
    return matcher


@pytest.fixture
def good_id():
    return str(uuid.uuid4())


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


def test_firearm_category_redirects_to_new_wizard(
    authorized_client,
    new_good_firearm_url,
    new_good_url,
    application,
    control_list_entries,
):
    response = authorized_client.post(new_good_url, data={"wizard_goto_step": AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE})
    response = authorized_client.post(
        new_good_url,
        data={
            f"add_good-current_step": AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE,
            f"{AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE}-type": "firearms",
        },
    )

    assert response.status_code == 302
    assert response.url == new_good_firearm_url


def test_add_good_firearm_access_denied_without_feature_flag(
    settings,
    authorized_client,
    new_good_firearm_url,
):
    settings.FEATURE_FLAG_PRODUCT_2_0 = False
    response = authorized_client.get(new_good_firearm_url)
    assert response.status_code == 404


def test_add_good_firearm_invalid_application(
    data_standard_case, requests_mock, authorized_client, new_good_firearm_url
):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=app_url, status_code=404)
    response = authorized_client.get(new_good_firearm_url)
    assert response.status_code == 404


def test_add_good_firearm_start(authorized_client, new_good_firearm_url, new_good_url, application):
    response = authorized_client.get(new_good_firearm_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmCategoryForm)
    assert response.context["back_link_url"] == new_good_url
    assert response.context["title"] == "Firearm category"


@pytest.fixture
def goto_step(goto_step_factory, new_good_firearm_url):
    return goto_step_factory(new_good_firearm_url)


@pytest.fixture
def post_to_step(post_to_step_factory, new_good_firearm_url):
    return post_to_step_factory(new_good_firearm_url)


def test_add_good_firearm_displays_rfd_validity_step(
    application_with_organisation_rfd_document, rfd_certificate, goto_step, post_to_step
):
    goto_step(AddGoodFirearmSteps.IS_REPLICA)
    response = post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmRFDValidityForm)
    rfd_certificate_url = reverse("organisation:document", kwargs={"pk": rfd_certificate["id"]})
    assertContains(response, rfd_certificate_url)
    rfd_certificate_name = rfd_certificate["document"]["name"]
    assertContains(response, rfd_certificate_name)


def test_add_good_firearm_skips_rfd_validity_step_if_application_already_has_rfd_document(
    application_with_organisation_and_application_rfd_document, rfd_certificate, goto_step, post_to_step
):
    goto_step(AddGoodFirearmSteps.IS_REPLICA)
    response = post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmSection5Form)


def test_add_good_firearm_skips_rfd_validity_step(application_without_rfd_document, goto_step, post_to_step):
    goto_step(AddGoodFirearmSteps.IS_REPLICA)
    response = post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmRegisteredFirearmsDealerForm)


def test_add_good_firearm_shows_registered_firearms_step_after_confirming_certificate_invalid(
    application_with_organisation_rfd_document, rfd_certificate, goto_step, post_to_step
):
    goto_step(AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID)
    response = post_to_step(AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID, {"is_rfd_certificate_valid": False})

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmRegisteredFirearmsDealerForm)


def test_add_good_firearm_shows_registered_firearms_step_after_confirming_certificate_valid(
    application_with_organisation_rfd_document, rfd_certificate, goto_step, post_to_step
):
    goto_step(AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID)
    response = post_to_step(AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID, {"is_rfd_certificate_valid": True})

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmSection5Form)


def test_add_good_firearm_shows_upload_rfd_step_after_confirmed_as_registered_firearms_dealer(
    application_without_rfd_document, goto_step, post_to_step
):
    goto_step(AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER)
    response = post_to_step(AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER, {"is_registered_firearm_dealer": True})

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmAttachRFDCertificate)


def test_add_good_firearm_product_document_not_available(
    application_with_organisation_rfd_document, goto_step, post_to_step
):
    goto_step(AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY)
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": False, "no_document_comments": "product not manufactured yet"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmCategoryForm)


def test_add_good_firearm_product_document_available_but_sensitive(
    application_with_organisation_rfd_document, goto_step, post_to_step
):
    goto_step(AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY)
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": True},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmDocumentSensitivityForm)

    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        {"is_document_sensitive": True},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmCategoryForm)


def test_add_good_firearm_product_document_available_but_not_sensitive(
    application_with_organisation_rfd_document, goto_step, post_to_step
):
    goto_step(AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY)
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": True},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmDocumentSensitivityForm)

    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        {"is_document_sensitive": False},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmDocumentUploadForm)

    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD,
        {"product_document": SimpleUploadedFile("data sheet", b"This is a detailed spec of this Rifle")},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmCategoryForm)


def test_add_good_firearm_not_registered_firearm_dealer(
    application_without_rfd_document,
    goto_step,
    post_to_step,
):
    goto_step(AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER)
    response = post_to_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
        {"is_registered_firearm_dealer": False},
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmFirearmAct1968Form)


@pytest.mark.parametrize(
    "form_data, expected_next_form",
    (
        (
            {"firearms_act_section": "dont_know", "not_covered_explanation": "explanation"},
            FirearmDocumentAvailability,
        ),
        (
            {"firearms_act_section": "firearms_act_section1"},
            FirearmDocumentAvailability,
        ),
        (
            {"firearms_act_section": "firearms_act_section2"},
            FirearmDocumentAvailability,
        ),
        (
            {"firearms_act_section": "firearms_act_section5"},
            FirearmAttachSection5LetterOfAuthorityForm,
        ),
    ),
)
def test_add_good_firearm_act_selection(
    application_without_rfd_document,
    goto_step,
    post_to_step,
    form_data,
    expected_next_form,
):
    goto_step(AddGoodFirearmSteps.FIREARM_ACT_1968)
    response = post_to_step(
        AddGoodFirearmSteps.FIREARM_ACT_1968,
        form_data,
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], expected_next_form)


@pytest.fixture
def application_with_document(data_standard_case, requests_mock, document_type):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    case = data_standard_case["case"]
    case["organisation"] = {
        "documents": [
            {
                "id": str(uuid.uuid4()),
                "document": {
                    "name": f"{document_type}.txt",
                },
                "document_type": document_type,
                "is_expired": False,
            }
        ],
    }
    matcher = requests_mock.get(url=app_url, json=case)
    return matcher


@pytest.mark.parametrize(
    "form_data, document_type",
    (
        (
            {"firearms_act_section": "firearms_act_section1"},
            "section-one-certificate",
        ),
        (
            {"firearms_act_section": "firearms_act_section2"},
            "section-two-certificate",
        ),
        (
            {"firearms_act_section": "firearms_act_section5"},
            "section-five-certificate",
        ),
    ),
)
def test_add_good_firearm_act_selection_skips_when_valid_certificate_already_exists(
    goto_step,
    post_to_step,
    form_data,
    application_with_document,
):
    goto_step(AddGoodFirearmSteps.FIREARM_ACT_1968)
    response = post_to_step(
        AddGoodFirearmSteps.FIREARM_ACT_1968,
        form_data,
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmDocumentAvailability)


def test_add_good_firearm_with_rfd_document_submission(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
    pv_gradings,
    application_with_organisation_rfd_document,
    good_id,
    post_goods_matcher,
):
    authorized_client.get(new_good_firearm_url)

    post_good_document_matcher = requests_mock.post(
        f"/goods/{good_id}/documents/",
        status_code=201,
        json={},
    )

    post_applications_document_matcher = requests_mock.post(
        f"/applications/{data_standard_case['case']['id']}/documents/",
        status_code=201,
        json={},
    )

    post_to_step(
        AddGoodFirearmSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    post_to_step(
        AddGoodFirearmSteps.NAME,
        {"name": "TEST NAME"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": True},
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING_DETAILS,
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
    post_to_step(
        AddGoodFirearmSteps.CALIBRE,
        {"calibre": "calibre 123"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID,
        {"is_rfd_certificate_valid": True},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {"is_covered_by_section_5": "no"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": True},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        {"is_document_sensitive": False},
    )
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD,
        {"product_document": SimpleUploadedFile("data sheet", b"This is a detailed spec of this Rifle")},
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "applications:product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "firearm_details": {
            "calibre": "calibre 123",
            "category": ["NON_AUTOMATIC_SHOTGUN"],
            "is_covered_by_firearm_act_section_one_two_or_five": "No",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "is_replica": True,
            "is_rfd_certificate_valid": True,
            "replica_description": "This is a replica",
            "type": "firearms",
        },
        "control_list_entries": ["ML1", "ML1a"],
        "name": "TEST NAME",
        "is_good_controlled": True,
        "is_pv_graded": "yes",
        "pv_grading_details": {
            "prefix": "NATO",
            "grading": "official",
            "suffix": "",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue": "2020-02-20",
        },
        "item_category": "group2_firearms",
        "is_document_available": True,
        "no_document_comments": "",
        "is_document_sensitive": False,
    }

    assert post_good_document_matcher.called_once
    good_doc_request = post_good_document_matcher.last_request
    assert good_doc_request.json() == [{"name": "data sheet", "s3_key": "data sheet", "size": 0, "description": ""}]

    assert post_applications_document_matcher.called_once
    application_doc_request = post_applications_document_matcher.last_request
    assert application_doc_request.json() == {
        "description": "Registered firearm dealer certificate",
        "document_type": "rfd-certificate",
        "name": "rfd_certificate.txt",
        "s3_key": "rfd_certificate.txt.s3_key",
        "safe": True,
        "size": 3,
    }


def test_add_good_firearm_with_rfd_document_marked_as_invalid_submission(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
    pv_gradings,
    application_with_organisation_rfd_document,
    good_id,
    rfd_certificate,
    post_goods_matcher,
):
    authorized_client.get(new_good_firearm_url)

    document_id = rfd_certificate["id"]
    organisation_id = rfd_certificate["organisation"]
    post_applications_document_matcher = requests_mock.delete(
        f"/organisations/{organisation_id}/document/{document_id}/",
        status_code=204,
        json={},
    )

    post_to_step(
        AddGoodFirearmSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    post_to_step(
        AddGoodFirearmSteps.NAME,
        {"name": "TEST NAME"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": True},
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING_DETAILS,
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
    post_to_step(
        AddGoodFirearmSteps.CALIBRE,
        {"calibre": "calibre 123"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID,
        {"is_rfd_certificate_valid": False},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
        {"is_registered_firearm_dealer": False},
    )
    post_to_step(
        AddGoodFirearmSteps.FIREARM_ACT_1968,
        {"firearms_act_section": "dont_know", "not_covered_explanation": "not covered"},
    )
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": False, "no_document_comments": "product not manufactured yet"},
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "applications:product_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "firearm_details": {
            "calibre": "calibre 123",
            "category": ["NON_AUTOMATIC_SHOTGUN"],
            "is_covered_by_firearm_act_section_one_two_or_five": "Unsure",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "not covered",
            "is_registered_firearm_dealer": False,
            "is_replica": True,
            "is_rfd_certificate_valid": False,
            "replica_description": "This is a replica",
            "type": "firearms",
        },
        "control_list_entries": ["ML1", "ML1a"],
        "name": "TEST NAME",
        "is_good_controlled": True,
        "is_pv_graded": "yes",
        "pv_grading_details": {
            "prefix": "NATO",
            "grading": "official",
            "suffix": "",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue": "2020-02-20",
        },
        "item_category": "group2_firearms",
        "is_document_available": False,
        "no_document_comments": "product not manufactured yet",
    }

    assert post_applications_document_matcher.called_once


def test_add_good_firearm_without_rfd_document_submission_registered_firearms_dealer(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
    application_without_rfd_document,
    application,
    product_summary_url,
    good_id,
    post_goods_matcher,
):
    authorized_client.get(new_good_firearm_url)

    post_additional_document_matcher = requests_mock.post(
        f"/applications/{data_standard_case['case']['id']}/documents/",
        status_code=201,
        json={},
    )

    post_to_step(
        AddGoodFirearmSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    post_to_step(
        AddGoodFirearmSteps.NAME,
        {"name": "TEST NAME"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": False},
    )
    post_to_step(
        AddGoodFirearmSteps.CALIBRE,
        {"calibre": "calibre 123"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
        {"is_registered_firearm_dealer": True},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {"is_covered_by_section_5": "no"},
    )
    expiry_date = datetime.date.today() + datetime.timedelta(days=5)
    file_name = "test"
    post_to_step(
        AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE,
        {
            "reference_code": "12345",
            "file": SimpleUploadedFile(file_name, b"test content"),
            **decompose_date("expiry_date", expiry_date),
        },
    )
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": False, "no_document_comments": "product not manufactured yet"},
    )

    assert response.status_code == 302
    assert response.url == product_summary_url

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "firearm_details": {
            "calibre": "calibre 123",
            "category": ["NON_AUTOMATIC_SHOTGUN"],
            "is_covered_by_firearm_act_section_one_two_or_five": "No",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "is_registered_firearm_dealer": True,
            "is_replica": True,
            "replica_description": "This is a replica",
            "type": "firearms",
        },
        "control_list_entries": ["ML1", "ML1a"],
        "name": "TEST NAME",
        "is_good_controlled": True,
        "is_pv_graded": "no",
        "item_category": "group2_firearms",
        "is_document_available": False,
        "no_document_comments": "product not manufactured yet",
    }

    assert post_additional_document_matcher.called_once
    last_request = post_additional_document_matcher.last_request
    assert last_request.json() == {
        "description": "Registered firearm dealer certificate",
        "document_on_organisation": {
            "expiry_date": expiry_date.isoformat(),
            "reference_code": "12345",
            "document_type": "rfd-certificate",
        },
        "document_type": "rfd-certificate",
        "name": file_name,
        "s3_key": file_name,
        "size": 0,
    }


def test_add_good_firearm_without_rfd_document_submission_not_registered_firearms_dealer(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
    application_without_rfd_document,
    application,
    good_id,
    product_summary_url,
    post_goods_matcher,
):
    authorized_client.get(new_good_firearm_url)

    post_to_step(
        AddGoodFirearmSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    post_to_step(
        AddGoodFirearmSteps.NAME,
        {"name": "TEST NAME"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": False},
    )
    post_to_step(
        AddGoodFirearmSteps.CALIBRE,
        {"calibre": "calibre 123"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
        {"is_registered_firearm_dealer": False},
    )
    post_to_step(
        AddGoodFirearmSteps.FIREARM_ACT_1968,
        {
            "firearms_act_section": "dont_know",
            "not_covered_explanation": "firearms act not covered explanation",
        },
    )
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": False, "no_document_comments": "product not manufactured yet"},
    )

    assert response.status_code == 302
    assert response.url == product_summary_url

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "firearm_details": {
            "calibre": "calibre 123",
            "category": ["NON_AUTOMATIC_SHOTGUN"],
            "is_registered_firearm_dealer": False,
            "is_replica": True,
            "replica_description": "This is a replica",
            "type": "firearms",
            "is_covered_by_firearm_act_section_one_two_or_five": "Unsure",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "firearms act not covered explanation",
        },
        "control_list_entries": ["ML1", "ML1a"],
        "name": "TEST NAME",
        "is_good_controlled": True,
        "is_pv_graded": "no",
        "item_category": "group2_firearms",
        "is_document_available": False,
        "no_document_comments": "product not manufactured yet",
    }


def test_add_good_firearm_without_rfd_document_submission_not_registered_firearms_dealer_section_1(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
    application_without_rfd_document,
    application,
    good_id,
    product_summary_url,
    post_goods_matcher,
):
    authorized_client.get(new_good_firearm_url)

    post_to_step(
        AddGoodFirearmSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    post_to_step(
        AddGoodFirearmSteps.NAME,
        {"name": "TEST NAME"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": False},
    )
    post_to_step(
        AddGoodFirearmSteps.CALIBRE,
        {"calibre": "calibre 123"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
        {"is_registered_firearm_dealer": False},
    )
    post_to_step(
        AddGoodFirearmSteps.FIREARM_ACT_1968,
        {"firearms_act_section": "firearms_act_section1"},
    )
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": False, "no_document_comments": "product not manufactured yet"},
    )
    assert response.status_code == 302
    assert response.url == product_summary_url

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "firearm_details": {
            "calibre": "calibre 123",
            "category": ["NON_AUTOMATIC_SHOTGUN"],
            "firearms_act_section": "firearms_act_section1",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_registered_firearm_dealer": False,
            "is_replica": True,
            "replica_description": "This is a replica",
            "type": "firearms",
        },
        "control_list_entries": ["ML1", "ML1a"],
        "name": "TEST NAME",
        "is_good_controlled": True,
        "is_pv_graded": "no",
        "item_category": "group2_firearms",
        "is_document_available": False,
        "no_document_comments": "product not manufactured yet",
    }


def test_add_good_firearm_without_rfd_document_submission_not_registered_firearms_dealer_section_2(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
    application_without_rfd_document,
    application,
    good_id,
    product_summary_url,
    post_goods_matcher,
):
    authorized_client.get(new_good_firearm_url)

    post_to_step(
        AddGoodFirearmSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    post_to_step(
        AddGoodFirearmSteps.NAME,
        {"name": "TEST NAME"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": False},
    )
    post_to_step(
        AddGoodFirearmSteps.CALIBRE,
        {"calibre": "calibre 123"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
        {"is_registered_firearm_dealer": False},
    )
    post_to_step(
        AddGoodFirearmSteps.FIREARM_ACT_1968,
        {"firearms_act_section": "firearms_act_section2"},
    )
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": False, "no_document_comments": "product not manufactured yet"},
    )
    assert response.status_code == 302
    assert response.url == product_summary_url

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "firearm_details": {
            "calibre": "calibre 123",
            "category": ["NON_AUTOMATIC_SHOTGUN"],
            "firearms_act_section": "firearms_act_section2",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_registered_firearm_dealer": False,
            "is_replica": True,
            "replica_description": "This is a replica",
            "type": "firearms",
        },
        "control_list_entries": ["ML1", "ML1a"],
        "name": "TEST NAME",
        "is_good_controlled": True,
        "is_pv_graded": "no",
        "item_category": "group2_firearms",
        "is_document_available": False,
        "no_document_comments": "product not manufactured yet",
    }


def test_add_good_firearm_without_rfd_document_submission_not_registered_firearms_dealer_section_5(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
    application_without_rfd_document,
    application,
    good_id,
    product_summary_url,
    post_goods_matcher,
):
    authorized_client.get(new_good_firearm_url)

    post_application_document_matcher = requests_mock.post(
        f"/applications/{data_standard_case['case']['id']}/documents/",
        status_code=201,
        json={},
    )

    post_to_step(
        AddGoodFirearmSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    post_to_step(
        AddGoodFirearmSteps.NAME,
        {"name": "TEST NAME"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": False},
    )
    post_to_step(
        AddGoodFirearmSteps.CALIBRE,
        {"calibre": "calibre 123"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
        {"is_registered_firearm_dealer": False},
    )
    post_to_step(
        AddGoodFirearmSteps.FIREARM_ACT_1968,
        {"firearms_act_section": "firearms_act_section5"},
    )
    certificate_expiry_date = datetime.date.today() + datetime.timedelta(days=5)
    post_to_step(
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY,
        {
            "file": SimpleUploadedFile("letter_of_authority.pdf", b"This is the letter of authority"),
            "section_certificate_number": "12345",
            **decompose_date("section_certificate_date_of_expiry", certificate_expiry_date),
        },
    )
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": False, "no_document_comments": "product not manufactured yet"},
    )
    assert response.status_code == 302
    assert response.url == product_summary_url

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "firearm_details": {
            "calibre": "calibre 123",
            "category": ["NON_AUTOMATIC_SHOTGUN"],
            "firearms_act_section": "firearms_act_section5",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_registered_firearm_dealer": False,
            "is_replica": True,
            "replica_description": "This is a replica",
            "section_certificate_date_of_expiry": certificate_expiry_date.isoformat(),
            "section_certificate_missing": False,
            "section_certificate_number": "12345",
            "type": "firearms",
        },
        "control_list_entries": ["ML1", "ML1a"],
        "name": "TEST NAME",
        "is_good_controlled": True,
        "is_pv_graded": "no",
        "item_category": "group2_firearms",
        "is_document_available": False,
        "no_document_comments": "product not manufactured yet",
    }

    assert post_application_document_matcher.called_once
    last_request = post_application_document_matcher.last_request
    assert last_request.json() == {
        "description": "Letter of authority for 'p1'",
        "document_on_organisation": {
            "document_type": "section-five-certificate",
            "expiry_date": certificate_expiry_date.isoformat(),
            "reference_code": "12345",
        },
        "document_type": "section-five-certificate",
        "name": "letter_of_authority.pdf",
        "s3_key": "letter_of_authority.pdf",
        "size": 0,
    }


def test_add_good_firearm_with_rfd_document_submission_section_5(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
    application_with_organisation_rfd_document,
    rfd_certificate,
    application,
    good_id,
    product_summary_url,
    post_goods_matcher,
):
    authorized_client.get(new_good_firearm_url)

    post_applications_document_matcher = requests_mock.post(
        f"/applications/{data_standard_case['case']['id']}/documents/",
        status_code=201,
        json={},
    )

    post_to_step(
        AddGoodFirearmSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    post_to_step(
        AddGoodFirearmSteps.NAME,
        {"name": "TEST NAME"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": False},
    )
    post_to_step(
        AddGoodFirearmSteps.CALIBRE,
        {"calibre": "calibre 123"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID,
        {"is_rfd_certificate_valid": True},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {"is_covered_by_section_5": "yes"},
    )
    certificate_expiry_date = datetime.date.today() + datetime.timedelta(days=5)
    post_to_step(
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY,
        {
            "file": SimpleUploadedFile("letter_of_authority.pdf", b"This is the letter of authority"),
            "section_certificate_number": "12345",
            **decompose_date("section_certificate_date_of_expiry", certificate_expiry_date),
        },
    )
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": False, "no_document_comments": "product not manufactured yet"},
    )
    assert response.status_code == 302
    assert response.url == product_summary_url

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "firearm_details": {
            "calibre": "calibre 123",
            "category": ["NON_AUTOMATIC_SHOTGUN"],
            "firearms_act_section": "firearms_act_section5",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "is_replica": True,
            "is_rfd_certificate_valid": True,
            "replica_description": "This is a replica",
            "section_certificate_date_of_expiry": certificate_expiry_date.isoformat(),
            "section_certificate_missing": False,
            "section_certificate_number": "12345",
            "type": "firearms",
        },
        "control_list_entries": ["ML1", "ML1a"],
        "name": "TEST NAME",
        "is_good_controlled": True,
        "is_pv_graded": "no",
        "item_category": "group2_firearms",
        "is_document_available": False,
        "no_document_comments": "product not manufactured yet",
    }

    assert post_applications_document_matcher.call_count == 2

    assert post_applications_document_matcher.request_history[0].json() == {
        "description": "Registered firearm dealer certificate",
        "document_type": "rfd-certificate",
        "name": "rfd_certificate.txt",
        "s3_key": "rfd_certificate.txt.s3_key",
        "safe": True,
        "size": 3,
    }

    assert post_applications_document_matcher.request_history[1].json() == {
        "description": "Letter of authority for 'p1'",
        "document_on_organisation": {
            "document_type": "section-five-certificate",
            "expiry_date": certificate_expiry_date.isoformat(),
            "reference_code": "12345",
        },
        "document_type": "section-five-certificate",
        "name": "letter_of_authority.pdf",
        "s3_key": "letter_of_authority.pdf",
        "size": 0,
    }


def test_add_good_firearm_with_rfd_document_submission_section_5_with_current_section_5(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
    application_with_rfd_and_section_5_document,
    rfd_certificate,
    application,
    good_id,
    product_summary_url,
    post_goods_matcher,
):
    authorized_client.get(new_good_firearm_url)

    post_applications_document_matcher = requests_mock.post(
        f"/applications/{data_standard_case['case']['id']}/documents/",
        status_code=201,
        json={},
    )

    post_to_step(
        AddGoodFirearmSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    post_to_step(
        AddGoodFirearmSteps.NAME,
        {"name": "TEST NAME"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": False},
    )
    post_to_step(
        AddGoodFirearmSteps.CALIBRE,
        {"calibre": "calibre 123"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID,
        {"is_rfd_certificate_valid": True},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {"is_covered_by_section_5": "yes"},
    )
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": False, "no_document_comments": "product not manufactured yet"},
    )
    assert response.status_code == 302
    assert response.url == product_summary_url

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "firearm_details": {
            "calibre": "calibre 123",
            "category": ["NON_AUTOMATIC_SHOTGUN"],
            "firearms_act_section": "firearms_act_section5",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "is_replica": True,
            "is_rfd_certificate_valid": True,
            "replica_description": "This is a replica",
            "section_certificate_date_of_expiry": "2024-09-30",
            "section_certificate_missing": False,
            "section_certificate_number": "section 5 ref",
            "type": "firearms",
        },
        "control_list_entries": ["ML1", "ML1a"],
        "name": "TEST NAME",
        "is_good_controlled": True,
        "is_pv_graded": "no",
        "item_category": "group2_firearms",
        "is_document_available": False,
        "no_document_comments": "product not manufactured yet",
    }

    assert post_applications_document_matcher.called_once
    application_doc_request = post_applications_document_matcher.last_request
    assert application_doc_request.json() == {
        "description": "Registered firearm dealer certificate",
        "document_type": "rfd-certificate",
        "name": "rfd_certificate.txt",
        "s3_key": "rfd_certificate.txt.s3_key",
        "safe": True,
        "size": 3,
    }


def test_add_good_firearm_submission_error(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
    application_with_organisation_rfd_document,
):
    authorized_client.get(new_good_firearm_url)

    requests_mock.post(
        f"/goods/",
        status_code=400,
        json={},
    )

    post_to_step(
        AddGoodFirearmSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    post_to_step(
        AddGoodFirearmSteps.NAME,
        {"name": "TEST NAME"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": False},
    )
    post_to_step(
        AddGoodFirearmSteps.CALIBRE,
        {"calibre": "calibre 123"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID,
        {"is_rfd_certificate_valid": True},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {"is_covered_by_section_5": "no"},
    )
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        {"is_document_available": False, "no_document_comments": "product not manufactured yet"},
    )

    assert response.status_code == 200
    assertContains(response, "Unexpected error adding firearm", html=True)
