import pytest
from django.urls import reverse
from django.contrib.messages import constants, get_messages

from core import client
from core.exceptions import ServiceError

from core.constants import ExporterRoles


@pytest.fixture()
def sites_data():
    return [
        {
            "id": "1",
            "name": "site a",
            "address": {
                "address_line_1": "line 1",
                "address_line_2": "line 2",
                "city": "city 1",
                "postcode": "AAA 11",
                "country": {"name": "UK"},
            },
        },
        {
            "id": "2",
            "name": "site b",
            "address": {
                "address_line_1": "site 2 line 1",
                "address_line_2": "site 2 line 2",
                "city": "city 2",
                "postcode": "BBB 11",
                "country": {"name": "UK"},
            },
        },
    ]


@pytest.fixture
def url(organisation_pk):
    return reverse("organisations:add-exporter-admin", kwargs={"pk": organisation_pk})


@pytest.fixture
def success_url(organisation_pk):
    return reverse("organisations:organisation_members", kwargs={"pk": organisation_pk})


@pytest.fixture
def mock_get_organisation_members(requests_mock, organisation_pk):
    url = client._build_absolute_uri(f"/organisations/{organisation_pk}/users/?disable_pagination=True")
    data = [{"email": "user1@example.com"}]
    yield requests_mock.get(url=url, json=data)


@pytest.fixture
def mock_get_organisation_sites(requests_mock, organisation_pk, sites_data):
    url = client._build_absolute_uri(f"/organisations/{organisation_pk}/users/")
    url = f"/organisations/{organisation_pk}/sites/?disable_pagination=True"
    json = {"sites": sites_data}
    yield requests_mock.get(client._build_absolute_uri(url), json=json)


@pytest.fixture
def mock_organisation_create_users(requests_mock, organisation_pk):
    url = client._build_absolute_uri(f"/caseworker/organisations/{organisation_pk}/exporter-users/")
    yield requests_mock.post(url=url, json={}, status_code=201)


@pytest.fixture
def mock_organisation_create_users_failure(requests_mock, organisation_pk):
    url = client._build_absolute_uri(f"/caseworker/organisations/{organisation_pk}/exporter-users/")
    yield requests_mock.post(url=url, json={}, status_code=500)


@pytest.fixture
def mock_get_organisation_500_error(requests_mock, organisation_pk):
    yield requests_mock.get(
        client._build_absolute_uri(f"/organisations/{organisation_pk}/"),
        json={},
        status_code=500,
    )


def test_create_exporter_admin_user_get(
    authorized_client,
    requests_mock,
    url,
    success_url,
    mock_get_organisation,
    mock_get_organisation_members,
    mock_get_organisation_sites,
):
    """Test to check add exporter admin form is populated with the correct values"""

    response = authorized_client.get(url)
    assert response.status_code == 200

    exporter_admin_form = response.context["form"]

    assert exporter_admin_form.cancel_url == success_url
    assert response.context["back_link_url"] == success_url
    assert exporter_admin_form.organisation_users == {"user1@example.com"}
    assert exporter_admin_form.fields["sites"].choices[0].value == "1"
    assert exporter_admin_form.fields["sites"].choices[1].value == "2"


def test_create_exporter_admin_form_success(
    authorized_client,
    requests_mock,
    url,
    success_url,
    mock_get_organisation,
    mock_get_organisation_members,
    mock_get_organisation_sites,
    mock_organisation_create_users,
):
    """Test to check add exporter admin is successfull when posted with correct data"""

    data = {"email": "user2@example.com", "sites": ["1"]}
    expected_data = {**data, "role": ExporterRoles.administrator.id}

    response = authorized_client.post(url, data=data)

    assert response.status_code == 302
    assert response.url == success_url

    assert mock_organisation_create_users.called
    assert mock_organisation_create_users.last_request.json() == expected_data

    assert [(m.level, m.message) for m in get_messages(response.wsgi_request)] == [
        (constants.SUCCESS, "Administrator successfully added to organisation")
    ]


@pytest.mark.parametrize(
    "data, expected_errors",
    (
        (
            {"email": "", "sites": []},
            {
                "email": ["Enter an email address in the correct format, like name@example.com"],
                "sites": ["Select at least one site"],
            },
        ),
        (
            {"email": "", "sites": ["1"]},
            {
                "email": ["Enter an email address in the correct format, like name@example.com"],
            },
        ),
        (
            {"email": "jkefhekjwh", "sites": ["1"]},
            {"email": ["Enter a valid email address."]},
        ),
        (
            {"email": "user1@example.com", "sites": ["1"]},
            {"email": ["Enter an email address that is not registered to this organisation"]},
        ),
    ),
)
def test_create_exporter_admin_errors(
    authorized_client,
    data,
    expected_errors,
    url,
    mock_get_organisation,
    mock_get_organisation_members,
    mock_get_organisation_sites,
):
    """Test to check add exporter admin form when posted with incomplete data shows error"""

    response = authorized_client.post(url, data=data)
    assert response.status_code == 200
    assert response.context["form"].errors == expected_errors


def test_create_exporter_admin_api_failed(
    authorized_client,
    url,
    mock_get_organisation,
    mock_get_organisation_members,
    mock_get_organisation_sites,
    mock_organisation_create_users_failure,
):
    """Test to check add exporter admin when posted with correct data handles API failure"""

    data = {"email": "user2@example.com", "sites": ["1"]}

    with pytest.raises(ServiceError) as ex:
        authorized_client.post(url, data=data)

    assert ex.value.status_code == 500
    assert ex.value.user_message == "Unexpected error adding user to organisation"


def test_create_exporter_admin_404_on_get_organisation_error(
    authorized_client,
    url,
    mock_get_organisation_500_error,
):
    """Test to check add exporter admin errors when we fail to get a organisation"""
    response = authorized_client.get(url)
    assert response.status_code == 404


def test_create_exporter_admin_404_on_no_permission(
    authorized_client,
    mock_gov_user,
    url,
):
    """Test to check add exporter admin errors when user doesn't have manage organisation permission"""

    mock_gov_user["user"]["role"]["permissions"] = ["NO_PERMISSION"]

    response = authorized_client.get(url)
    assert response.status_code == 404

    response = authorized_client.post(url)
    assert response.status_code == 404


@pytest.mark.parametrize("organisation_status", ["in-review", "rejected", "unknown"])
def test_create_exporter_admin_404_on_org_no_approved(
    authorized_client,
    requests_mock,
    url,
    organisation_pk,
    organisation_status,
):
    """Test to check add exporter admin errors when we the organisation isn't approved"""

    requests_mock.get(
        client._build_absolute_uri(f"/organisations/{organisation_pk}/"),
        json={"status": {"key": organisation_status}},
    )

    response = authorized_client.get(url)
    assert response.status_code == 404

    response = authorized_client.post(url)
    assert response.status_code == 404
