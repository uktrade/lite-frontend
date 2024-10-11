from django import forms
from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from crispy_forms_gds.layout import HTML

from core.common.forms import BaseForm, TextChoice
from exporter.core.services import get_countries
from .validators import (
    validate_vat,
    validate_eori,
    validate_phone,
    validate_registration,
    validate_sic_number,
)
from exporter.core.organisation.services import validate_registration_number


class RegistrationConfirmation(BaseForm):
    # This is just a dummy form which isn't rendered in the FE
    class Layout:
        TITLE = ""

    def get_layout_fields(self):
        return ()


class RegistrationTypeForm(BaseForm):
    class Layout:
        TITLE = "Select the type of organisation"

    class RegistrationTypeChoices(models.TextChoices):
        COMMERCIAL = ("commercial", "Commercial company")
        INDIVIDUAL = (
            "individual",
            "Other (such as individual, partnership, government, charity or educational institution)",
        )

    type = forms.ChoiceField(
        choices=[
            TextChoice(
                RegistrationTypeChoices.COMMERCIAL,
            ),
            TextChoice(
                RegistrationTypeChoices.INDIVIDUAL,
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
    SIC_CODE_LABEL = "Standard industrial classification (SIC code)"
    REGISTRATION_LABEL = "Companies House registration number (CRN)"

    class Layout:
        TITLE = "Enter organisation details"

    name = forms.CharField(
        label="Name",
        error_messages={
            "required": "Enter a name",
        },
    )

    eori_number = forms.CharField(
        label=EORI_LABEL,
        help_text=(
            """The first two letters are the country code, like GB or XI. This is followed by 12 or 15 numbers, like GB123456123456.
            <a href='https://www.gov.uk/eori' class='govuk-link govuk-link--no-visited-state'"
            "target='_blank'>Get an EORI number </a> if you don't have one."""
        ),
        error_messages={
            "required": "Enter an EORI number",
        },
        validators=[validate_eori],
    )

    sic_number = forms.CharField(
        label=SIC_CODE_LABEL,
        help_text=(
            "<a href='https://www.gov.uk/government/publications/standard-industrial-classification-of-economic-activities-sic'"
            "class='govuk-link govuk-link--no-visited-state' target='_blank'>Find your SIC code</a>.  If you have more than "
            "one, enter the SIC code you use most frequently."
        ),
        error_messages={
            "required": "Enter a SIC code",
        },
        validators=[validate_sic_number],
    )

    vat_number = forms.CharField(
        label=VAT_LABEL,
        help_text="""This is 9 numbers, sometimes with ‘GB’ at the start, for example 123456789 or GB123456789.
        You can find it on your VAT registration certificate.""",
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

    def __init__(self, *args, **kwargs):
        if kwargs.get("request"):
            self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_registration_number(self):
        if self.cleaned_data["registration_number"]:
            response, status_code = validate_registration_number(self.request, self.cleaned_data)
            if status_code != 200:
                self.add_error("registration_number", response["errors"]["registration_number"])
                return
        return self.cleaned_data["registration_number"]


class RegisterDetailsIndividualUKForm(RegisterDetailsBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["registration_number"].label = self.REGISTRATION_LABEL + " (optional)"
        self.fields["registration_number"].required = False

    def clean(self):
        for field in ["sic_number", "vat_number"]:
            if self.errors.get(field):
                del self.errors[field]
        super().clean()
        return

    def get_layout_fields(self):
        return ("name", "eori_number", "registration_number")


class RegisterDetailsIndividualOverseasForm(RegisterDetailsIndividualUKForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # individual non-uk
        self.fields["eori_number"].label = self.EORI_LABEL + " (optional)"
        self.fields["eori_number"].required = False


class RegisterDetailsCommercialUKForm(RegisterDetailsBaseForm):
    class Layout:
        TITLE = "Register a commercial organisation"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Name of organisation"

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

    website = forms.CharField(label="Website", help_text="Use the format https://www.example.com", required=False)

    def clean_website(self):
        website = self.cleaned_data.get("website")

        validator = URLValidator()

        if website:
            try:
                validator(website)
            except ValidationError:
                website = "https://" + website
                try:
                    validator(website)
                except ValidationError:
                    raise ValidationError("Enter a valid URL.")
                else:
                    return website
            else:
                return website

        return website

    def __init__(self, *args, **kwargs):
        if kwargs.get("request"):
            self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)


class RegisterAddressDetailsUKCommercialForm(RegisterAddressDetailsBaseForm):
    class Layout:
        TITLE = "What is your registered office address?"

    p1_address_help = HTML.details(
        "Help with your registered office address",
        "<p>This is usually the office address registered with Companies House. Or HM Revenue and Customs if you're not on Companies House.</p>"
        "<p>Your organisation might have multiple sites or business addresses, but there will only be one registered office.</p>",
    )

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
            "required": "Enter a county or state",
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
            self.p1_address_help,
        )


class RegisterAddressDetailsUKIndividualForm(RegisterAddressDetailsUKCommercialForm):

    class Layout:
        TITLE = "Where in the United Kingdom are you based?"

    name = forms.CharField(
        label="Name of headquarters",
        error_messages={
            "required": "Enter a name for your site",
        },
        help_text="Use the name 'Home' if you are providing the address where you live",
    )

    p1_address_help = HTML.details(
        "Help with providing your address",
        """<p>Provide your organisation's registered address if you have one. This is usually the office address registered with Companies House or HMRC.
        Your organisation might have multiple sites or business addresses, but there will only be one registered office.</p>""",
    )


class RegisterAddressDetailsOverseasCommercialForm(RegisterAddressDetailsBaseForm):
    class Layout:
        TITLE = "Where is your organisation based?"

    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}),
        label="Address",
        error_messages={
            "required": "Enter an address",
        },
    )
    country = forms.ChoiceField(
        choices=[],
        widget=forms.widgets.Select(attrs={"data-module": "autocomplete-select"}),
        error_messages={
            "required": "Enter a country",
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        countries = get_countries(self.request, False, ["GB"])
        country_choices = [("", "")] + [(country["id"], country["name"]) for country in countries]
        self.fields["country"].choices = country_choices

    def get_layout_fields(self):
        return ("name", "address", "phone_number", "website", "country")


class RegisterAddressDetailsOverseasIndividualForm(RegisterAddressDetailsOverseasCommercialForm):
    class Layout:
        TITLE = "What is your registered office address?"


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
