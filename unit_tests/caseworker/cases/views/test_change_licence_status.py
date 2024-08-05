from caseworker.core.constants import LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID
from core.constants import CaseStatusEnum, LicenceStatusEnum
import pytest

from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(data_standard_case, mock_gov_user):
    # Setup the correct permission to allow License state changes
    mock_gov_user["user"]["role"]["id"] = LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID


@pytest.fixture
def queue_id(data_queue):
    return data_queue["id"]


@pytest.fixture
def licence_id(data_standard_case):
    return data_standard_case["case"]["licences"][0]["id"]


@pytest.fixture
def case_id(data_standard_case):
    return data_standard_case["case"]["id"]


@pytest.fixture
def get_licence_details_api_url(licence_id):
    return client._build_absolute_uri(f"/licences/licence_details/{licence_id}")


@pytest.fixture
def change_licence_status_url(queue_id, case_id, licence_id):
    return reverse(
        "cases:change_licence_status",
        kwargs={
            "queue_pk": queue_id,
            "pk": case_id,
            "licence_pk": licence_id,
        },
    )


@pytest.fixture
def case_url(queue_id, case_id):
    return reverse(
        "cases:case",
        kwargs={
            "queue_pk": queue_id,
            "pk": case_id,
            "tab": "details",
        },
    )


@pytest.fixture
def mock_get_licence_details(requests_mock, licence_id, licence_details):

    yield requests_mock.get(
        client._build_absolute_uri(f"/licences/licence_details/{licence_id}"),
        json=licence_details,
        status_code=200,
    )


@pytest.fixture
def licence_details(licence_id):
    return {"id": licence_id, "status": "issued", "case_status": "finalised", "reference_code": "12345AB"}


@pytest.mark.parametrize(
    "licence_state, expected",
    (
        (
            LicenceStatusEnum.ISSUED,
            [("issued", "Issued"), ("suspended", "Suspended"), ("reinstated", "Reinstated")],
        ),
        (
            LicenceStatusEnum.REINSTATED,
            [("reinstated", "Reinstated"), ("suspended", "Suspended"), ("revoked", "Revoked")],
        ),
        (
            LicenceStatusEnum.SUSPENDED,
            [("suspended", "Suspended"), ("reinstated", "Reinstated"), ("revoked", "Revoked")],
        ),
    ),
)
def test_get_change_licence_status(
    authorized_client,
    mock_queue,
    mock_case,
    licence_details,
    licence_id,
    change_licence_status_url,
    case_url,
    requests_mock,
    licence_state,
    expected,
):

    licence_details["status"] = licence_state
    requests_mock.get(
        client._build_absolute_uri(f"/licences/licence_details/{licence_id}"),
        json=licence_details,
        status_code=200,
    )
    response = authorized_client.get(change_licence_status_url)
    assert response.status_code == 200

    change_licence_form = response.context["form"]

    assert change_licence_form.fields["status"].choices == expected
    assert change_licence_form.initial == {"status": licence_state}
    assert change_licence_form.cancel_url == case_url
    assert change_licence_form.reference_code == licence_details["reference_code"]


def test_get_change_licence_status_submit_form(
    authorized_client,
    mock_queue,
    mock_case,
    change_licence_status_url,
    mock_get_licence_details,
):

    response = authorized_client.post(change_licence_status_url, data={"status": "issued"})

    assert response.status_code == 302
    assert response.url == change_licence_status_url


@pytest.mark.parametrize(
    "licence_state",
    (
        (LicenceStatusEnum.EXHAUSTED),
        (LicenceStatusEnum.EXPIRED),
        (LicenceStatusEnum.REVOKED),
        (LicenceStatusEnum.CANCELLED),
    ),
)
def test_get_change_licence_status_change_not_permitted_404(
    authorized_client,
    mock_queue,
    mock_case,
    licence_details,
    licence_id,
    change_licence_status_url,
    requests_mock,
    licence_state,
):

    licence_details["status"] = licence_state
    requests_mock.get(
        client._build_absolute_uri(f"/licences/licence_details/{licence_id}"),
        json=licence_details,
        status_code=200,
    )
    response = authorized_client.get(change_licence_status_url)
    assert response.status_code == 404


def test_get_change_licence_status_case_status_not_finialized_404(
    authorized_client,
    mock_queue,
    mock_case,
    licence_details,
    licence_id,
    change_licence_status_url,
    requests_mock,
):

    licence_details["case_status"] = CaseStatusEnum.WITHDRAWN
    requests_mock.get(
        client._build_absolute_uri(f"/licences/licence_details/{licence_id}"),
        json=licence_details,
        status_code=200,
    )
    response = authorized_client.get(change_licence_status_url)
    assert response.status_code == 404


def test_get_change_licence_status_error_404(
    authorized_client,
    mock_queue,
    mock_case,
    licence_details,
    licence_id,
    change_licence_status_url,
    requests_mock,
):

    requests_mock.get(
        client._build_absolute_uri(f"/licences/licence_details/{licence_id}"),
        json=licence_details,
        status_code=500,
    )
    response = authorized_client.get(change_licence_status_url)
    assert response.status_code == 404


def test_get_change_licence_status_case_non_lu_manager_404(
    authorized_client,
    mock_queue,
    mock_case,
    mock_get_licence_details,
    change_licence_status_url,
    mock_gov_user,
):

    mock_gov_user["user"]["role"]["id"] = "12345"
    response = authorized_client.get(change_licence_status_url)
    assert response.status_code == 404
