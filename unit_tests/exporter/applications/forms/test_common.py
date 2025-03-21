import pytest

from exporter.applications.forms.common import (
    ApplicationNameForm,
    LicenceTypeForm,
    ToldByAnOfficialForm,
)


@pytest.mark.parametrize(
    "data, is_valid, cleaned_data, errors",
    (
        ({"application_type": "siel"}, True, {"application_type": "siel"}, {}),
        (
            {"application_type": "ogel"},
            False,
            {},
            {"application_type": ["Select a valid choice. ogel is not one of the available choices."]},
        ),
        (
            {"application_type": "oiel"},
            False,
            {},
            {"application_type": ["Select a valid choice. oiel is not one of the available choices."]},
        ),
    ),
)
def test_licence_type_form(data, is_valid, cleaned_data, errors):
    form = LicenceTypeForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
    assert form.cleaned_data == cleaned_data


@pytest.mark.parametrize(
    "data, is_valid, cleaned_data, errors",
    (
        ({"name": "name of application"}, True, {"name": "name of application"}, {}),
        ({}, False, {}, {"name": ["This field is required."]}),
        ({"name": ""}, False, {}, {"name": ["This field is required."]}),
    ),
)
def test_application_name_form(data, is_valid, cleaned_data, errors):
    form = ApplicationNameForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
    assert form.cleaned_data == cleaned_data


@pytest.mark.parametrize(
    "data, is_valid, cleaned_data, errors",
    (
        (
            {"have_you_been_informed": "yes", "reference_number_on_information_form": "CRE/2020/1234567"},
            True,
            {"have_you_been_informed": "yes", "reference_number_on_information_form": "CRE/2020/1234567"},
            {},
        ),
        (
            {"have_you_been_informed": "no", "reference_number_on_information_form": "CRE/2020/1234567"},
            True,
            {"have_you_been_informed": "no", "reference_number_on_information_form": ""},
            {},
        ),
        (
            {"have_you_been_informed": "no"},
            True,
            {"have_you_been_informed": "no", "reference_number_on_information_form": ""},
            {},
        ),
        (
            {"have_you_been_informed": "yes"},
            True,
            {"have_you_been_informed": "yes", "reference_number_on_information_form": ""},
            {},
        ),
        (
            {},
            False,
            {"reference_number_on_information_form": ""},
            {"have_you_been_informed": ["This field is required."]},
        ),
    ),
)
def test_told_by_an_official_form_reference_number_removed_if_not_informed(data, is_valid, cleaned_data, errors):
    form = ToldByAnOfficialForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors
    assert form.cleaned_data == cleaned_data
