from unittest.mock import patch

import pytest

from exporter.applications.forms import parties


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"reuse_party": "True"}, True, None),
        ({"reuse_party": ""}, False, {"reuse_party": ["Select yes if you want to reuse an existing party"]}),
    ),
)
def test_party_reuse_form(data, valid, errors):
    form = parties.PartyReuseForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"sub_type": "government"}, True, None),
        ({"sub_type": "other", "sub_type_other": "test_sub_type"}, True, None),
        ({"sub_type": ""}, False, {"sub_type": ["Select what type of party you're creating"]}),
        ({"sub_type": "other"}, False, {"sub_type_other": ["Enter the type of the party you're adding"]}),
    ),
)
def test_party_subtype_select_form(data, valid, errors):
    form = parties.PartySubTypeSelectForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"name": "test"}, True, None),
        ({"name": ""}, False, {"name": ["Enter a name"]}),
    ),
)
def test_party_name_form(data, valid, errors):
    form = parties.PartyNameForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"website": "test"}, True, None),
        ({"website": ""}, True, None),
        ({}, True, None),
    ),
)
def test_party_website_form(data, valid, errors):
    form = parties.PartyWebsiteForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"address": "1 somewhere", "country": "aus"}, True, None),
        ({"address": "", "country": ""}, False, {"address": ["Enter an address"], "country": ["Select the country"]}),
    ),
)
@patch("exporter.applications.forms.parties.get_countries")
def test_party_address_form(mock_get_countries, data, valid, errors):
    class Request:
        csp_nonce = "test"

    request = Request()
    mock_get_countries.return_value = [{"id": "aus", "name": "Austria"}, {"id": "fr", "name": "France"}]
    form = parties.PartyAddressForm(request=request, data=data)

    assert form.is_valid() == valid
    mock_get_countries.assert_called_once_with(request, False, ["GB"])

    if not valid:
        assert form.errors == errors


@pytest.mark.parametrize(
    "data, valid, errors",
    (
        ({"signatory_name_euu": "test"}, True, None),
        ({"signatory_name_euu": ""}, False, {"signatory_name_euu": ["Enter a name"]}),
    ),
)
def test_party_signatory_name_form(data, valid, errors):
    form = parties.PartySignatoryNameForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == errors
