from django import forms

from exporter.core.common.forms import BaseForm
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

    type = forms.ChoiceField(
        choices=(
            ("commercial", "Commercial organisation"),
            ("individual", "Private individual"),
        ),
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


class RegisterDetailsForm(BaseForm):
    class Layout:
        TITLE = "Register a private individual"

    def __init__(self, is_individual, *args, **kwargs):
        self.is_individual = is_individual
        if self.is_individual:
            self.declared_fields["name"].label = "First and last name"
            self.Layout.TITLE = "Register a private individual"
            self.declared_fields["vat_number"].label = "UK VAT number (optional)"
            self.declared_fields["vat_number"].required = False

        else:
            self.declared_fields["name"].label = "Name of organisation"
            self.Layout.TITLE = "Register a commercial organisation"
            self.declared_fields["vat_number"].label = "UK VAT number"
            self.declared_fields["vat_number"].required = True

        super().__init__(*args, **kwargs)

    name = forms.CharField(
        label="First and last name",
        error_messages={
            "required": "Enter a name",
        },
    )

    eori_number = forms.CharField(
        label="European Union registration and identification number (EORI)",
        error_messages={
            "required": "Enter an EORI number",
        },
        validators=[validate_eori],
    )

    sic_number = forms.CharField(
        label="SIC Code",
        error_messages={
            "required": "Enter a SIC code",
        },
        validators=[validate_sic_number],
    )

    vat_number = forms.CharField(required=False, label="UK VAT number (optional)", validators=[validate_vat])
    registration_number = forms.CharField(
        label="Company registration number (CRN)",
        error_messages={
            "required": "Enter a registration number",
        },
        validators=[validate_registration],
    )

    def clean(self):
        if self.is_individual:
            for field in ["sic_number", "registration_number"]:
                if self.errors.get(field):
                    del self.errors[field]
        return

    def get_layout_fields(self):
        if self.is_individual:
            return ("name", "eori_number", "vat_number")
        else:
            return ("name", "eori_number", "sic_number", "vat_number", "registration_number")


class RegisterAddressDetailsForm(BaseForm):
    class Layout:
        TITLE = "Where in the United Kingdom are you based?"

    def __init__(self, is_uk_based, *args, **kwargs):
        self.is_uk_based = is_uk_based
        self.Layout.TITLE = "Where in the United Kingdom are you based?" if self.is_uk_based else "Where are you based?"

        super().__init__(*args, **kwargs)

    name = forms.CharField(
        label="Name of headquarters",
        error_messages={
            "required": "Enter a name for your site",
        },
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}),
        label="Address",
        error_messages={
            "required": "Enter an address",
        },
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
            "required": "Enter a real region",
        },
    )

    postcode = forms.CharField(
        label="Postcode",
        error_messages={
            "required": "Enter a real postcode",
        },
    )

    phone_number = forms.CharField(
        label="Phone number",
        error_messages={
            "required": "Enter a phone number",
        },
        validators=[validate_phone],
    )

    website = forms.CharField(label="Website", required=False, validators=[validate_website])

    country = forms.CharField(
        label="Country",
        error_messages={
            "required": "Enter a country",
        },
    )

    def clean(self):
        errors_to_remove = (
            {"address", "country"}
            if self.is_uk_based
            else {"address_line_1", "address_line_2", "city", "region", "postcode"}
        )

        for field in errors_to_remove:
            if self.errors.get(field):
                del self.errors[field]
        return

    def get_layout_fields(self):
        if self.is_uk_based:
            return (
                "name",
                "address_line_1",
                "address_line_2",
                "city",
                "region",
                "postcode",
                "phone_number",
                "website",
            )
        else:
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


class RegistrationEditName(BaseForm):
    class Layout:
        TITLE = "First and last name"

    name = forms.CharField(
        label="First and last name",
        error_messages={
            "required": "Enter a name",
        },
    )

    def get_layout_fields(self):
        return ("name",)


