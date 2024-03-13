import pytest
from exporter.core.organisation import forms


@pytest.mark.parametrize(
    "data, valid",
    (
        ({"type": "commercial"}, True),
        ({"type": "individual"}, True),
        ({"type": ""}, False),
    ),
)
def test_registration_type_form(data, valid):
    form = forms.RegistrationTypeForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors["type"][0] == "Select the type of organisation you're registering for"


@pytest.mark.parametrize(
    "data, valid",
    (
        ({"location": "united_kingdom"}, True),
        ({"location": "abroad"}, True),
        ({"location": ""}, False),
    ),
)
def test_registration_uk_based_form(data, valid):
    form = forms.RegistrationUKBasedForm(data=data)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors["location"][0] == "Select a location"


@pytest.mark.parametrize(
    "data, is_individual, is_uk_based, valid, error",
    (
        ({}, True, False, False, {"name": ["Enter a name"]}),
        ({"name": "joe", "eori_number": "123"}, True, False, False, {"eori_number": ["Invalid UK EORI number"]}),
        (
            {"name": "joe", "eori_number": "123456789101112131"},
            True,
            False,
            False,
            {"eori_number": ["EORI numbers are 17 characters or less"]},
        ),
        (
            {"name": "joe", "eori_number": "GX205672212000"},
            True,
            False,
            False,
            {"eori_number": ["Invalid UK EORI number"]},
        ),
        (
            {"name": "joe", "eori_number": "GB205672212000", "vat_number": "123"},
            True,
            False,
            False,
            {"vat_number": ["Standard UK VAT numbers are 9 digits long"]},
        ),
        (
            {"name": "joe", "eori_number": "GB205672212000", "vat_number": "123456789101112131"},
            True,
            False,
            False,
            {"vat_number": ["Standard UK VAT numbers are 9 digits long"]},
        ),
        (
            {"name": "joe", "eori_number": "GB205672212000", "vat_number": "GX123456789"},
            True,
            False,
            False,
            {"vat_number": ["Invalid UK VAT number"]},
        ),
        ({"name": "joe", "eori_number": "GB205672212000", "vat_number": "GB123456789"}, True, False, True, None),
        (
            {},
            False,
            False,
            False,
            {
                "name": ["Enter a name"],
            },
        ),
        (
            {
                "name": "joe",
                "eori_number": "GB205672212000",
                "vat_number": "GB123456789",
                "sic_number": "xyz",
                "registration_number": "21313ewfwe",
            },
            False,
            False,
            False,
            {
                "sic_number": ["Only enter numbers"],
                "registration_number": ["Registration numbers are 8 numbers long"],
            },
        ),
        (
            {
                "name": "joe",
                "eori_number": "GB205672212000",
                "vat_number": "GB123456789",
                "sic_number": "123",
                "registration_number": "1234567x",
            },
            False,
            False,
            False,
            {
                "sic_number": ["Enter a valid SIC code"],
                "registration_number": ["Registration numbers are 8 numbers long"],
            },
        ),
        (
            {
                "name": "joe",
                "eori_number": "GB205672212000",
                "vat_number": "GB123456789",
                "sic_number": "12345",
                "registration_number": "12345678",
            },
            False,
            False,
            True,
            None,
        ),
    ),
)
def test_register_details_form(data, is_individual, is_uk_based, valid, error):
    form = forms.RegisterDetailsForm(data=data, is_individual=is_individual, is_uk_based=is_uk_based)

    assert form.is_valid() == valid

    if not valid:
        assert form.errors == error


@pytest.mark.parametrize(
    "data, valid, error",
    (
        (
            {},
            False,
            {
                "name": ["Enter a name for your site"],
                "address_line_1": ["Enter a real building and street name"],
                "city": ["Enter a real city"],
                "region": ["Enter a real region"],
                "postcode": ["Enter a real postcode"],
                "phone_number": ["Enter a telephone number"],
            },
        ),
        (
            {
                "name": "joe",
                "address_line_1": "xyz",
                "region": "r",
                "city": "c1",
                "postcode": "pc",
                "phone_number": "12334",
                "website": "notreal.com",
            },
            False,
            {
                "phone_number": ["Invalid telephone number"],
                "website": ["Enter a valid URL"],
            },
        ),
        (
            {
                "name": "joe",
                "address_line_1": "xyz",
                "region": "r",
                "city": "c1",
                "postcode": "pc",
                "phone_number": "+441234567890",
                "website": "http://www.notreal.com",
            },
            True,
            None,
        ),
        (
            {
                "name": "joe",
                "address_line_1": "xyz",
                "region": "r",
                "city": "c1",
                "postcode": "pc",
                "phone_number": "01234567890",
                "website": "http://www.notreal.com",
            },
            True,
            None,
        ),
    ),
)
def test_register_uk_address_details_form(data, valid, error):
    form = forms.RegisterAddressDetailsForm(is_individual=True, is_uk_based=True, data=data)
    assert form.is_valid() == valid
    if not valid:
        assert form.errors == error


def test_register_non_uk_address_details_form():
    form = forms.RegisterAddressDetailsForm(is_individual=True, is_uk_based=False, data={})
    assert not form.is_valid()
    assert form.errors == {
        "name": ["Enter a name for your site"],
        "address": ["Enter an address"],
        "phone_number": ["Enter a telephone number"],
        "country": ["Enter a country"],
    }


def test_select_organisation_form_invalid(data_organisations):

    form = forms.SelectOrganisationForm(organisations=data_organisations, data={})
    assert not form.is_valid()
    assert form.errors == {"organisation": ["Select an organisation"]}


def test_select_organisation_form_valid(data_organisations):

    form = forms.SelectOrganisationForm(
        organisations=data_organisations, data={"organisation": data_organisations[0]["id"]}
    )
    assert form.is_valid()
