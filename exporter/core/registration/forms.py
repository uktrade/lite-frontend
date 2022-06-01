import re
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Layout, Submit
from django.core.validators import URLValidator, ValidationError
import phonenumbers
from django import forms
from .constants import Validation


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        for field in self.fields.values():
            if isinstance(field, forms.FileField):
                self.helper.attrs = {"enctype": "multipart/form-data"}
                break

        self.helper.layout = Layout(HTML.h1(self.Layout.TITLE), *self.get_layout_fields(), *self.get_layout_actions())

    def get_layout_fields(self):
        raise NotImplementedError(f"Implement `get_layout_fields` on {self.__class__.__name__}")

    def get_layout_actions(self):
        return [
            Submit("submit", getattr(self.Layout, "SUBMIT_BUTTON", "Continue")),
        ]


class RegistrationTypeForm(BaseForm):
    class Layout:
        TITLE = "Commercial organisation or private individual"

    type = forms.TypedChoiceField(
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

    location = forms.TypedChoiceField(
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


class RegisterIndividualDetailsForm(BaseForm):
    class Layout:
        TITLE = "Register a private individual"

    name = forms.CharField(
        label="First and last name",
        error_messages={
            "required": "Enter a name",
        },
    )

    eori_number = forms.CharField(
        label="European Union registration and identification number (EORI)",
        error_messages={
            "required": "Enter a EORI number",
        },
    )

    vat_number = forms.CharField(required=False, label="UK VAT number This field is (optional)")

    def clean_eori_number(self):
        value = self.cleaned_data["eori_number"]
        if value:
            eori = re.sub(r"[^A-Z0-9]", "", value)
            if len(eori) > Validation.UK_EORI_MAX_LENGTH:
                self.add_error("eori_number", "EORI numbers are 17 characters or less")
            elif not re.match(Validation.UK_EORI_VALIDATION_REGEX, eori):
                self.add_error("eori_number", "Invalid UK EORI number")
            return eori

    def clean_vat_number(self):
        value = self.cleaned_data["vat_number"]
        if value:
            stripped_vat = re.sub(r"[^A-Z0-9]", "", value)
            if len(stripped_vat) < Validation.UK_VAT_MIN_LENGTH:
                self.add_error("vat_number", "Standard UK VAT numbers are 9 digits long")
            elif len(stripped_vat) > Validation.UK_VAT_MAX_LENGTH:
                self.add_error("vat_number", "Standard UK VAT numbers are 9 digits long")
            elif not re.match(Validation.UK_VAT_VALIDATION_REGEX, stripped_vat):
                self.add_error("vat_number", "Invalid UK VAT number")
            return stripped_vat
        return value

    def get_layout_fields(self):
        return ("name", "eori_number", "vat_number")


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
    )

    website = forms.CharField(
        label="Website",
        required=False,
    )

    country = forms.CharField(
        label="Country",
        error_messages={
            "required": "Enter a country",
        },
    )

    def clean(self):
        if self.is_uk_based:
            errors_to_remove = {"address", "country"}.intersection(set(self.errors.keys()))
        else:
            errors_to_remove = {"address_line_1", "address_line_2", "city", "region", "postcode"}.intersection(
                set(self.errors.keys())
            )

        for field in errors_to_remove:
            del self.errors[field]
        return

    def clean_phone_number(self):
        value = self.cleaned_data["phone_number"]
        try:
            phone_number = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone_number):
                self.add_error("phone_number", "Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            self.add_error("phone_number", "Invalid phone number")
        return value

    def clean_website(self):
        value = self.cleaned_data["website"]
        if value:
            try:
                validator = URLValidator()
                validator(value)
            except ValidationError:
                self.add_error("website", "Enter a valid URL")
        return value

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
