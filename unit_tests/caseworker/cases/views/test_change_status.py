import pytest

from bs4 import BeautifulSoup

from django.contrib.messages import constants, get_messages
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from core import client
from core.constants import CaseStatusEnum
from core.exceptions import ServiceError


@pytest.fixture(autouse=True)
def setup(data_standard_case, mock_gov_user, mock_queue, mock_standard_case):
    data_standard_case["case"]["case_officer"] = mock_gov_user["user"]


@pytest.fixture
def queue_id(data_queue):
    return data_queue["id"]


@pytest.fixture
def case_id(data_standard_case):
    return data_standard_case["case"]["id"]


@pytest.fixture
def change_status_url(queue_id, case_id):
    return reverse(
        "cases:change_status",
        kwargs={
            "queue_pk": queue_id,
            "pk": case_id,
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
def post_status_api_url(case_id):
    return client._build_absolute_uri(f"/caseworker/applications/{case_id}/status/")


@pytest.fixture
def mock_post_case_status(requests_mock, post_status_api_url):
    return requests_mock.post(url=post_status_api_url, json={})


@pytest.fixture
def mock_post_case_status_failure(requests_mock, post_status_api_url):
    return requests_mock.post(
        url=post_status_api_url,
        json={},
        status_code=500,
    )


@pytest.fixture
def mock_standard_case_failure(requests_mock, data_standard_case):
    url = client._build_absolute_uri(f"/cases/{data_standard_case['case']['id']}/")
    yield requests_mock.get(url=url, json={}, status_code=500)


def test_change_status_GET(
    authorized_client,
    change_status_url,
    case_id,
):
    response = authorized_client.get(change_status_url)
    assert response.status_code == 200
    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["case"].id == case_id

    html = BeautifulSoup(response.content, "html.parser")
    all_h1s = [elem.get_text().strip() for elem in html.find_all("h1")]
    assert "Change case status" in all_h1s

    status_options = [item["value"] for item in html.find_all("option")]

    excluded_statuses = [
        CaseStatusEnum.APPLICANT_EDITING,
        CaseStatusEnum.FINALISED,
        CaseStatusEnum.REGISTERED,
        CaseStatusEnum.CLC,
        CaseStatusEnum.PV,
        CaseStatusEnum.SURRENDERED,
        CaseStatusEnum.REVOKED,
        CaseStatusEnum.SUSPENDED,
    ]
    for excluded_status in excluded_statuses:
        assert excluded_status not in status_options


@pytest.mark.parametrize(
    "gov_user_type,expected",
    [
        ("mock_gov_tau_user", False),
        ("mock_gov_fcdo_user", False),
        ("mock_gov_desnz_nuclear_user", False),
        ("mock_gov_lu_user", True),
    ],
)
def test_change_status_GET_provides_finalise_status(
    authorized_client,
    change_status_url,
    case_id,
    gov_user_type,
    expected,
    request,
):
    _ = request.getfixturevalue(gov_user_type)

    response = authorized_client.get(change_status_url)
    assert response.status_code == 200

    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["case"].id == case_id

    html = BeautifulSoup(response.content, "html.parser")
    all_h1s = [elem.get_text().strip() for elem in html.find_all("h1")]
    assert "Change case status" in all_h1s

    # Only LU users get an option set the status as 'Finalised'
    statuses = [item["value"] for item in html.find_all("option")]
    assert (CaseStatusEnum.FINALISED in statuses) == expected


@pytest.mark.parametrize(
    "gov_user_type,expected",
    [
        ("mock_gov_tau_user", False),
        ("mock_gov_fcdo_user", False),
        ("mock_gov_desnz_nuclear_user", False),
        ("mock_gov_lu_user", False),
        ("mock_gov_lu_super_user", True),
    ],
)
def test_closed_status_visible_to_specific_roles(
    authorized_client,
    change_status_url,
    case_id,
    gov_user_type,
    expected,
    request,
):
    _ = request.getfixturevalue(gov_user_type)

    response = authorized_client.get(change_status_url)
    assert response.status_code == 200

    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["case"].id == case_id

    html = BeautifulSoup(response.content, "html.parser")
    all_h1s = [elem.get_text().strip() for elem in html.find_all("h1")]
    assert "Change case status" in all_h1s

    # Only LU users get an option set the status as 'Finalised'
    statuses = [item["value"] for item in html.find_all("option")]
    assert (CaseStatusEnum.CLOSED in statuses) == expected


def test_change_status_success(
    authorized_client,
    case_url,
    change_status_url,
    mock_post_case_status,
):
    response = authorized_client.post(change_status_url, data={"status": "submitted"})
    assert response.status_code == 302
    assert response.url == case_url
    assert mock_post_case_status.called
    assert mock_post_case_status.last_request.json() == {
        "status": "submitted",
    }
    assert [(m.level, m.message) for m in get_messages(response.wsgi_request)] == [
        (constants.SUCCESS, "Case status successfully changed")
    ]


def test_change_status_failure(
    authorized_client,
    change_status_url,
    mock_post_case_status_failure,
):
    with pytest.raises(ServiceError) as ex:
        authorized_client.post(change_status_url, data={"status": "under_review"})

    assert ex.value.status_code == 500
    assert ex.value.user_message == "Unexpected error changing case status"


def test_get_change_status_initial_value(
    authorized_client,
    change_status_url,
    data_standard_case,
):
    """Test to check case change status form is populated with the correct initial value"""

    data_standard_case["case"]["data"]["status"] = {
        "key": "initial_checks",
        "value": "Initial checks",
    }

    response = authorized_client.get(change_status_url)
    soup = BeautifulSoup(response.content, "html.parser")
    select = soup.find(id="id_status")
    option_elements = select.find_all("option")
    assert "selected" not in option_elements[0].attrs
    assert "selected" not in option_elements[1].attrs
    assert "selected" in option_elements[2].attrs


def test_change_status_invalid_case_failure(
    authorized_client,
    change_status_url,
    mock_standard_case_failure,
):
    """Test to check Case status cannot be changed for an invalid case"""

    response = authorized_client.get(change_status_url)
    assert response.status_code == 404


def test_change_status_user_cannot_change_status(
    authorized_client,
    change_status_url,
    data_standard_case,
):
    """Test to check Case needs to be assigned to a user before they can change status"""

    data_standard_case["case"]["case_officer"] = None
    data_standard_case["case"]["assigned_users"] = []

    response = authorized_client.get(change_status_url)
    assert response.status_code == 404
