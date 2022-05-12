import datetime
import pytest
import uuid

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from exporter.applications.views.goods.add_good_firearm.views.constants import AddGoodFirearmToApplicationSteps
from exporter.applications.views.goods.add_good_firearm.views.edit import SummaryTypeMixin
from exporter.core.forms import CurrentFile
from exporter.core.helpers import decompose_date
from exporter.goods.forms.firearms import (
    FirearmDeactivationDetailsForm,
    FirearmIsDeactivatedForm,
    FirearmMadeBefore1938Form,
    FirearmOnwardAlteredProcessedForm,
    FirearmOnwardExportedForm,
    FirearmOnwardIncorporatedForm,
    FirearmQuantityAndValueForm,
    FirearmSerialIdentificationMarkingsForm,
    FirearmSerialNumbersForm,
    FirearmYearOfManufactureForm,
)


@pytest.fixture(autouse=True)
def setup(mock_application_get, mock_good_get, mock_good_on_application_get):
    pass


@pytest.fixture(autouse=True)
def set_feature_flags(settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS = True
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.fixture
def application(data_standard_case):
    return data_standard_case["case"]["data"]


@pytest.fixture
def section_one_document(good_on_application):
    return {
        "id": str(uuid.uuid4()),
        "name": "section_one_certificate.docx",
        "s3_key": "section_one_certificate.docx.s3_key",
        "safe": True,
        "document_type": "section-one-certificate",
        "good_on_application": good_on_application["id"],
    }


@pytest.fixture
def mock_section_one_document_get(requests_mock, section_one_document, application, good_id):
    url = f"/applications/{application['id']}/goods/{good_id}/documents/"
    return requests_mock.get(url, json={"documents": [section_one_document]})


@pytest.fixture
def edit_firearm_certificate_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:product_on_application_summary_edit_firearm_certificate",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.fixture
def product_on_application_summary_url(application, good_on_application, summary_type):
    url = reverse(
        f"applications:{summary_type.replace('-', '_')}",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
        },
    )
    return url


@pytest.fixture
def mock_good_on_application_put(requests_mock, good_on_application):
    url = f"/applications/good-on-application/{good_on_application['id']}/"
    return requests_mock.put(url, json={})


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_firearm_certificate_initial(
    authorized_client,
    application,
    good_id,
    section_one_document,
    mock_section_one_document_get,
    edit_firearm_certificate_url,
):
    response = authorized_client.get(edit_firearm_certificate_url)
    assert response.status_code == 200

    form = response.context["form"]
    initial = form.initial

    file = initial.pop("file")
    assert isinstance(file, CurrentFile)
    assert file.name == "section_one_certificate.docx"
    assert file.url == reverse(
        "applications:good-on-application-document",
        kwargs={
            "pk": application["id"],
            "good_pk": good_id,
            "doc_pk": section_one_document["id"],
        },
    )
    assert file.safe

    assert initial == {
        "section_certificate_date_of_expiry": datetime.date(2030, 12, 12),
        "section_certificate_missing": False,
        "section_certificate_missing_reason": "",
        "section_certificate_number": "12345",
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_firearm_certificate_retaining_current_file(
    authorized_client,
    edit_firearm_certificate_url,
    product_on_application_summary_url,
    mock_section_one_document_get,
    mock_good_on_application_put,
):
    response = authorized_client.post(
        edit_firearm_certificate_url,
        data={
            "section_certificate_number": "67890",
            "section_certificate_missing": False,
            **decompose_date("section_certificate_date_of_expiry", datetime.date(2024, 1, 1)),
        },
    )

    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "section_certificate_date_of_expiry": "2024-01-01",
            "section_certificate_missing": False,
            "section_certificate_number": "67890",
        },
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_firearm_certificate_retaining_upload_new_file(
    authorized_client,
    edit_firearm_certificate_url,
    product_on_application_summary_url,
    mock_section_one_document_get,
    mock_good_on_application_put,
    requests_mock,
    application,
    good_id,
    section_one_document,
    good_on_application,
):
    delete_good_on_application_matcher = requests_mock.delete(
        f"/applications/{application['id']}/goods/{good_id}/documents/{section_one_document['id']}/",
        json={},
    )

    post_good_on_application_document_matcher = requests_mock.post(
        f"/applications/{application['id']}/goods/{good_id}/documents/",
        status_code=201,
        json={},
    )

    post_application_document_matcher = requests_mock.post(
        f"/applications/{application['id']}/documents/",
        status_code=201,
        json={},
    )

    get_additional_documents_matcher = requests_mock.get(
        f"/applications/{application['id']}/documents/",
        status_code=200,
        json={
            "documents": [section_one_document],
        },
    )

    delete_additional_documents_matcher = requests_mock.delete(
        f"/applications/{application['id']}/documents/{section_one_document['id']}/",
        status_code=204,
        json={},
    )

    response = authorized_client.post(
        edit_firearm_certificate_url,
        data={
            "file": SimpleUploadedFile("firearm_certificate.pdf", b"This is the firearm certificate"),
            "section_certificate_number": "67890",
            "section_certificate_missing": False,
            **decompose_date("section_certificate_date_of_expiry", datetime.date(2024, 1, 1)),
        },
    )

    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "section_certificate_date_of_expiry": "2024-01-01",
            "section_certificate_missing": False,
            "section_certificate_number": "67890",
        },
    }

    assert delete_good_on_application_matcher.called_once

    assert get_additional_documents_matcher.called_once
    assert delete_additional_documents_matcher.called_once

    assert post_good_on_application_document_matcher.called_once
    assert post_good_on_application_document_matcher.last_request.json() == {
        "document_type": "section-one-certificate",
        "good_on_application": good_on_application["id"],
        "name": "firearm_certificate.pdf",
        "s3_key": "firearm_certificate.pdf",
        "size": 0,
    }

    assert post_application_document_matcher.called_once
    assert post_application_document_matcher.last_request.json() == {
        "description": "Firearm certificate for 'p1'",
        "document_type": "section-one-certificate",
        "name": "firearm_certificate.pdf",
        "s3_key": "firearm_certificate.pdf",
        "size": 0,
    }


