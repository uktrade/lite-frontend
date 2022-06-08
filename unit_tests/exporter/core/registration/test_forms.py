import pytest
from exporter.core.registration import forms


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
    "data, valid, error",
    (
        ({}, False, {"name": ["Enter a name"], "eori_number": ["Enter a EORI number"]}),
        ({"name": "joe", "eori_number": "123"}, False, {"eori_number": ["Invalid UK EORI number"]}),
        (
            {"name": "joe", "eori_number": "123456789101112131"},
            False,
            {"eori_number": ["EORI numbers are 17 characters or less"]},
        ),
        ({"name": "joe", "eori_number": "GX205672212000"}, False, {"eori_number": ["Invalid UK EORI number"]}),
        (
            {"name": "joe", "eori_number": "GB205672212000", "vat_number": "123"},
            False,
            {"vat_number": ["Standard UK VAT numbers are 9 digits long"]},
        ),
        (
            {"name": "joe", "eori_number": "GB205672212000", "vat_number": "123456789101112131"},
            False,
            {"vat_number": ["Standard UK VAT numbers are 9 digits long"]},
        ),
        (
            {"name": "joe", "eori_number": "GB205672212000", "vat_number": "GX123456789"},
            False,
            {"vat_number": ["Invalid UK VAT number"]},
        ),
        ({"name": "joe", "eori_number": "GB205672212000", "vat_number": "GB123456789"}, True, None),
    ),
)
def test_register_individual_details_form(data, valid, error):
    form = forms.RegisterDetailsForm(data=data, is_individual=True)

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
                "name": ["Enter a name"],
                "eori_number": ["Enter a EORI number"],
                "sic_number": ["Enter a SIC code"],
                "vat_number": ["This field is required."],
                "registration_number": ["Enter a registration number"],
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
            True,
            None,
        ),
    ),
)
def test_register_commercial_details_form(data, valid, error):
    form = forms.RegisterDetailsForm(data=data, is_individual=False)

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
                "phone_number": ["Enter a phone number"],
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
                "phone_number": ["Invalid phone number"],
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
    ),
)
def test_register_uk_address_details_form(data, valid, error):
    form = forms.RegisterAddressDetailsForm(is_uk_based=True, data=data)
    assert form.is_valid() == valid
    if not valid:
        assert form.errors == error


def test_register_non_uk_address_details_form():
    form = forms.RegisterAddressDetailsForm(is_uk_based=False, data={})
    assert not form.is_valid()
    assert form.errors == {
        "name": ["Enter a name for your site"],
        "address": ["Enter an address"],
        "phone_number": ["Enter a phone number"],
        "country": ["Enter a country"],
    }
