from datetime import datetime
import pytest

from django.urls import reverse


from exporter.applications.views.application_export_details.constants import ExportDetailsSteps
from exporter.applications.views.application_export_details.forms import (
    F680ReferenceNumberForm,
    F1686DetailsForm,
    SecurityOtherDetailsForm,
    SecurityClassifiedDetailsForm,
)


@pytest.fixture(autouse=True)
def setup(
    mock_application_put,
    mock_application_get,
    settings,
    no_op_storage,
):
    settings.FEATURE_FLAG_F680_SECURITY_CLASSIFIED_ENABLED = True


@pytest.fixture
def application_export_details_summary_url(data_standard_case):
    application_id = data_standard_case["case"]["data"]["id"]
    return reverse(
        "applications:application_export_details_summary",
        kwargs={
            "pk": application_id,
        },
    )


@pytest.fixture
def edit_export_details_url(application):
    url = reverse(
        "applications:edit_export_details",
        kwargs={
            "pk": application["id"],
        },
    )
    return url


@pytest.fixture
def post_to_edit_export_details(post_to_step_factory, edit_export_details_url):
    return post_to_step_factory(edit_export_details_url)


@pytest.mark.parametrize(
    "url_name, form_data, expected",
    (
        (
            "edit_export_details_f680_reference_number",
            {"f680_reference_number": "new ref number"},
            {"f680_reference_number": "new ref number"},
        ),
        (
            "edit_export_details_security_other_details",
            {"other_security_approval_details": "other details"},
            {"other_security_approval_details": "other details"},
        ),
        (
            "edit_export_details_f1686_details",
            {
                "f1686_contracting_authority": "signed by the joe",
                "f1686_reference_number": "dummy ref",
                "f1686_approval_date_0": "02",
                "f1686_approval_date_1": "02",
                "f1686_approval_date_2": "2020",
            },
            {
                "f1686_contracting_authority": "signed by the joe",
                "f1686_reference_number": "dummy ref",
                "f1686_approval_date": "2020-02-02",
            },
        ),
    ),
)
def test_edit_export_details_post(
    authorized_client,
    requests_mock,
    application,
    url_name,
    form_data,
    expected,
    application_export_details_summary_url,
):
    url = reverse(f"applications:{url_name}", kwargs={"pk": application["id"]})

    response = authorized_client.post(
        url,
        data=form_data,
    )
    assert response.status_code == 302
    assert response.url == application_export_details_summary_url
    assert requests_mock.last_request.json() == expected


@pytest.mark.parametrize(
    "url_name,application_data,initial",
    (
        (
            "edit_export_details_f680_reference_number",
            {"f680_reference_number": "new ref number"},
            {"f680_reference_number": "new ref number"},
        ),
        (
            "edit_export_details_security_other_details",
            {"other_security_approval_details": "other details"},
            {"other_security_approval_details": "other details"},
        ),
        (
            "edit_export_details_f1686_details",
            {
                "f1686_contracting_authority": "signed by the joe",
                "f1686_reference_number": "dummy ref",
                "f1686_approval_date": "2020-02-02",
            },
            {
                "f1686_contracting_authority": "signed by the joe",
                "f1686_reference_number": "dummy ref",
                "f1686_approval_date": datetime.fromisoformat("2020-02-02").date(),
            },
        ),
    ),
)
def test_edit_export_details_initial(
    authorized_client,
    application,
    url_name,
    application_data,
    initial,
):
    application.update(application_data)

    url = reverse(f"applications:{url_name}", kwargs={"pk": application["id"]})
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert response.context["form"].initial == initial


def test_edit_export_details_true(
    authorized_client,
    edit_export_details_url,
    post_to_edit_export_details,
    mock_application_put,
    application,
):
    application_data = {
        "is_mod_security_approved": True,
        "security_approvals": ["F680", "F1686", "Other"],
        "f680_reference_number": "dummy ref 1",
        "f1686_contracting_authority": "dummy contracting authority 1",
        "other_security_approval_details": "other security approval details 1",
    }
    application.update(application_data)

    response = authorized_client.get(edit_export_details_url)
    assert response.status_code == 200

    assert isinstance(response.context["form"], SecurityClassifiedDetailsForm)
    assert response.context["form"].initial == {
        "is_mod_security_approved": True,
        "security_approvals": ["F680", "F1686", "Other"],
    }

    response = post_to_edit_export_details(
        ExportDetailsSteps.SECURITY_CLASSIFIED,
        {
            "is_mod_security_approved": True,
            "security_approvals": ["F680", "F1686", "Other"],
        },
    )
    assert response.status_code == 200

    assert isinstance(response.context["form"], F680ReferenceNumberForm)
    assert response.context["form"].initial == {
        "f680_reference_number": "dummy ref 1",
    }

    response = post_to_edit_export_details(
        ExportDetailsSteps.F680_REFERENCE_NUMBER,
        {
            "f680_reference_number": "dummy ref 2",
        },
    )

    assert response.status_code == 200

    assert isinstance(response.context["form"], F1686DetailsForm)

    assert response.context["form"].initial == {
        "f1686_contracting_authority": "dummy contracting authority 1",
        "f1686_reference_number": None,
        "f1686_approval_date": None,
    }

    response = post_to_edit_export_details(
        ExportDetailsSteps.F1686_DETAILS,
        {
            "f1686_contracting_authority": "dummy contracting authority 2",
            "f1686_reference_number": "f1686  reference number update",
            "f1686_approval_date_0": "02",
            "f1686_approval_date_1": "02",
            "f1686_approval_date_2": "2020",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], SecurityOtherDetailsForm)

    assert response.context["form"].initial == {"other_security_approval_details": "other security approval details 1"}

    response = post_to_edit_export_details(
        ExportDetailsSteps.SECURITY_OTHER_DETAILS,
        {"other_security_approval_details": "other security approval details 2"},
    )

    assert response.status_code == 302

    assert mock_application_put.called_once
    last_request = mock_application_put.last_request

    assert last_request.json() == {
        "security_approvals": ["F680", "F1686", "Other"],
        "is_mod_security_approved": True,
        "f680_reference_number": "dummy ref 2",
        "f1686_contracting_authority": "dummy contracting authority 2",
        "f1686_reference_number": "f1686  reference number update",
        "f1686_approval_date": "2020-02-02",
        "other_security_approval_details": "other security approval details 2",
    }

    assert response.url == reverse(
        "applications:application_export_details_summary",
        kwargs={
            "pk": application["id"],
        },
    )
