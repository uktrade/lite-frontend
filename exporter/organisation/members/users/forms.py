from crispy_forms_gds.layout import HTML
from django import forms
from django.db import models

from crispy_forms_gds.choices import Choice
from exporter.core.common.forms import BaseForm

from exporter.core.constants import Roles
from django.core.validators import validate_email
from django.template.loader import render_to_string


class TextChoice(Choice):
    def __init__(self, choice, **kwargs):
        super().__init__(choice.value, choice.label, **kwargs)


class SelectRoleForm(BaseForm):
    class Layout:
        TITLE = "Who do you want to add?"

    class RoleChoices(models.TextChoices):
        AGENT_ROLE = Roles.AGENT_USER_ROLE[0], "An agent"
        EXPORTER_ROLE = Roles.EXPORTER_USER_ROLE[0], "An exporter"
        ADMIN_ROLE = Roles.ADMINISTRATOR_USER_ROLE[0], "An administrator"

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
            "required": "Please select a role",
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

    email = forms.CharField(
        label="email",
        validators=[validate_email],
        error_messages={
            "required": "Enter an email address",
        },
    )

    sites = forms.MultipleChoiceField(
        choices=(),
        error_messages={
            "required": "Please select at least one site",
        },
        label="Sites",
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self, request, role_id, sites, *args, **kwargs):
        self.request = request
        role_name = [item[1] for item in Roles.IMMUTABLE_ROLES if item[0] == role_id]
        self.Layout.TITLE = f"Add an {role_name[0]}"
        site_choices = [(x["id"], x["name"] + "<html>") for x in sites]

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
        return render_to_string("organisation/members/includes/site-address.html", {"site_address": site_address})

    def get_layout_fields(self):
        return ("email", "sites")


class AgentDeclarationForm(BaseForm):
    class Layout:
        TITLE = "Declaration"

    def get_layout_fields(self):
        return (
            HTML.p(
                "I authorise this agent to make and submit export license applications on my behalf. I give permision to manage all related queries.",
            ),
        )
