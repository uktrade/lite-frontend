from django import forms
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from core.common.forms import BaseForm, CustomErrorDateInputField
from caseworker.f680.recommendation.constants import RecommendationSecurityGradingPrefix, RecommendationSecurityGrading
from caseworker.f680.outcome.constants import SecurityReleaseOutcomeDuration

from core.common.validators import (
    FutureDateValidator,
)


class SelectOutcomeForm(BaseForm):
    class Layout:
        TITLE = "Select outcome for one or more security releases"

    security_release_requests = forms.MultipleChoiceField(
        label="Security release requests",
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=(),
    )
    OUTCOME_CHOICES = [
        ("approve", "Approve"),
        ("refuse", "Refuse"),
    ]
    outcome = forms.ChoiceField(
        choices=OUTCOME_CHOICES,
        widget=forms.RadioSelect,
        label="Select outcome",
        error_messages={"required": "Select if you approve or refuse"},
    )

    def __init__(self, security_release_requests, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["security_release_requests"].choices = (
            [
                request["id"],
                f"{request['recipient']['name']} - {request['recipient']['country']['name']} - {request['security_grading_final']}",
            ]
            for request in security_release_requests
        )

    def get_layout_fields(self):
        return (
            "security_release_requests",
            "outcome",
        )


class ApproveOutcomeForm(BaseForm):
    class Layout:
        TITLE = "Approve"

    security_grading_choices = (
        ("official", "Official"),
        ("official-sensitive", "Official-Sensitive"),
        ("secret", "Secret"),
        ("top-secret", "Top Secret"),
    )
    security_grading = forms.ChoiceField(
        choices=security_grading_choices,
        widget=forms.RadioSelect,
        label="Select security release",
        error_messages={"required": "Select the security release"},
    )
    approval_types = forms.MultipleChoiceField(
        label="Approval types",
        required=True,
        widget=forms.CheckboxSelectMultiple,
        # TODO: Overlap here with the exporter choices - find a way to make it DRY
        choices=(
            ("initial_discussion_or_promoting", "Initial discussions or promoting products"),
            ("demonstration_in_uk", "Demonstration in the United Kingdom to overseas customers"),
            ("demonstration_overseas", "Demonstration overseas"),
            ("training", "Training"),
            ("through_life_support", "Through life support"),
            ("supply", "Supply"),
        ),
        error_messages={"required": "Select approval types"},
    )
    conditions = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7}),
        label="Conditions",
        required=False,
    )
    validity_start_date = CustomErrorDateInputField(
        label="Validity start date",
        help_text="For example 25 2 2025",
        require_all_fields=False,
        initial=timezone.now,
        error_messages={
            "required": "Enter the validity start date",
            "incomplete": "Enter the validity start date",
            "invalid": "Validity start date must be a real date",
            "day": {
                "incomplete": "Validity start date must include a day",
                "invalid": "Validity start date must be a real date",
            },
            "month": {
                "incomplete": "Validity start date must include a month",
                "invalid": "Validity start date must be a real date",
            },
            "year": {
                "incomplete": "Validity start date must include a year",
                "invalid": "Validity start date must be a real date",
            },
        },
        validators=[
            FutureDateValidator("Validity start date must be from today or in the future", include_today=True),
        ],
    )
    validity_period = forms.ChoiceField(
        choices=SecurityReleaseOutcomeDuration.choices,
        widget=forms.RadioSelect,
        label="Select validity period",
        initial=SecurityReleaseOutcomeDuration.MONTHS_24,
        error_messages={"required": "Select validity period"},
    )

    def __init__(self, all_approval_types, *args, **kwargs):
        super().__init__(*args, **kwargs)
        approval_type_choices = []
        for choice_key, choice_value in self.fields["approval_types"].choices:
            if choice_key in all_approval_types:
                approval_type_choices.append((choice_key, choice_value))
        self.fields["approval_types"].choices = approval_type_choices

    def clean(self):
        cleaned_data = super().clean()

        validity_start_date = cleaned_data.get("validity_start_date", None)
        validity_period = cleaned_data.pop("validity_period", None)
        validity_end_date = None

        if validity_start_date and validity_period:
            duration = int(validity_period)
            validity_end_date = validity_start_date + relativedelta(months=duration)

        return {
            **cleaned_data,
            "validity_start_date": validity_start_date.isoformat() if validity_start_date else "",
            "validity_end_date": validity_end_date.isoformat() if validity_end_date else "",
        }

    def get_layout_fields(self):
        return (
            "security_grading",
            "approval_types",
            "validity_start_date",
            "validity_period",
            "conditions",
        )


class RefuseOutcomeForm(BaseForm):
    class Layout:
        TITLE = "Refuse"

    refusal_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7}),
        label="Refusal reasons",
        required=True,
        error_messages={"required": "Enter refusal reasons"},
    )

    def get_layout_fields(self):
        return ("refusal_reasons",)
