import uuid
from caseworker.core.constants import LICENSING_UNIT_SENIOR_MANAGER_ROLE_ID
from core.constants import CaseStatusEnum, LicenceStatusEnum
from core.exceptions import ServiceError
import pytest

from django.urls import reverse
from django.contrib.messages import constants, get_messages

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
def change_licence_status_confirmation_url(queue_id, case_id, licence_id):
    return reverse(
        "cases:change_licence_status_confirmation",
        kwargs={
            "queue_pk": queue_id,
            "pk": case_id,
            "licence_pk": licence_id,
            "status": LicenceStatusEnum.SUSPENDED,
        },
    )


@pytest.fixture
def case_url(queue_id, case_id):
    return reverse(
        "cases:case",
        kwargs={
            "queue_pk": queue_id,
            "pk": case_id,
            "tab": "licences",
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
def mock_update_licence_details(requests_mock, licence_id):
    yield requests_mock.patch(client._build_absolute_uri(f"/licences/licence_details/{licence_id}"), json={})


@pytest.fixture
def mock_update_licence_details_failure(requests_mock, licence_id):
    yield requests_mock.patch(
        client._build_absolute_uri(f"/licences/licence_details/{licence_id}"), json={}, status_code=500
    )


@pytest.fixture
def licence_details(licence_id):
    return {"id": licence_id, "status": "issued", "case_status": "finalised", "reference_code": "12345AB"}


@pytest.mark.parametrize(
    "licence_state, expected",
    (
        (
            LicenceStatusEnum.ISSUED,
            [("suspended", "Suspended"), ("revoked", "Revoked")],
        ),
        (
            LicenceStatusEnum.REINSTATED,
            [("suspended", "Suspended"), ("revoked", "Revoked")],
        ),
        (
            LicenceStatusEnum.SUSPENDED,
            [("reinstated", "Reinstated"), ("revoked", "Revoked")],
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
    """Test to check licence change status form is populated with the correct values"""

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
    assert change_licence_form.cancel_url == case_url
    assert change_licence_form.reference_code == licence_details["reference_code"]


def test_get_change_licence_status_no_status_selected(
    authorized_client,
    mock_queue,
    mock_case,
    mock_get_licence_details,
    change_licence_status_url,
):
    """Test to check licence change status form gives error when no status is selected"""

    response = authorized_client.post(change_licence_status_url, data={})
    assert response.status_code == 200
    assert response.context["form"].errors == {"status": ["Select a status to change the licence to"]}


def test_change_licence_status_submit_form(
    authorized_client,
    mock_queue,
    mock_case,
    queue_id,
    licence_id,
    case_id,
    change_licence_status_url,
    mock_get_licence_details,
):
    """Test to check licence change status form follows to the correct confirmation screen"""

    response = authorized_client.post(change_licence_status_url, data={"status": "suspended"})

    assert response.status_code == 302
    assert response.url == reverse(
        "cases:change_licence_status_confirmation",
        kwargs={
            "queue_pk": queue_id,
            "pk": case_id,
            "licence_pk": licence_id,
            "status": "suspended",
        },
    )


@pytest.mark.parametrize(
    "licence_state",
    (
        (LicenceStatusEnum.EXHAUSTED),
        (LicenceStatusEnum.EXPIRED),
        (LicenceStatusEnum.REVOKED),
        (LicenceStatusEnum.CANCELLED),
    ),
)
def test_change_licence_status_change_not_permitted_404(
    authorized_client,
    mock_queue,
    mock_case,
    licence_details,
    licence_id,
    change_licence_status_url,
    requests_mock,
    licence_state,
):
    """Test to check licence change status errors when the licence status shouldn't be editied"""
    licence_details["status"] = licence_state
    requests_mock.get(
        client._build_absolute_uri(f"/licences/licence_details/{licence_id}"),
        json=licence_details,
        status_code=200,
    )
    response = authorized_client.get(change_licence_status_url)
    assert response.status_code == 404


def test_change_licence_status_case_status_not_finialized_404(
    authorized_client,
    mock_queue,
    mock_case,
    licence_details,
    licence_id,
    change_licence_status_url,
    requests_mock,
):
    """Test to check licence change status errors when the case isn't finalized"""
    licence_details["case_status"] = CaseStatusEnum.WITHDRAWN
    requests_mock.get(
        client._build_absolute_uri(f"/licences/licence_details/{licence_id}"),
        json=licence_details,
        status_code=200,
    )
    response = authorized_client.get(change_licence_status_url)
    assert response.status_code == 404


def test_change_licence_status_error_404(
    authorized_client,
    mock_queue,
    mock_case,
    licence_details,
    licence_id,
    change_licence_status_url,
    requests_mock,
):
    """Test to check licence change status errors it failed to load getting an licence object"""
    requests_mock.get(
        client._build_absolute_uri(f"/licences/licence_details/{licence_id}"),
        json=licence_details,
        status_code=500,
    )
    response = authorized_client.get(change_licence_status_url)
    assert response.status_code == 404


def test_change_licence_status_case_non_lu_manager_404(
    authorized_client,
    mock_queue,
    mock_case,
    mock_get_licence_details,
    change_licence_status_url,
    mock_gov_user,
):
    """Test to check licence change status errors if the user isn't LU Senior Manager"""
    mock_gov_user["user"]["role"]["id"] = "1234"
    response = authorized_client.get(change_licence_status_url)
    assert response.status_code == 404


def test_get_change_licence_status_confirmation(
    authorized_client,
    mock_queue,
    mock_case,
    mock_get_licence_details,
    change_licence_status_confirmation_url,
    case_url,
):
    """Test to check licence change confirmation loads correctly with correct cancel url"""
    response = authorized_client.get(change_licence_status_confirmation_url)
    assert response.status_code == 200

    assert response.context["form"].cancel_url == case_url


@pytest.mark.parametrize(
    "licence_state",
    (
        (LicenceStatusEnum.EXHAUSTED),
        (LicenceStatusEnum.EXPIRED),
        (LicenceStatusEnum.REVOKED),
        (LicenceStatusEnum.CANCELLED),
    ),
)
def test_get_post_change_licence_status_confirmation_not_permitted_404(
    authorized_client,
    mock_queue,
    mock_case,
    mock_get_licence_details,
    change_licence_status_confirmation_url,
    case_url,
    licence_details,
    requests_mock,
    licence_state,
):
    """Test to check licence change confirmation errors when a licence isn't permitted to be changed"""
    licence_details["status"] = licence_state
    requests_mock.get(
        client._build_absolute_uri(f"/licences/licence_details/{licence_id}"),
        json=licence_details,
        status_code=200,
    )
    response = authorized_client.get(change_licence_status_confirmation_url)
    assert response.status_code == 404

    response = authorized_client.post(change_licence_status_confirmation_url, data={"status": "revoked"})
    assert response.status_code == 404


def test_get_post_change_licence_status_confirmation_case_status_not_finialized_404(
    authorized_client,
    mock_queue,
    mock_case,
    licence_details,
    licence_id,
    change_licence_status_confirmation_url,
    requests_mock,
):
    """Test to check licence change confirmation errors when a case isn't in finalized state"""
    licence_details["case_status"] = CaseStatusEnum.WITHDRAWN
    requests_mock.get(
        client._build_absolute_uri(f"/licences/licence_details/{licence_id}"),
        json=licence_details,
        status_code=200,
    )
    response = authorized_client.get(change_licence_status_confirmation_url)
    assert response.status_code == 404

    response = authorized_client.post(change_licence_status_confirmation_url)
    assert response.status_code == 404


def test_get_post_change_licence_status_confirmation_case_non_lu_manager_404(
    authorized_client,
    mock_queue,
    mock_case,
    mock_get_licence_details,
    change_licence_status_confirmation_url,
    mock_gov_user,
):
    """Test to check licence change confirmation errors when the user isn't LU Senior Manager"""
    mock_gov_user["user"]["role"]["id"] = str(uuid.uuid4())
    response = authorized_client.get(change_licence_status_confirmation_url)
    assert response.status_code == 404

    response = authorized_client.post(change_licence_status_confirmation_url)
    assert response.status_code == 404


def test_change_licence_status_confirmation_error_404(
    authorized_client,
    mock_queue,
    mock_case,
    licence_details,
    licence_id,
    change_licence_status_confirmation_url,
    requests_mock,
):
    """Test to check licence change confirmation errors when we fail to get a licence object"""
    requests_mock.get(
        client._build_absolute_uri(f"/licences/licence_details/{licence_id}"),
        json=licence_details,
        status_code=500,
    )
    response = authorized_client.get(change_licence_status_confirmation_url)
    assert response.status_code == 404


def test_get_change_licence_status_confirmation_successfull(
    authorized_client,
    mock_queue,
    mock_case,
    mock_get_licence_details,
    queue_id,
    case_id,
    mock_update_licence_details,
    change_licence_status_confirmation_url,
):
    """Test to check licence change confirmation successfully called API endpoint and returns as expected"""
    response = authorized_client.post(change_licence_status_confirmation_url)
    assert response.status_code == 302
    assert response.url == reverse(
        "cases:case",
        kwargs={
            "queue_pk": queue_id,
            "pk": case_id,
            "tab": "licences",
        },
    )
    assert mock_update_licence_details.called
    assert mock_update_licence_details.last_request.json() == {
        "status": "suspended",
    }
    assert [(m.level, m.message) for m in get_messages(response.wsgi_request)] == [
        (constants.SUCCESS, "Licence status successfully changed")
    ]


def test_get_change_licence_status_confirmation_failure(
    authorized_client,
    mock_queue,
    mock_case,
    mock_get_licence_details,
    mock_update_licence_details_failure,
    change_licence_status_confirmation_url,
):
    """Test to check licence change confirmation propagates and handles an API update error"""
    with pytest.raises(ServiceError) as ex:
        authorized_client.post(change_licence_status_confirmation_url)

    assert ex.value.status_code == 500
    assert ex.value.user_message == "Unexpected error changing licence status"
