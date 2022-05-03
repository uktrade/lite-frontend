import datetime
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from exporter.applications.views.goods.add_good_firearm.views.constants import AddGoodFirearmSteps
from exporter.core.helpers import decompose_date
from exporter.goods.forms.firearms import (
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmSection5Form,
)


@pytest.fixture(autouse=True)
def setup(settings, no_op_storage):
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.fixture
def edit_url(data_standard_case):
    application_id = data_standard_case["case"]["data"]["id"]
    good = data_standard_case["case"]["data"]["goods"][0]["good"]

    return reverse(
        "applications:firearm_edit_section_5_firearms_act_1968",
        kwargs={"pk": application_id, "good_pk": good["id"]},
    )


@pytest.fixture
def goto_step(goto_step_factory, edit_url):
    return goto_step_factory(edit_url)


@pytest.fixture
def post_to_step(post_to_step_factory, edit_url):
    return post_to_step_factory(edit_url)


def test_edit_section_5_firearms_act_set_yes_without_document(
    data_standard_case,
    application_without_rfd_document,
    mock_good_get,
    mock_good_put,
    post_to_step,
    edit_url,
    authorized_client,
    product_summary_url,
    requests_mock,
    good_id,
):
    post_applications_document_matcher = requests_mock.post(
        f"/applications/{data_standard_case['case']['id']}/documents/",
        status_code=201,
        json={},
    )

    response = authorized_client.get(edit_url)
    assert isinstance(response.context["form"], FirearmSection5Form)

    response = post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {
            "is_covered_by_section_5": "yes",
        },
    )
    assert isinstance(response.context["form"], FirearmAttachSection5LetterOfAuthorityForm)

    section_5_letter_expiry_date = datetime.date.today() + datetime.timedelta(days=10)
    response = post_to_step(
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY,
        {
            "file": SimpleUploadedFile("letter_of_authority.pdf", b"This is the letter of authority"),
            "section_certificate_number": "12345",
            **decompose_date("section_certificate_date_of_expiry", section_5_letter_expiry_date),
        },
    )

    assert response.status_code == 302
    assert response.url == product_summary_url

    assert mock_good_put.last_request.json() == {
        "firearm_details": {
            "firearms_act_section": "firearms_act_section5",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "section_certificate_date_of_expiry": section_5_letter_expiry_date.isoformat(),
            "section_certificate_missing": False,
            "section_certificate_number": "12345",
        },
    }

    assert post_applications_document_matcher.called_once
    assert post_applications_document_matcher.last_request.json() == {
        "description": "Letter of authority for 'p1'",
        "document_on_organisation": {
            "document_type": "section-five-certificate",
            "expiry_date": section_5_letter_expiry_date.isoformat(),
            "reference_code": "12345",
        },
        "document_type": "section-five-certificate",
        "name": "letter_of_authority.pdf",
        "s3_key": "letter_of_authority.pdf",
        "size": 0,
    }


def test_edit_section_5_firearms_act_set_yes_with_document(
    data_standard_case,
    application_with_rfd_and_section_5_document,
    mock_good_get,
    mock_good_put,
    post_to_step,
    edit_url,
    authorized_client,
    product_summary_url,
    requests_mock,
    good_id,
):
    response = authorized_client.get(edit_url)
    assert isinstance(response.context["form"], FirearmSection5Form)

    response = post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {
            "is_covered_by_section_5": "yes",
        },
    )

    assert response.status_code == 302
    assert response.url == product_summary_url

    assert mock_good_put.last_request.json() == {
        "firearm_details": {
            "firearms_act_section": "firearms_act_section5",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "section_certificate_date_of_expiry": "2024-09-30",
            "section_certificate_missing": False,
            "section_certificate_number": "section 5 ref",
        },
    }


def test_edit_section_5_firearms_act_set_no(
    data_standard_case,
    application_with_rfd_and_section_5_document,
    mock_good_get,
    mock_good_put,
    post_to_step,
    edit_url,
    authorized_client,
    product_summary_url,
    requests_mock,
    good_id,
):
    response = authorized_client.get(edit_url)
    assert isinstance(response.context["form"], FirearmSection5Form)

    response = post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {
            "is_covered_by_section_5": "no",
        },
    )

    assert response.status_code == 302
    assert response.url == product_summary_url

    assert mock_good_put.last_request.json() == {
        "firearm_details": {
            "is_covered_by_firearm_act_section_one_two_or_five": "No",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
        },
    }


def test_edit_section_5_firearms_act_set_dont_know(
    data_standard_case,
    application_with_rfd_and_section_5_document,
    mock_good_get,
    mock_good_put,
    post_to_step,
    edit_url,
    authorized_client,
    product_summary_url,
    requests_mock,
    good_id,
):
    response = authorized_client.get(edit_url)
    assert isinstance(response.context["form"], FirearmSection5Form)

    response = post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {
            "is_covered_by_section_5": "dont_know",
        },
    )

    assert response.status_code == 302
    assert response.url == product_summary_url

    assert mock_good_put.last_request.json() == {
        "firearm_details": {
            "is_covered_by_firearm_act_section_one_two_or_five": "Unsure",
        },
    }
