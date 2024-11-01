from datetime import datetime
import pytest
from bs4 import BeautifulSoup

from django.urls import reverse


from exporter.applications.views.security_approvals.constants import SecurityApprovalSteps
from exporter.applications.views.security_approvals.forms import (
    F1686DetailsForm,
    SecurityOtherDetailsForm,
    SecurityClassifiedDetailsForm,
    SubjectToITARControlsForm,
)


@pytest.fixture(autouse=True)
def setup(
    mock_application_put,
    mock_application_get,
    no_op_storage,
):
    yield


@pytest.fixture
def application_security_approvals_summary_url(data_standard_case):
    application_id = data_standard_case["case"]["data"]["id"]
    return reverse(
        "applications:security_approvals_summary",
        kwargs={
            "pk": application_id,
        },
    )


@pytest.fixture
def edit_security_approvals_url(application):
    url = reverse(
        "applications:edit_security_approvals_details",
        kwargs={
            "pk": application["id"],
        },
    )
    return url


@pytest.fixture
def post_to_edit_security_approvals(post_to_step_factory, edit_security_approvals_url):
    return post_to_step_factory(edit_security_approvals_url)


@pytest.mark.parametrize(
    "url_name, form_data, expected",
    (
        (
            "edit_security_approvals_subject_to_itar_controls",
            {"subject_to_itar_controls": False},
            {"subject_to_itar_controls": False},
        ),
        (
            "edit_security_approvals_f680_reference_number",
            {"f680_reference_number": "new ref number"},
            {"f680_reference_number": "new ref number"},
        ),
        (
            "edit_security_approvals_security_other_details",
            {"other_security_approval_details": "other details"},
            {"other_security_approval_details": "other details"},
        ),
        (
            "edit_security_approvals_f1686_details",
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
        (
            "edit_security_approvals_f1686_details",
            {
                "f1686_contracting_authority": "some text",
                "f1686_approval_date_0": "01",
                "f1686_approval_date_1": "01",
                "f1686_approval_date_2": "2022",
            },
            {
                "f1686_contracting_authority": "some text",
                "f1686_reference_number": "",
                "f1686_approval_date": "2022-01-01",
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
    application_security_approvals_summary_url,
):
    url = reverse(f"applications:{url_name}", kwargs={"pk": application["id"]})

    response = authorized_client.post(
        url,
        data=form_data,
    )
    assert response.status_code == 302
    assert response.url == application_security_approvals_summary_url
    assert requests_mock.last_request.json() == expected


@pytest.mark.parametrize(
    ("url_name", "application_data", "initial", "expected_title"),
    [
        (
            "edit_security_approvals_f680_reference_number",
            {"f680_reference_number": "new ref number"},
            {"f680_reference_number": "new ref number"},
            "What is the F680 reference number? - LITE - GOV.UK",
        ),
        (
            "edit_security_approvals_security_other_details",
            {"other_security_approval_details": "other details"},
            {"other_security_approval_details": "other details"},
            "Provide details of your written approval - LITE - GOV.UK",
        ),
        (
            "edit_security_approvals_f1686_details",
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
            "Provide details of your F1686 approval - LITE - GOV.UK",
        ),
    ],
)
def test_edit_security_approvals_initial(
    authorized_client, application, url_name, application_data, initial, expected_title
):
    application.update(application_data)

    url = reverse(f"applications:{url_name}", kwargs={"pk": application["id"]})
    response = authorized_client.get(url)

    assert response.status_code == 200
    assert response.context["form"].initial == initial
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == expected_title


def test_edit_security_approvals_true(
    authorized_client,
    edit_security_approvals_url,
    post_to_edit_security_approvals,
    mock_application_put,
    application,
    application_security_approvals_summary_url,
):
    application_data = {
        "is_mod_security_approved": True,
        "security_approvals": ["F680"],
        "f680_reference_number": "dummy ref 1",
        "f1686_contracting_authority": "dummy contracting authority 1",
        "other_security_approval_details": "other security approval details 1",
    }
    application.update(application_data)

    response = authorized_client.get(edit_security_approvals_url)
    assert response.status_code == 200

    assert isinstance(response.context["form"], SecurityClassifiedDetailsForm)
    assert response.context["form"].initial == {
        "is_mod_security_approved": True,
        "security_approvals": ["F680"],
    }

    response = post_to_edit_security_approvals(
        SecurityApprovalSteps.SECURITY_CLASSIFIED,
        {
            "is_mod_security_approved": True,
            "security_approvals": ["F680", "F1686", "Other"],
        },
    )

    assert response.status_code == 200

    assert isinstance(response.context["form"], F1686DetailsForm)

    assert response.context["form"].initial == {
        "f1686_contracting_authority": "dummy contracting authority 1",
        "f1686_reference_number": None,
        "f1686_approval_date": None,
    }

    response = post_to_edit_security_approvals(
        SecurityApprovalSteps.F1686_DETAILS,
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

    response = post_to_edit_security_approvals(
        SecurityApprovalSteps.SECURITY_OTHER_DETAILS,
        {"other_security_approval_details": "other security approval details 2"},
    )

    assert response.status_code == 302

    assert mock_application_put.called_once
    last_request = mock_application_put.last_request

    assert last_request.json() == {
        "security_approvals": ["F680", "F1686", "Other"],
        "is_mod_security_approved": True,
        "f1686_contracting_authority": "dummy contracting authority 2",
        "f1686_reference_number": "f1686  reference number update",
        "f1686_approval_date": "2020-02-02",
        "other_security_approval_details": "other security approval details 2",
    }

    assert response.url == application_security_approvals_summary_url


@pytest.mark.parametrize(
    "application_security_approvals, edit_value_security_approvals, expected_form",
    (
        (
            ["F680"],
            ["F680", "F1686"],
            F1686DetailsForm,
        ),
        (
            ["F1686"],
            ["F680", "F1686"],
            SubjectToITARControlsForm,
        ),
        (
            ["F680"],
            ["F680", "Other"],
            SecurityOtherDetailsForm,
        ),
        (
            ["F680", "Other"],
            ["F680", "F1686", "Other"],
            F1686DetailsForm,
        ),
    ),
)
def test_edit_security_approvals_conditions(
    authorized_client,
    edit_security_approvals_url,
    post_to_edit_security_approvals,
    mock_application_put,
    application,
    application_security_approvals_summary_url,
    application_security_approvals,
    edit_value_security_approvals,
    expected_form,
):
    application_data = {
        "is_mod_security_approved": True,
        "security_approvals": application_security_approvals,
    }
    application.update(application_data)

    authorized_client.get(edit_security_approvals_url)

    response = post_to_edit_security_approvals(
        SecurityApprovalSteps.SECURITY_CLASSIFIED,
        {
            "is_mod_security_approved": True,
            "security_approvals": edit_value_security_approvals,
        },
    )

    assert response.status_code == 200

    assert isinstance(response.context["form"], expected_form)
