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
    "data, valid, error",
    (
        ({}, False, {"name": ["Enter a name"], "eori_number": ["Enter an EORI number"]}),
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
                "eori_number": ["Enter an EORI number"],
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


def test_select_organisation_form_invalid(data_organisations):

    form = forms.SelectOrganisationForm(organisations=data_organisations, data={})
    assert not form.is_valid()
    assert form.errors == {"organisation": ["Select an organisation"]}


def test_select_organisation_form_valid(data_organisations):

    form = forms.SelectOrganisationForm(
        organisations=data_organisations, data={"organisation": data_organisations[0]["id"]}
    )
    assert form.is_valid()


@pytest.mark.parametrize(
    "data, valid, form_field, error_message, form_class",
    (
        ({"name": "test"}, True, "name", None, forms.RegistrationEditName),
        ({"name": ""}, False, "name", "Enter a name", forms.RegistrationEditName),
        ({"eori_number": "GB205672212000"}, True, "eori_number", None, forms.RegistrationEditEoriNumber),
        ({"eori_number": "ewfwef"}, False, "eori_number", "Invalid UK EORI number", forms.RegistrationEditEoriNumber),
        ({"vat_number": "GB123456789"}, True, "vat_number", None, forms.RegistrationEditVatNumber),
        (
            {"vat_number": "ewfwef"},
            False,
            "vat_number",
            "Standard UK VAT numbers are 9 digits long",
            forms.RegistrationEditVatNumber,
        ),
        ({"sic_number": "12345"}, True, "sic_number", None, forms.RegistrationEditSICNumber),
        ({"sic_number": "abc"}, False, "sic_number", "Only enter numbers", forms.RegistrationEditSICNumber),
        (
            {"registration_number": "12345678"},
            True,
            "registration_number",
            None,
            forms.RegistrationEditRegistrationNumber,
        ),
        (
            {"registration_number": "1234567x"},
            False,
            "registration_number",
            "Registration numbers are 8 numbers long",
            forms.RegistrationEditRegistrationNumber,
        ),
        ({"name": "Can building"}, True, "name", None, forms.RegistrationEditAddressName),
        ({"name": ""}, False, "name", "Enter a name for your site", forms.RegistrationEditAddressName),
        ({"address": "address 0"}, True, "address", None, forms.RegistrationEditAddress),
        ({"address": ""}, False, "address", "Enter an address", forms.RegistrationEditAddress),
        ({"address_line_1": "55 lite av"}, True, "address_line_1", None, forms.RegistrationEditAddress1),
        (
            {"address_line_1": ""},
            False,
            "address_line_1",
            "Enter a real building and street name",
            forms.RegistrationEditAddress1,
        ),
        ({"address_line_2": "lite town"}, True, "address_line_2", None, forms.RegistrationEditAddress2),
        ({"city": "lite town"}, True, "city", None, forms.RegistrationEditCity),
        ({"city": ""}, False, "city", "Enter a real city", forms.RegistrationEditCity),
        ({"region": "lite region"}, True, "region", None, forms.RegistrationEditRegion),
        ({"region": ""}, False, "region", "Enter a real region", forms.RegistrationEditRegion),
        ({"postcode": "LR1 8GG"}, True, "postcode", None, forms.RegistrationEditPostCode),
        ({"postcode": ""}, False, "postcode", "Enter a real postcode", forms.RegistrationEditPostCode),
        ({"phone_number": "+441234567890"}, True, "phone_number", None, forms.RegistrationEditPhoneNumber),
        ({"phone_number": "424rwew"}, False, "phone_number", "Invalid phone number", forms.RegistrationEditPhoneNumber),
        ({"website": "http://www.notreal.com"}, True, "website", None, forms.RegistrationEditWebsite),
        ({"website": "efew"}, False, "website", "Enter a valid URL", forms.RegistrationEditWebsite),
        ({"country": "UK"}, True, "country", None, forms.RegistrationEditCountry),
        ({"country": ""}, False, "country", "Enter a country", forms.RegistrationEditCountry),
    ),
)
def test_draft_registration_single_edit_form(data, valid, form_field, error_message, form_class):
    form = form_class(data=data)
    assert form.is_valid() == valid
    if not valid:
        assert form.errors[form_field][0] == error_message
    else:
        assert form.cleaned_data[form_field]
