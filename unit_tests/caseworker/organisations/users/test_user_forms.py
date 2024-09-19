from caseworker.organisations.members.users.forms import AddAdminExporterUserForm
import pytest


@pytest.fixture()
def site_data():
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
        }
    ]


@pytest.mark.parametrize(
    "data, organisation_users_data, is_valid, errors",
    (
        (
            {"email": "", "sites": []},
            [],
            False,
            {
                "email": ["Enter an email address in the correct format, like name@example.com"],
                "sites": ["Select at least one site"],
            },
        ),
        (
            {"email": "", "sites": ["1"]},
            [],
            False,
            {
                "email": ["Enter an email address in the correct format, like name@example.com"],
            },
        ),
        (
            {"email": "jkefhekjwh", "sites": ["1"]},
            [],
            False,
            {"email": ["Enter a valid email address."]},
        ),
        (
            {"email": "ex@example.com", "sites": ["1"]},
            ["ex@example.com"],
            False,
            {"email": ["Enter an email address that is not registered to this organisation"]},
        ),
        (
            {"email": "ex@example.com", "sites": ["1"]},
            ["ex_2@example.com"],
            True,
            {},
        ),
    ),
)
def test_add_admin_exporter_user_form(data, organisation_users_data, is_valid, errors, site_data):
    cancel_url = "/cancel/"
    form = AddAdminExporterUserForm(
        organisation_users=organisation_users_data, sites=site_data, cancel_url=cancel_url, data=data
    )
    assert form.is_valid() is is_valid
    assert form.errors == errors