@pytest.fixture
def section_two_document(good_on_application):
    return {
        "id": str(uuid.uuid4()),
        "name": "section_two_certificate.docx",
        "s3_key": "section_two_certificate.docx.s3_key",
        "safe": True,
        "document_type": "section-two-certificate",
        "good_on_application": good_on_application["id"],
    }


@pytest.fixture
def mock_section_two_document_get(requests_mock, section_two_document, application, good_id):
    url = f"/applications/{application['id']}/goods/{good_id}/documents/"
    return requests_mock.get(url, json={"documents": [section_two_document]})


@pytest.fixture
def edit_shotgun_certificate_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:product_on_application_summary_edit_shotgun_certificate",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_shotgun_certificate_initial(
    authorized_client,
    application,
    good_id,
    section_two_document,
    mock_section_two_document_get,
    edit_shotgun_certificate_url,
):
    response = authorized_client.get(edit_shotgun_certificate_url)
    assert response.status_code == 200

    form = response.context["form"]
    initial = form.initial

    file = initial.pop("file")
    assert isinstance(file, CurrentFile)
    assert file.name == "section_two_certificate.docx"
    assert file.url == reverse(
        "applications:good-on-application-document",
        kwargs={
            "pk": application["id"],
            "good_pk": good_id,
            "doc_pk": section_two_document["id"],
        },
    )
    assert file.safe

    assert initial == {
        "section_certificate_date_of_expiry": datetime.date(2030, 12, 12),
        "section_certificate_missing": False,
        "section_certificate_missing_reason": "",
        "section_certificate_number": "12345",
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_shotgun_certificate_retaining_current_file(
    authorized_client,
    edit_shotgun_certificate_url,
    product_on_application_summary_url,
    mock_section_two_document_get,
    mock_good_on_application_put,
):
    response = authorized_client.post(
        edit_shotgun_certificate_url,
        data={
            "section_certificate_number": "67890",
            "section_certificate_missing": False,
            **decompose_date("section_certificate_date_of_expiry", datetime.date(2024, 1, 1)),
        },
    )

    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "section_certificate_date_of_expiry": "2024-01-01",
            "section_certificate_missing": False,
            "section_certificate_number": "67890",
        },
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_shotgun_certificate_retaining_upload_new_file(
    authorized_client,
    edit_shotgun_certificate_url,
    product_on_application_summary_url,
    mock_section_two_document_get,
    mock_good_on_application_put,
    requests_mock,
    application,
    good_id,
    section_two_document,
    good_on_application,
):
    delete_good_on_application_matcher = requests_mock.delete(
        f"/applications/{application['id']}/goods/{good_id}/documents/{section_two_document['id']}/",
        json={},
    )

    post_good_on_application_document_matcher = requests_mock.post(
        f"/applications/{application['id']}/goods/{good_id}/documents/",
        status_code=201,
        json={},
    )

    post_application_document_matcher = requests_mock.post(
        f"/applications/{application['id']}/documents/",
        status_code=201,
        json={},
    )

    get_additional_documents_matcher = requests_mock.get(
        f"/applications/{application['id']}/documents/",
        status_code=200,
        json={
            "documents": [section_two_document],
        },
    )

    delete_additional_documents_matcher = requests_mock.delete(
        f"/applications/{application['id']}/documents/{section_two_document['id']}/",
        status_code=204,
        json={},
    )

    response = authorized_client.post(
        edit_shotgun_certificate_url,
        data={
            "file": SimpleUploadedFile("shotgun_certificate.pdf", b"This is the shotgun certificate"),
            "section_certificate_number": "67890",
            "section_certificate_missing": False,
            **decompose_date("section_certificate_date_of_expiry", datetime.date(2024, 1, 1)),
        },
    )

    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "section_certificate_date_of_expiry": "2024-01-01",
            "section_certificate_missing": False,
            "section_certificate_number": "67890",
        },
    }

    assert delete_good_on_application_matcher.called_once

    assert get_additional_documents_matcher.called_once
    assert delete_additional_documents_matcher.called_once

    assert post_good_on_application_document_matcher.called_once
    assert post_good_on_application_document_matcher.last_request.json() == {
        "document_type": "section-two-certificate",
        "good_on_application": good_on_application["id"],
        "name": "shotgun_certificate.pdf",
        "s3_key": "shotgun_certificate.pdf",
        "size": 0,
    }

    assert post_application_document_matcher.called_once
    assert post_application_document_matcher.last_request.json() == {
        "description": "Shotgun certificate for 'p1'",
        "document_type": "section-two-certificate",
        "name": "shotgun_certificate.pdf",
        "s3_key": "shotgun_certificate.pdf",
        "size": 0,
    }


