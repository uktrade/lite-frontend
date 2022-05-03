import datetime
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from exporter.core.helpers import decompose_date
from exporter.goods.forms.firearms import (
    FirearmAttachFirearmCertificateForm,
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmAttachShotgunCertificateForm,
)


@pytest.fixture(autouse=True)
def setup(settings, no_op_storage):
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.mark.parametrize(
    "url_name, form_class",
    (("firearm_edit_letter_of_authority", FirearmAttachSection5LetterOfAuthorityForm),),
)
def test_edit_certificate_view_exists(
    data_standard_case,
    application_without_rfd_document,
    mock_good_get,
    authorized_client,
    url_name,
    form_class,
):
    application_id = data_standard_case["case"]["data"]["id"]
    good = data_standard_case["case"]["data"]["goods"][0]["good"]

    url = reverse(f"applications:{url_name}", kwargs={"pk": application_id, "good_pk": good["id"]})
    response = authorized_client.get(url)
    assert response.status_code == 200

    form = response.context["form"]
    assert isinstance(form, form_class)


@pytest.mark.parametrize(
    "url_name, certificate_type",
    (("firearm_edit_letter_of_authority", "section-five-certificate"),),
)
def test_edit_certificate_submission_success(
    data_standard_case,
    application_without_rfd_document,
    mock_good_get,
    mock_good_put,
    authorized_client,
    url_name,
    product_summary_url,
    requests_mock,
    certificate_type,
):
    application_id = data_standard_case["case"]["data"]["id"]
    good = data_standard_case["case"]["data"]["goods"][0]["good"]

    post_applications_document_matcher = requests_mock.post(
        f"/applications/{data_standard_case['case']['id']}/documents/",
        status_code=201,
        json={},
    )

    certificate_expiry_date = datetime.date.today() + datetime.timedelta(days=5)

    url = reverse(f"applications:{url_name}", kwargs={"pk": application_id, "good_pk": good["id"]})
    post_data = {
        "file": SimpleUploadedFile(f"{certificate_type}.pdf", b"This is the firearm certificate"),
        "section_certificate_number": "12345",
        **decompose_date("section_certificate_date_of_expiry", certificate_expiry_date),
    }
    response = authorized_client.post(url, data=post_data)

    assert response.status_code == 302
    assert response.url == product_summary_url

    assert mock_good_put.called_once
    assert mock_good_put.last_request.json() == {
        "firearm_details": {
            "section_certificate_date_of_expiry": certificate_expiry_date.isoformat(),
            "section_certificate_missing": False,
            "section_certificate_number": "12345",
        },
    }

    assert post_applications_document_matcher.called_once
    assert post_applications_document_matcher.last_request.json() == {
        "description": "Letter of authority for 'p1'",
        "document_on_organisation": {
            "document_type": certificate_type,
            "expiry_date": certificate_expiry_date.isoformat(),
            "reference_code": "12345",
        },
        "document_type": "section-five-certificate",
        "name": f"{certificate_type}.pdf",
        "s3_key": f"{certificate_type}.pdf",
        "size": 0,
    }
