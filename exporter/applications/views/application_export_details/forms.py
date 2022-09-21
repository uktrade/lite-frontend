from datetime import datetime

from crispy_forms_gds.layout import HTML
from django import forms
from django.template.loader import render_to_string

from core.forms.layouts import (
    ConditionalQuestion,
    ConditionalRadios,
)

from exporter.core.validators import PastDateValidator
from exporter.core.forms import CustomErrorDateInputField
from exporter.core.common.forms import BaseForm, coerce_str_to_bool
from exporter.applications.constants import SecurityClassifiedApprovalsType


class SecurityClassifiedDetailsForm(BaseForm):
    class Layout:
        TITLE = "If you are exporting security classified products, you may need a Ministry of Defence (MOD) approval"

    security_approvals = forms.MultipleChoiceField(
        choices=SecurityClassifiedApprovalsType.choices,
        label="What type of approval do you have?",
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    is_mod_security_approved = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="Do you have an MOD security approval, such as F680 or F1686?",
        error_messages={
            "required": "Select no if you do not have an MOD security approval",
        },
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_mod_security_approved",
                "No",
                ConditionalQuestion(
                    "Yes",
                    "security_approvals",
                ),
            ),
            HTML.details(
                "Help with security approvals",
                render_to_string("applications/forms/help_with_security_approvals.html"),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        is_mod_security_approved = cleaned_data.get("is_mod_security_approved")
        mod_security_classified_approvals = cleaned_data.get("security_approvals")

        if is_mod_security_approved and not mod_security_classified_approvals:
            self.add_error("security_approvals", "Select the type of security approval")
        return cleaned_data


class F680ReferenceNumberForm(BaseForm):
    class Layout:
        TITLE = "What is the F680 reference number?"

    f680_reference_number = forms.CharField(
        widget=forms.TextInput,
        label="",
        error_messages={
            "required": " Enter the F680 reference number",
        },
    )

    def get_layout_fields(self):
        return ("f680_reference_number",)


class F1686DetailsForm(BaseForm):
    class Layout:
        TITLE = "Provide details of your F1686 approval"

    f1686_contracting_authority = forms.CharField(
        widget=forms.TextInput,
        label="Who is the contracting authority (or signatory and job role)?",
        error_messages={
            "required": "Enter the contracting authority (or signatory and job role)",
        },
    )

    f1686_reference_number = forms.CharField(
        widget=forms.TextInput,
        label="Reference number",
        error_messages={
            "required": "Enter a reference number",
        },
    )

    f1686_approval_date = CustomErrorDateInputField(
        label="Approval date",
        require_all_fields=False,
        help_text=f"For example, 20 2 {datetime.now().year-2}",
        error_messages={
            "required": "Enter the approval date",
            "incomplete": "Enter a approval date",
            "invalid": "Approval date must be a real date",
            "day": {
                "incomplete": "Approval date must include a day",
                "invalid": "Approval date be a real date",
            },
            "month": {
                "incomplete": "Approval date must include a month",
                "invalid": "Approval date must be a real date",
            },
            "year": {
                "incomplete": "Approval date must include a year",
                "invalid": "Approval date must be a real date",
            },
        },
        validators=[PastDateValidator("Approval date must be in the past")],
    )

    def get_layout_fields(self):
        return (
            "f1686_contracting_authority",
            "f1686_reference_number",
            "f1686_approval_date",
        )


class SecurityOtherDetailsForm(BaseForm):
    class Layout:
        TITLE = "Provide details of your written approval"

    other_security_approval_details = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        label="",
        help_text="Enter any details you have about the MOD contracting authority, reference numbers, the signatory of the approval, or the Project Security Instruction.",
        error_messages={
            "required": "Enter the details of your written approval",
        },
    )

    def get_layout_fields(self):
        return ("other_security_approval_details",)
