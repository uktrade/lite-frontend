from django import forms

from core.common.forms import BaseForm


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
                f"{request['recipient']['name']} - {request['recipient']['country']['name']} - {request['security_grading']['value']}",
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
        label="Select security grading",
        error_messages={"required": "Select the security grading"},
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
    )
    conditions = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7}),
        label="Provisos",
        required=False,
    )

    def get_layout_fields(self):
        return (
            "security_grading",
            "approval_types",
            "conditions",
        )


class RefuseOutcomeForm(BaseForm):
    class Layout:
        TITLE = "Refuse"

    refusal_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7}),
        label="Refusal reasons",
        required=True,
    )

    def get_layout_fields(self):
        return ("refusal_reasons",)
