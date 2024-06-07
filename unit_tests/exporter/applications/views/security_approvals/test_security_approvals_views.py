import pytest

from django.urls import reverse

from exporter.applications.views.security_approvals.constants import SecurityApprovalSteps
from exporter.applications.views.security_approvals.forms import (
    F680ReferenceNumberForm,
    F1686DetailsForm,
    SecurityOtherDetailsForm,
)


@pytest.fixture(autouse=True)
def setup(no_op_storage):
    yield


@pytest.fixture
def application_security_approvals_url(data_standard_case):
    application_id = data_standard_case["case"]["data"]["id"]
    return reverse(
        "applications:security_approvals",
        kwargs={
            "pk": application_id,
        },
    )


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
def goto_step(goto_step_factory, application_security_approvals_url):
    return goto_step_factory(application_security_approvals_url)


@pytest.fixture
def post_to_step(post_to_step_factory, application_security_approvals_url):
    return post_to_step_factory(application_security_approvals_url)


def test_application_security_approvals_end_to_end(
    authorized_client,
    data_standard_case,
    application_security_approvals_url,
    mock_application_get,
    mock_application_put,
    post_to_step,
):
    authorized_client.get(application_security_approvals_url)

    response = post_to_step(
        SecurityApprovalSteps.SECURITY_CLASSIFIED,
        {
            "is_mod_security_approved": True,
            "security_approvals": ["F680", "F1686", "Other"],
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], F680ReferenceNumberForm)

    response = post_to_step(
        SecurityApprovalSteps.F680_REFERENCE_NUMBER,
        {
            "f680_reference_number": "dummy ref",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], F1686DetailsForm)

    response = post_to_step(
        SecurityApprovalSteps.F1686_DETAILS,
        {
            "f1686_contracting_authority": "dummy contracting authority",
            "f1686_reference_number": "f1686  reference number update",
            "f1686_approval_date_0": "02",
            "f1686_approval_date_1": "02",
            "f1686_approval_date_2": "2020",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], SecurityOtherDetailsForm)

    response = post_to_step(
        SecurityApprovalSteps.SECURITY_OTHER_DETAILS,
        {
            "other_security_approval_details": "dummy other details",
        },
    )

    assert response.status_code == 302

    assert mock_application_put.called_once
    last_request = mock_application_put.last_request

    assert last_request.json() == {
        "security_approvals": ["F680", "F1686", "Other"],
        "is_mod_security_approved": True,
        "f680_reference_number": "dummy ref",
        "f1686_contracting_authority": "dummy contracting authority",
        "f1686_reference_number": "f1686  reference number update",
        "f1686_approval_date": "2020-02-02",
        "other_security_approval_details": "dummy other details",
    }

    assert response.url == reverse(
        "applications:security_approvals_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
        },
    )


def test_application_security_approvals_end_to_end_alternative(
    authorized_client,
    data_standard_case,
    application_security_approvals_url,
    mock_application_get,
    mock_application_put,
    post_to_step,
):
    authorized_client.get(application_security_approvals_url)

    response = post_to_step(
        SecurityApprovalSteps.SECURITY_CLASSIFIED,
        {
            "is_mod_security_approved": True,
            "security_approvals": ["F1686", "Other"],
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], F1686DetailsForm)

    response = post_to_step(
        SecurityApprovalSteps.F1686_DETAILS,
        {
            "f1686_contracting_authority": "dummy contracting authority",
            "f1686_reference_number": "dummy f1686 reference number",
            "f1686_approval_date_0": "02",
            "f1686_approval_date_1": "02",
            "f1686_approval_date_2": "2020",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], SecurityOtherDetailsForm)

    response = post_to_step(
        SecurityApprovalSteps.SECURITY_OTHER_DETAILS,
        {
            "other_security_approval_details": "dummy other details",
        },
    )

    assert response.status_code == 302

    assert mock_application_put.called_once
    last_request = mock_application_put.last_request

    assert last_request.json() == {
        "security_approvals": ["F1686", "Other"],
        "is_mod_security_approved": True,
        "f1686_contracting_authority": "dummy contracting authority",
        "f1686_reference_number": "dummy f1686 reference number",
        "f1686_approval_date": "2020-02-02",
        "other_security_approval_details": "dummy other details",
    }

    assert response.url == reverse(
        "applications:security_approvals_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
        },
    )


def test_application_security_approvals_short(
    authorized_client,
    data_standard_case,
    application_security_approvals_url,
    mock_application_get,
    mock_application_put,
    post_to_step,
):
    authorized_client.get(application_security_approvals_url)

    response = post_to_step(
        SecurityApprovalSteps.SECURITY_CLASSIFIED,
        {
            "is_mod_security_approved": False,
        },
    )

    assert response.status_code == 302

    assert mock_application_put.called_once
    last_request = mock_application_put.last_request

    assert last_request.json() == {
        "security_approvals": [],
        "is_mod_security_approved": False,
    }
    assert response.url == reverse(
        "applications:security_approvals_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
        },
    )


@pytest.fixture
def task_list_url(application):
    return reverse(
        "applications:task_list",
        kwargs={
            "pk": application["id"],
        },
    )


def test_application_summary(
    authorized_client,
    application_security_approvals_summary_url,
    task_list_url,
    mock_application_get,
):

    response = authorized_client.get(application_security_approvals_summary_url)
    assert response.context["security_classified_approvals_types"]
    assert response.context["application"]
    assert response.context["back_link_url"] == task_list_url
