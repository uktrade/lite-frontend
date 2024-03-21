from django import forms
from django.db import models

from crispy_forms_gds.layout import HTML

from core.common.forms import BaseForm, TextChoice
from .validators import (
    validate_vat,
    validate_eori,
    validate_phone,
    validate_website,
    validate_registration,
    validate_sic_number,
)


class RegistrationTypeForm(BaseForm):
    class Layout:
        TITLE = "Commercial organisation or private individual"

    class RegistrationTypeChoices(models.TextChoices):
        COMMERCIAL = ("commercial", "Commercial organisation")
        INDIVIDUAL = ("individual", "Private individual")

    type = forms.ChoiceField(
        choices=[
            TextChoice(
                RegistrationTypeChoices.COMMERCIAL,
                hint="Select this if you want to register an organisation that will be exporting",
            ),
            TextChoice(
                RegistrationTypeChoices.INDIVIDUAL,
                hint="Select this if you're a private individual that will be exporting alone",
            ),
        ],
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select the type of organisation you're registering for",
        },
    )

    def get_layout_fields(self):
        return ("type",)


class RegistrationUKBasedForm(BaseForm):
    class Layout:
        TITLE = "Where is your organisation based?"

    location = forms.ChoiceField(
        choices=(
            ("united_kingdom", "In the United Kingdom"),
            ("abroad", "Outside of the United Kingdom"),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select a location",
        },
    )

    def get_layout_fields(self):
        return ("location",)


class RegisterDetailsBaseForm(BaseForm):

    VAT_LABEL = "UK VAT number"
    EORI_LABEL = "European Union registration and identification number (EORI)"
    SIC_CODE_LABEL = "SIC Code"
    REGISTRATION_LABEL = "Company registration number (CRN)"

    class Layout:
        TITLE = "Register a private individual"

    name = forms.CharField(
        label="First and last name",
        error_messages={
            "required": "Enter a name",
        },
    )

    eori_number = forms.CharField(
        label=EORI_LABEL,
        help_text=(
            "<a href='https://www.gov.uk/eori' class='govuk-link govuk-link--no-visited-state'"
            "target='_blank'>Get an EORI number </a> if you don't have one."
        ),
        error_messages={
            "required": "Enter a EORI number",
        },
        validators=[validate_eori],
    )

    sic_number = forms.CharField(
        label=SIC_CODE_LABEL,
        help_text=(
            "<a href='https://www.gov.uk/government/publications/standard-industrial-classification-of-economic-activities-sic'"
            "class='govuk-link govuk-link--no-visited-state' target='_blank'>Find your SIC code.</a>"
        ),
        error_messages={
            "required": "Enter a SIC code",
        },
        validators=[validate_sic_number],
    )

    vat_number = forms.CharField(
        label=VAT_LABEL,
        help_text="9 digits long, with the first 2 letters indicating the country code of the registered business.",
        validators=[validate_vat],
    )
    registration_number = forms.CharField(
        label=REGISTRATION_LABEL,
        help_text="8 numbers, or 2 letters followed by 6 numbers.",
        error_messages={
            "required": "Enter a registration number",
        },
        validators=[validate_registration],
    )


class RegisterDetailsIndividualUKForm(RegisterDetailsBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = "First and last name"
        self.Layout.TITLE = "Register a private individual"
        self.fields["vat_number"].label = self.REGISTRATION_LABEL + " (optional)"
        self.fields["vat_number"].required = False

    def clean(self):
        for field in ["sic_number", "registration_number"]:
            if self.errors.get(field):
                del self.errors[field]
        return

    def get_layout_fields(self):
        return ("name", "eori_number", "vat_number")


class RegisterDetailsIndividualOverseasForm(RegisterDetailsIndividualUKForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # individual non-uk
        self.fields["eori_number"].label = self.EORI_LABEL + " (optional)"
        self.fields["eori_number"].required = False


class RegisterDetailsCommercialUKForm(RegisterDetailsBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Name of organisation"
        self.Layout.TITLE = "Register a commercial organisation"

    def get_layout_fields(self):
        return ("name", "eori_number", "sic_number", "vat_number", "registration_number")


class RegisterDetailsCommercialOverseasForm(RegisterDetailsCommercialUKForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["eori_number"].label = self.EORI_LABEL + " (optional)"
        self.fields["eori_number"].required = False
        self.fields["sic_number"].label = self.SIC_CODE_LABEL + " (optional)"
        self.fields["sic_number"].required = False
        self.fields["vat_number"].label = self.VAT_LABEL + " (optional)"
        self.fields["vat_number"].required = False
        self.fields["registration_number"].label = self.REGISTRATION_LABEL + " (optional)"
        self.fields["registration_number"].required = False


class RegisterAddressDetailsBaseForm(BaseForm):

    name = forms.CharField(
        label="Name of headquarters",
        error_messages={
            "required": "Enter a name for your site",
        },
    )

    phone_number = forms.CharField(
        label="Organisation telephone number",
        help_text="For international numbers include the country code",
        error_messages={
            "required": "Enter a telephone number",
        },
        validators=[validate_phone],
    )

    website = forms.CharField(label="Website", required=False, validators=[validate_website])


class RegisterAddressDetailsUKForm(RegisterAddressDetailsBaseForm):
    class Layout:
        TITLE = "What is your registered office address?"

    def __init__(self, is_individual, *args, **kwargs):
        if is_individual:
            self.Layout.TITLE = "Where in the United Kingdom are you based?"
        super().__init__(*args, **kwargs)

    address_line_1 = forms.CharField(
        label="Building and street",
        error_messages={
            "required": "Enter a real building and street name",
        },
    )
    address_line_2 = forms.CharField(
        label="",
        required=False,
    )

    city = forms.CharField(
        label="Town or city",
        error_messages={
            "required": "Enter a real city",
        },
    )
    region = forms.CharField(
        label="County or state",
        error_messages={
            "required": "Enter a real region",
        },
    )

    postcode = forms.CharField(
        label="Postcode",
        error_messages={
            "required": "Enter a real postcode",
        },
    )

    def get_layout_fields(self):
        return (
            "name",
            "address_line_1",
            "address_line_2",
            "city",
            "region",
            "postcode",
            "phone_number",
            "website",
            HTML.details(
                "Help with your registered office address",
                "<p>This is usually the office address registered with Companies House. Or HM Revenue and Customs if you're not on Companies House.</p>"
                "<p>Your organisation might have multiple sites or business addresses, but there will only be one registered office.</p>",
            ),
        )


class RegisterAddressDetailsOverseasForm(RegisterAddressDetailsBaseForm):
    class Layout:
        TITLE = "Where is your organisation based?"

    def __init__(self, is_individual, *args, **kwargs):
        if is_individual:
            self.Layout.TITLE = "What is your registered office address?"
        super().__init__(*args, **kwargs)

    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}),
        label="Address",
        error_messages={
            "required": "Enter an address",
        },
    )

    country = forms.CharField(
        label="Country",
        error_messages={
            "required": "Enter a country",
        },
    )

    def get_layout_fields(self):
        return ("name", "address", "phone_number", "website", "country")


class SelectOrganisationForm(BaseForm):
    class Layout:
        TITLE = "Select your organisation"
        SUBTITLE = "You can switch between organisations from your dashboard."

    organisation = forms.ChoiceField(
        choices=(),
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select an organisation",
        },
    )

    def __init__(self, organisations, *args, **kwargs):
        organisation_choices = [(x["id"], x["name"]) for x in organisations]
        self.declared_fields["organisation"].choices = organisation_choices
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return ("organisation",)
