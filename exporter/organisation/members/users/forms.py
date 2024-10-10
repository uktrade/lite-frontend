from crispy_forms_gds.layout import HTML
from crispy_forms_gds.choices import Choice
from django import forms
from django.db import models
from django.template.loader import render_to_string

from core.common.forms import BaseForm, TextChoice
from core.constants import ExporterRoles


class SelectRoleForm(BaseForm):
    class Layout:
        TITLE = "Who do you want to add?"

    class RoleChoices(models.TextChoices):
        AGENT_ROLE = ExporterRoles.agent.id, "An agent"
        EXPORTER_ROLE = ExporterRoles.exporter.id, "An exporter"
        ADMIN_ROLE = ExporterRoles.administrator.id, "An administrator"

    ROLE_CHOICES = (
        TextChoice(RoleChoices.AGENT_ROLE),
        TextChoice(RoleChoices.EXPORTER_ROLE),
        TextChoice(RoleChoices.ADMIN_ROLE),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select a role",
        },
    )

    def get_layout_fields(self):
        return (
            "role",
            HTML.details(
                "Help with roles",
                render_to_string("organisation/forms/members/help_with_roles.html"),
            ),
        )


class AddUserForm(BaseForm):
    class Layout:
        TITLE = ""

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

    def __init__(self, organisation_users, role_id, sites, *args, **kwargs):
        self.organisation_users = organisation_users
        role_name = [role.name for role in ExporterRoles.immutable_roles if role.id == role_id]
        self.Layout.TITLE = f"Add an {role_name[0]}"
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
                address.get("address_line_3"),
                address.get("city"),
                address.get("postcode"),
                address.get("country").get("name"),
            ],
        )
        return render_to_string("organisation/members/includes/site-address.html", {"site_address": site_address})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email in self.organisation_users:
            raise forms.ValidationError("Enter an email address that is not registered to this organisation")
        return email

    def get_layout_fields(self):
        return ("email", "sites")


class AgentDeclarationForm(BaseForm):
    class Layout:
        TITLE = "Declaration"

    def get_layout_fields(self):
        return (
            HTML.p(
                "I confirm that this agent is authorised to make and submit export licence applications"
                " on my behalf and that they have permission to manage all related queries."
            ),
        )