@pytest.fixture
def edit_made_before_1938_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:product_on_application_summary_edit_made_before_1938",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_made_before_1938_initial(
    authorized_client,
    edit_made_before_1938_url,
):
    response = authorized_client.get(edit_made_before_1938_url)
    assert response.status_code == 200

    form = response.context["form"]
    assert isinstance(form, FirearmMadeBefore1938Form)

    assert form.initial == {
        "is_made_before_1938": True,
    }


@pytest.fixture
def post_to_step_made_before_1938(post_to_step_factory, edit_made_before_1938_url):
    return post_to_step_factory(edit_made_before_1938_url)


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_made_before_1938_true(
    post_to_step_made_before_1938,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = post_to_step_made_before_1938(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938, data={"is_made_before_1938": True}
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmYearOfManufactureForm)
    assert response.context["form"].initial == {
        "year_of_manufacture": 1930,
    }

    response = post_to_step_made_before_1938(
        AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE, data={"year_of_manufacture": "1930"}
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "is_made_before_1938": True,
            "year_of_manufacture": 1930,
        },
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_made_before_1938_false(
    post_to_step_made_before_1938,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = post_to_step_made_before_1938(
        AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938, data={"is_made_before_1938": False}
    )

    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "is_made_before_1938": False,
        },
    }


