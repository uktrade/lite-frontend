from django.urls import reverse_lazy

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit, Field, HTML, Div
from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def validate_website(value):
    if value:
        try:
            validator = URLValidator()
            validator(value)
        except ValidationError:
            raise ValidationError("Enter a valid URL")
    return value


class AddAdditionalContactForm(forms.Form):
    details = forms.CharField(label="Information about the contact")
    name = forms.CharField(label="Full name")
    address = forms.CharField(label="Address", widget=forms.Textarea)
    email = forms.EmailField(label="Email address")
    phone_number = forms.CharField(label="Phone number", help_text="For international numbers include the country code")
    website = forms.CharField(label="Website", required=False, validators=[validate_website])
    country = forms.ChoiceField(label="Country", choices=())

    def __init__(self, *args, **kwargs):
        country = kwargs.pop("country", [])
        super().__init__(*args, **kwargs)
        self.fields["country"].choices = country

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("details"),
            Field("name"),
            Field("address"),
            Field("email"),
            Field("phone_number"),
            Field("website"),
            Field("country"),
            Submit("submit", "Save and continue"),
        )
