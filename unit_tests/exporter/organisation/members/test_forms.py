import pytest
from exporter.organisation.members.users import forms
from core.constants import ExporterRoles


@pytest.mark.parametrize(
    "data, valid",
    (
        ({"role": ""}, False),
        ({"role": "agent"}, True),
    ),
)
def test_select_role_form_validation(data, valid):
    form = forms.SelectRoleForm(data=data)
    assert form.is_valid() == valid

    if not valid:
        assert form.errors["role"][0] == "Select a role"


@pytest.mark.parametrize(
    "data, valid, error",
    (
        (
            {},
            False,
            {
                "email": ["Enter an email address in the correct format, like name@example.com"],
                "sites": ["Select at least one site"],
            },
        ),
        (
            {"email": "joe@", "sites": ["f733084d-5a11-4a41-a55b-974d2fb779a7"]},
            False,
            {"email": ["Enter a valid email address."]},
        ),
        (
            {"email": "joe@bloggs.com", "sites": ["f733084d-5a11-4a41-a55b-974d2fb779a7"]},
            True,
            None,
        ),
    ),
)
def test_select_role_form_validation(data, valid, error, mock_sites, mock_organisation_users_list):
    form = forms.AddUserForm(
        data=data,
        organisation_users=mock_organisation_users_list,
        role_id=ExporterRoles.agent.id,
        sites=mock_sites["sites"],
    )
    assert form.is_valid() == valid

    if not valid:
        assert form.errors == error


def test_select_role_form(mock_sites, mock_organisation_users_list):
    data = {"email": "joe@bloggs.com", "sites": [mock_sites["sites"][0]["id"]]}
    form = forms.AddUserForm(
        data=data,
        organisation_users=mock_organisation_users_list,
        role_id=ExporterRoles.administrator.id,
        sites=mock_sites["sites"],
    )
    assert form.is_valid()
    assert form.fields["sites"].choices[0][0] == mock_sites["sites"][0]["id"]

    assert (
        form.fields["sites"].choices[0].hint
        == "\n    42 Question Road<br />\n\n    London<br />\n\n    Islington<br />\n\n    United Kingdom<br />\n\n"
    )
    assert ExporterRoles.administrator.name in form.Layout.TITLE


def test_select_role_validate_email(mock_sites, mock_organisation_users_list):
    mock_organisation_users_list = [
        "joe@bloggs.com",
    ]
    data = {"email": "joe@bloggs.com", "sites": [mock_sites["sites"][0]["id"]]}
    form = forms.AddUserForm(
        data=data,
        organisation_users=mock_organisation_users_list,
        role_id=ExporterRoles.administrator.id,
        sites=mock_sites["sites"],
    )
    assert not form.is_valid()
    assert form.errors == {"email": ["Enter an email address that is not registered to this organisation"]}
