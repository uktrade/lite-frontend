from django import forms
from datetime import datetime

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
        TITLE = "Some security classified products need an approval before they can be exported"

    security_approvals = forms.MultipleChoiceField(
        choices=SecurityClassifiedApprovalsType.choices,
        label="",
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    has_security_approval = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="Do you have a Ministry of Defence security approval (such as F680 or F1686)?",
        error_messages={
            "required": "Select yes if product's are security required",
        },
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "has_security_approval",
                "No",
                ConditionalQuestion(
                    "Yes",
                    "security_approvals",
                ),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        has_security_approval = cleaned_data.get("has_security_approval")
        mod_security_classified_approvals = cleaned_data.get("security_approvals")

        if has_security_approval and not mod_security_classified_approvals:
            self.add_error("security_approvals", "Select at least 1 security approval")
        return cleaned_data


class F680ReferenceNumberForm(BaseForm):
    class Layout:
        TITLE = "What is the F680 reference number?"

    f680_reference_number = forms.CharField(
        widget=forms.TextInput,
        label="",
        error_messages={
            "required": "Enter a reference number",
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
            "required": "Enter a contracting authority",
        },
    )

    is_f1686_approval_document_available = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="Do you have an approval document to upload?",
        error_messages={
            "required": "Select if you have an approval document",
        },
    )

    f1686_approval_document = forms.FileField(
        label="Upload the approval document",
        error_messages={
            "required": "Select an approval document",
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
            ConditionalRadios(
                "is_f1686_approval_document_available",
                ConditionalQuestion(
                    "Yes",
                    "f1686_approval_document",
                ),
                ConditionalQuestion(
                    "No",
                    "f1686_reference_number",
                    "f1686_approval_date",
                ),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        is_f1686_approval_document_available = cleaned_data.get("is_f1686_approval_document_available")
        if is_f1686_approval_document_available is False:
            # Remove the default error as the message
            self.errors.pop("f1686_approval_document", None)
        elif is_f1686_approval_document_available is True:
            self.errors.pop("f1686_reference_number", None)
            self.errors.pop("f1686_approval_date", None)
        elif is_f1686_approval_document_available is None:
            # Remove the default error as the message
            self.errors.pop("f1686_approval_document", None)
            self.errors.pop("f1686_reference_number", None)
            self.errors.pop("f1686_approval_date", None)
        return cleaned_data


class SecurityOtherDetailsForm(BaseForm):
    class Layout:
        TITLE = "Provide details of your approval"

    other_security_approval_details = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        label="Provide as much information as possible, such as...",
        error_messages={
            "required": "Enter approval details",
        },
    )

    other_security_approval_document = forms.FileField(
        label="Upload any supporting documents (optional)",
        required=False,
    )

    def get_layout_fields(self):
        return (
            "other_security_approval_details",
            "other_security_approval_document",
        )