@pytest.fixture
def edit_year_of_manufacture_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:product_on_application_summary_edit_year_of_manufacture",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_year_of_manufacture_initial(authorized_client, edit_year_of_manufacture_url):
    response = authorized_client.get(edit_year_of_manufacture_url)
    assert response.status_code == 200

    form = response.context["form"]
    assert isinstance(form, FirearmYearOfManufactureForm)

    assert form.initial == {
        "year_of_manufacture": 1930,
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_year_of_manufacture_post(
    authorized_client,
    edit_year_of_manufacture_url,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = authorized_client.post(
        edit_year_of_manufacture_url,
        data={
            "year_of_manufacture": 1931,
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {"year_of_manufacture": 1931},
    }


@pytest.fixture
def edit_onward_exported_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:product_on_application_summary_edit_onward_exported",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.fixture
def post_to_step_onward_exported(post_to_step_factory, edit_onward_exported_url):
    return post_to_step_factory(edit_onward_exported_url)


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_onward_exported_true(
    authorized_client,
    edit_onward_exported_url,
    post_to_step_onward_exported,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = authorized_client.get(edit_onward_exported_url)
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, FirearmOnwardExportedForm)
    assert form.initial == {
        "is_onward_exported": True,
    }

    response = post_to_step_onward_exported(
        AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED,
        data={"is_onward_exported": True},
    )
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, FirearmOnwardAlteredProcessedForm)
    assert form.initial == {
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "I will alter it real good",
    }

    response = post_to_step_onward_exported(
        AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED,
        data={
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "Altering",
        },
    )
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, FirearmOnwardIncorporatedForm)
    assert form.initial == {
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "I will onward incorporate",
    }

    response = post_to_step_onward_exported(
        AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED,
        data={
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "Incorporated",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "Altering",
            "is_onward_exported": True,
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "Incorporated",
        },
        "is_good_incorporated": True,
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_onward_exported_false(
    authorized_client,
    edit_onward_exported_url,
    post_to_step_onward_exported,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = authorized_client.get(edit_onward_exported_url)
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, FirearmOnwardExportedForm)
    assert form.initial == {
        "is_onward_exported": True,
    }

    response = post_to_step_onward_exported(
        AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED,
        data={"is_onward_exported": False},
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "is_onward_exported": False,
        },
    }


@pytest.fixture
def edit_onward_altered_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:product_on_application_summary_edit_onward_altered",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_onward_altered_processed(
    authorized_client,
    edit_onward_altered_url,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = authorized_client.get(edit_onward_altered_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmOnwardAlteredProcessedForm)
    assert response.context["form"].initial == {
        "is_onward_altered_processed": True,
        "is_onward_altered_processed_comments": "I will alter it real good",
    }

    response = authorized_client.post(
        edit_onward_altered_url,
        data={
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "Altered",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url
    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "is_onward_altered_processed": True,
            "is_onward_altered_processed_comments": "Altered",
        },
    }


@pytest.fixture
def edit_onward_incorporated_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:product_on_application_summary_edit_onward_incorporated",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_onward_incorporated(
    authorized_client,
    edit_onward_incorporated_url,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = authorized_client.get(edit_onward_incorporated_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmOnwardIncorporatedForm)
    assert response.context["form"].initial == {
        "is_onward_incorporated": True,
        "is_onward_incorporated_comments": "I will onward incorporate",
    }

    response = authorized_client.post(
        edit_onward_incorporated_url,
        data={
            "is_onward_incorporated": True,
            "is_onward_incorporated_comments": "Incorporated",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url
    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {"is_onward_incorporated": True, "is_onward_incorporated_comments": "Incorporated"},
        "is_good_incorporated": True,
    }


@pytest.fixture
def edit_is_deactivated_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:product_on_application_summary_edit_is_deactivated",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.fixture
def post_to_step_is_deactivated(post_to_step_factory, edit_is_deactivated_url):
    return post_to_step_factory(edit_is_deactivated_url)


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_is_deactivated_initial(
    authorized_client,
    edit_is_deactivated_url,
):
    response = authorized_client.get(edit_is_deactivated_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmIsDeactivatedForm)
    assert response.context["form"].initial == {
        "is_deactivated": True,
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_is_deactivated_true(
    post_to_step_is_deactivated,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = post_to_step_is_deactivated(
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED,
        data={
            "is_deactivated": True,
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmDeactivationDetailsForm)
    assert response.context["form"].initial == {
        "date_of_deactivation": datetime.date(2007, 12, 12),
        "is_deactivated_to_standard": False,
        "not_deactivated_to_standard_comments": "Not deactivated",
    }

    response = post_to_step_is_deactivated(
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD,
        data={
            **decompose_date("date_of_deactivation", datetime.date(2008, 1, 1)),
            "is_deactivated_to_standard": False,
            "not_deactivated_to_standard_comments": "Comments",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "date_of_deactivation": "2008-01-01",
            "is_deactivated": True,
            "is_deactivated_to_standard": False,
            "not_deactivated_to_standard_comments": "Comments",
        },
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_is_deactivated_false(
    post_to_step_is_deactivated,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = post_to_step_is_deactivated(
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED,
        data={
            "is_deactivated": False,
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "is_deactivated": False,
        },
    }


@pytest.fixture
def edit_is_deactivated_to_standard_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:product_on_application_summary_edit_is_deactivated_to_standard",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_is_deactivated_to_standard(
    authorized_client,
    edit_is_deactivated_to_standard_url,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = authorized_client.get(edit_is_deactivated_to_standard_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmDeactivationDetailsForm)
    assert response.context["form"].initial == {
        "date_of_deactivation": datetime.date(2007, 12, 12),
        "is_deactivated_to_standard": False,
        "not_deactivated_to_standard_comments": "Not deactivated",
    }

    response = authorized_client.post(
        edit_is_deactivated_to_standard_url,
        data={
            **decompose_date("date_of_deactivation", datetime.date(2008, 1, 1)),
            "is_deactivated_to_standard": False,
            "not_deactivated_to_standard_comments": "Comments",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url
    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "date_of_deactivation": "2008-01-01",
            "is_deactivated_to_standard": False,
            "not_deactivated_to_standard_comments": "Comments",
        },
    }


@pytest.fixture
def edit_quantity_value_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:product_on_application_summary_edit_quantity_value",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_quantity_value(
    authorized_client,
    edit_quantity_value_url,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = authorized_client.get(edit_quantity_value_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmQuantityAndValueForm)
    assert response.context["form"].initial == {
        "number_of_items": 3,
        "value": "16.32",
    }

    response = authorized_client.post(
        edit_quantity_value_url,
        data={
            "number_of_items": 20,
            "value": "20.22",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url
    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {"number_of_items": 20},
        "quantity": 20,
        "unit": "NAR",
        "value": "20.22",
    }


@pytest.fixture
def edit_serial_identification_markings_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:product_on_application_summary_edit_serial_identification_markings",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.fixture
def post_to_step_serial_identification_markings(post_to_step_factory, edit_serial_identification_markings_url):
    return post_to_step_factory(edit_serial_identification_markings_url)


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_serial_identification_markings_initial(
    authorized_client,
    edit_serial_identification_markings_url,
):
    response = authorized_client.get(edit_serial_identification_markings_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmSerialIdentificationMarkingsForm)
    assert response.context["form"].initial == {
        "serial_numbers_available": "NOT_AVAILABLE",
        "no_identification_markings_details": "No markings",
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_serial_identification_markings_available(
    post_to_step_serial_identification_markings,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = post_to_step_serial_identification_markings(
        AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        data={
            "serial_numbers_available": "AVAILABLE",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmSerialNumbersForm)

    response = post_to_step_serial_identification_markings(
        AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS,
        data={
            "serial_numbers_0": "1111",
            "serial_numbers_1": "2222",
            "serial_numbers_2": "3333",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "no_identification_markings_details": "",
            "serial_numbers": [
                "1111",
                "2222",
                "3333",
            ],
            "serial_numbers_available": "AVAILABLE",
        },
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_serial_identification_markings_later(
    post_to_step_serial_identification_markings,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = post_to_step_serial_identification_markings(
        AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        data={
            "serial_numbers_available": "LATER",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "no_identification_markings_details": "",
            "serial_numbers_available": "LATER",
        },
    }


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_serial_identification_markings_not_available(
    post_to_step_serial_identification_markings,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = post_to_step_serial_identification_markings(
        AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING,
        data={
            "serial_numbers_available": "NOT_AVAILABLE",
            "no_identification_markings_details": "No serial numbers",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "no_identification_markings_details": "No serial numbers",
            "serial_numbers_available": "NOT_AVAILABLE",
        },
    }


@pytest.fixture
def edit_serial_numbers_url(application, good_on_application, summary_type):
    url = reverse(
        "applications:product_on_application_summary_edit_serial_numbers",
        kwargs={
            "pk": application["id"],
            "good_on_application_pk": good_on_application["id"],
            "summary_type": summary_type,
        },
    )
    return url


@pytest.mark.parametrize(
    "summary_type",
    SummaryTypeMixin.SUMMARY_TYPES,
)
def test_edit_serial_numbers(
    authorized_client,
    edit_serial_numbers_url,
    product_on_application_summary_url,
    mock_good_on_application_put,
):
    response = authorized_client.get(edit_serial_numbers_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmSerialNumbersForm)

    response = authorized_client.post(
        edit_serial_numbers_url,
        data={
            "serial_numbers_0": "1111",
            "serial_numbers_1": "2222",
            "serial_numbers_2": "3333",
        },
    )
    assert response.status_code == 302
    assert response.url == product_on_application_summary_url

    assert mock_good_on_application_put.called_once
    assert mock_good_on_application_put.last_request.json() == {
        "firearm_details": {
            "serial_numbers": [
                "1111",
                "2222",
                "3333",
            ],
        },
    }
