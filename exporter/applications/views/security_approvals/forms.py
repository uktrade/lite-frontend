from datetime import datetime

from crispy_forms_gds.layout import HTML
from django import forms
from django.template.loader import render_to_string

from core.constants import SecurityClassifiedApprovalsType
from core.forms.layouts import (
    ConditionalRadiosQuestion,
    ConditionalRadios,
)
from core.forms.utils import coerce_str_to_bool

from exporter.core.validators import PastDateValidator
from exporter.core.forms import CustomErrorDateInputField
from core.common.forms import BaseForm


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
        help_text="This includes the release of United States ITAR (International Traffic in Arms regulations) material.",
        error_messages={
            "required": "Select no if you do not have an MOD security approval",
        },
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_mod_security_approved",
                "No",
                ConditionalRadiosQuestion(
                    "Yes",
                    "security_approvals",
                ),
            ),
            HTML.details(
                "Help with security approvals and ITAR",
                render_to_string("applications/forms/help_with_security_approvals.html"),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        is_mod_security_approved = cleaned_data.get("is_mod_security_approved")
        security_approvals = cleaned_data.get("security_approvals")
        if not is_mod_security_approved:
            cleaned_data["security_approvals"] = []
        if is_mod_security_approved and not security_approvals:
            self.add_error("security_approvals", "Select the type of security approval")
        return cleaned_data


class SubjectToITARControlsForm(BaseForm):
    class Layout:
        TITLE = "Are any products on this application subject to ITAR controls?"

    help_text = """
    We need to know if this export involves any defence articles including technical data that are
    subject to controls under the United States (US) International Traffic in Arms regulations (ITAR).
    """

    subject_to_itar_controls = forms.TypedChoiceField(
        choices=(
            (False, "No"),
            (True, "Yes"),
        ),
        coerce=coerce_str_to_bool,
        widget=forms.RadioSelect,
        label="Are any products on this application subject to ITAR controls?",
        help_text=help_text,
        error_messages={
            "required": "Select no if the products are not subject to ITAR controls",
        },
    )

    def get_layout_fields(self):
        return ("subject_to_itar_controls",)


class F680ReferenceNumberForm(BaseForm):
    class Layout:
        TITLE = "What is the F680 reference number?"

    f680_reference_number = forms.CharField(
        widget=forms.TextInput,
        label="What is the F680 reference number?",
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
        required=False,
        widget=forms.TextInput,
        label="What is the F1686 reference number?",
        help_text="Reference number (optional)",
    )

    f1686_approval_date = CustomErrorDateInputField(
        label="When was the F1686 approved?",
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
        label="Enter any details you have about the MOD contracting authority, reference numbers, "
        "the signatory of the approval, or the Project Security Instruction.",
        error_messages={
            "required": "Enter the details of your written approval",
        },
    )

    def get_layout_fields(self):
        return ("other_security_approval_details",)
