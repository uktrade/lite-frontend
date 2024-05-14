import pytest
from exporter.core.organisation import forms
from core import client


@pytest.fixture
def mock_registration_number_fail(requests_mock):
    url = client._build_absolute_uri("/organisations/registration_number")
    return requests_mock.post(
        url=url,
        json={"errors": {"registration_number": ["This registration number is already in use."]}},
        status_code=400,
    )


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
    "data, valid, error, form_class",
    (
        (
            {},
            False,
            {"name": ["Enter a name"], "eori_number": ["Enter a EORI number"]},
            forms.RegisterDetailsIndividualUKForm,
        ),
        (
            {"name": "joe", "eori_number": "GB205672212000"},
            True,
            {},
            forms.RegisterDetailsIndividualUKForm,
        ),
        ({}, False, {"name": ["Enter a name"]}, forms.RegisterDetailsIndividualOverseasForm),
        ({"name": "joe"}, True, {}, forms.RegisterDetailsIndividualOverseasForm),
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
            forms.RegisterDetailsCommercialUKForm,
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
            {},
            forms.RegisterDetailsCommercialUKForm,
        ),
    ),
)
def test_register_details_form_required_fields(
    data, valid, error, form_class, mock_request, mock_validate_registration_number
):
    form = form_class(data=data, request=mock_request)
    assert form.is_valid() == valid

    if not valid:
        assert form.errors == error


@pytest.mark.parametrize(
    "data, valid, error, form_class",
    (
        (
            {"name": "joe", "eori_number": "123"},
            False,
            {"eori_number": ["Invalid UK EORI number"]},
            forms.RegisterDetailsIndividualUKForm,
        ),
        (
            {"name": "joe", "eori_number": "123456789101112131"},
            False,
            {"eori_number": ["EORI numbers are 17 characters or less"]},
            forms.RegisterDetailsIndividualUKForm,
        ),
        (
            {"name": "joe", "eori_number": "GX205672212000"},
            False,
            {"eori_number": ["Invalid UK EORI number"]},
            forms.RegisterDetailsIndividualUKForm,
        ),
        (
            {"name": "joe", "eori_number": "GB205672212000", "registration_number": "123"},
            False,
            {"registration_number": ["Registration numbers are 8 numbers long"]},
            forms.RegisterDetailsIndividualUKForm,
        ),
        (
            {"name": "joe", "eori_number": "GB205672212000", "registration_number": "123456789101112131"},
            False,
            {"registration_number": ["Registration numbers are 8 numbers long"]},
            forms.RegisterDetailsIndividualUKForm,
        ),
        (
            {"name": "joe", "eori_number": "GB205672212000", "registration_number": "1234567FS"},
            False,
            {"registration_number": ["Registration numbers are 8 numbers long"]},
            forms.RegisterDetailsIndividualUKForm,
        ),
        (
            {
                "name": "joe",
                "eori_number": "GB205672212000",
                "vat_number": "GB123456789",
                "sic_number": "xyz",
                "registration_number": "1234567x",
            },
            False,
            {"sic_number": ["Only enter numbers"], "registration_number": ["Registration numbers are 8 numbers long"]},
            forms.RegisterDetailsCommercialOverseasForm,
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
            forms.RegisterDetailsCommercialOverseasForm,
        ),
    ),
)
def test_register_details_form_field_validation(
    data, valid, error, form_class, mock_request, mock_validate_registration_number
):
    form = form_class(data=data, request=mock_request)
    assert form.is_valid() == valid

    if not valid:
        assert form.errors == error


@pytest.mark.parametrize(
    "data, valid, error, form_class",
    (
        (
            {
                "name": "joe",
                "eori_number": "GB205672212000",
                "vat_number": "GB123456789",
                "sic_number": "12345",
                "registration_number": "12345678",
            },
            False,
            {"registration_number": ["This registration number is already in use."]},
            forms.RegisterDetailsCommercialUKForm,
        ),
    ),
)
def test_registration_number_validation_error(
    data, valid, error, form_class, mock_request, mock_registration_number_fail
):
    form = form_class(data=data, request=mock_request)
    assert form.is_valid() == valid

    if not valid:
        assert form.errors == error


@pytest.mark.parametrize(
    "data, valid, error",
    (
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
            {},
        ),
    ),
)
def test_register_address_details_validate_fields(data, valid, error):
    form = forms.RegisterAddressDetailsUKForm(is_individual=True, data=data)
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
                "phone_number": ["Enter a telephone number"],
                "address": ["Enter an address"],
                "country": ["Enter a country"],
            },
        ),
        (
            {
                "name": "joe",
                "address": "23 Long road home, no where land",
                "phone_number": "+441234567890",
                "country": "US",
            },
            True,
            {},
        ),
        (
            {
                "name": "joe",
                "address": "23 Long road home, no where land",
                "phone_number": "+441234567895",
                "country": "TH",
            },
            True,
            {},
        ),
    ),
)
def test_register_non_uk_address_details_form(data, valid, error, mock_request, mock_get_countries):
    form = forms.RegisterAddressDetailsOverseasForm(is_individual=False, data=data, request=mock_request)
    assert form.is_valid() == valid
    if not valid:
        assert form.errors == error


def test_select_organisation_form_invalid(data_organisations):

    form = forms.SelectOrganisationForm(organisations=data_organisations, data={})
    assert not form.is_valid()
    assert form.errors == {"organisation": ["Select an organisation"]}


def test_select_organisation_form_valid(data_organisations):

    form = forms.SelectOrganisationForm(
        organisations=data_organisations, data={"organisation": data_organisations[0]["id"]}
    )
    assert form.is_valid()