class RegistrationEditEoriNumber(BaseForm):
    class Layout:
        TITLE = "EORI number"

    eori_number = forms.CharField(
        label="European Union registration and identification number (EORI)",
        error_messages={
            "required": "Enter an EORI number",
        },
        validators=[validate_eori],
    )

    def get_layout_fields(self):
        return ("eori_number",)


class RegistrationEditVatNumber(BaseForm):
    class Layout:
        TITLE = "UK VAT number"

    vat_number = forms.CharField(required=False, label="UK VAT number (optional)", validators=[validate_vat])

    def get_layout_fields(self):
        return ("vat_number",)


class RegistrationEditSICNumber(BaseForm):
    class Layout:
        TITLE = "SIC Code"

    sic_number = forms.CharField(
        label="SIC Code",
        error_messages={
            "required": "Enter a SIC code",
        },
        validators=[validate_sic_number],
    )

    def get_layout_fields(self):
        return ("sic_number",)


class RegistrationEditRegistrationNumber(BaseForm):
    class Layout:
        TITLE = "Company registration number"

    registration_number = forms.CharField(
        label="Company registration number (CRN)",
        error_messages={
            "required": "Enter a registration number",
        },
        validators=[validate_registration],
    )

    def get_layout_fields(self):
        return ("registration_number",)


class RegistrationEditAddressName(BaseForm):
    class Layout:
        TITLE = "Name of headquarters"

    name = forms.CharField(
        label="Name of headquarters",
        error_messages={
            "required": "Enter a name for your site",
        },
    )

    def get_layout_fields(self):
        return ("name",)


class RegistrationEditAddress(BaseForm):
    class Layout:
        TITLE = "Address"

    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}),
        label="Address",
        error_messages={
            "required": "Enter an address",
        },
    )

    def get_layout_fields(self):
        return ("address",)


class RegistrationEditAddress1(BaseForm):
    class Layout:
        TITLE = "Change address1"

    address_line_1 = forms.CharField(
        label="Building and street",
        error_messages={
            "required": "Enter a real building and street name",
        },
    )

    def get_layout_fields(self):
        return ("address_line_1",)


class RegistrationEditAddress2(BaseForm):
    class Layout:
        TITLE = "Address"

    address_line_2 = forms.CharField(
        label="",
        required=False,
    )

    def get_layout_fields(self):
        return ("address_line_2",)


class RegistrationEditCity(BaseForm):
    class Layout:
        TITLE = "City"

    city = forms.CharField(
        label="Town or city",
        error_messages={
            "required": "Enter a real city",
        },
    )

    def get_layout_fields(self):
        return ("city",)


class RegistrationEditRegion(BaseForm):
    class Layout:
        TITLE = "County or state"

    region = forms.CharField(
        label="County or state",
        error_messages={
            "required": "Enter a real region",
        },
    )

    def get_layout_fields(self):
        return ("region",)


class RegistrationEditPostCode(BaseForm):
    class Layout:
        TITLE = "Postcode"

    postcode = forms.CharField(
        label="Postcode",
        error_messages={
            "required": "Enter a real postcode",
        },
    )

    def get_layout_fields(self):
        return ("postcode",)


class RegistrationEditPhoneNumber(BaseForm):
    class Layout:
        TITLE = "Phone number"

    phone_number = forms.CharField(
        label="Phone number",
        error_messages={
            "required": "Enter a phone number",
        },
        validators=[validate_phone],
    )

    def get_layout_fields(self):
        return ("phone_number",)


class RegistrationEditWebsite(BaseForm):
    class Layout:
        TITLE = "Website"

    website = forms.CharField(label="Website", required=False, validators=[validate_website])

    def get_layout_fields(self):
        return ("website",)


class RegistrationEditCountry(BaseForm):
    class Layout:
        TITLE = "Country"

    country = forms.CharField(
        label="Country",
        error_messages={
            "required": "Enter a country",
        },
    )

    def get_layout_fields(self):
        return ("country",)
