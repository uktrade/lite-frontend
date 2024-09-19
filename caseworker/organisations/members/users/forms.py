from crispy_forms_gds.layout import HTML
from crispy_forms_gds.choices import Choice
from django import forms
from django.template.loader import render_to_string

from core.common.forms import BaseForm


class AddAdminExporterUserForm(BaseForm):
    class Layout:
        TITLE = "Add an administrator"
        SUBMIT_BUTTON_TEXT = "Save"

    email = forms.EmailField(
        label="Email",
        error_messages={
            "required": "Enter an email address in the correct format, like name@example.com",
        },
    )

    sites = forms.MultipleChoiceField(
        choices=(),
        error_messages={
            "required": "Select at least one site",
        },
        label="Sites",
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self, organisation_users, sites, cancel_url, *args, **kwargs):
        self.cancel_url = cancel_url
        self.organisation_users = organisation_users
        site_choices = [Choice(x["id"], x["name"], hint=self.format_address(x.get("address", {}))) for x in sites]
        self.declared_fields["sites"].choices = site_choices
        super().__init__(*args, **kwargs)

    def format_address(self, address):

        site_address = filter(
            None,
            [
                address.get("address"),
                address.get("address_line_1"),
                address.get("address_line_2"),
                address.get("city"),
                address.get("postcode"),
                address.get("country").get("name"),
            ],
        )
        return render_to_string("organisations/organisation/includes/site-address.html", {"site_address": site_address})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email in self.organisation_users:
            raise forms.ValidationError("Enter an email address that is not registered to this organisation")
        return email

    def get_layout_fields(self):
        return (
            "email",
            "sites",
        )

    def get_layout_actions(self):
        layout_actions = super().get_layout_actions()

        layout_actions.append(
            HTML(
                f'<a class="govuk-button govuk-button--secondary" href="{self.cancel_url}" id="cancel-id-cancel">Cancel</a>'
            ),
        )
        return layout_actions
