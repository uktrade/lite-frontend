from django import forms
from django.forms.formsets import formset_factory
from django.utils.html import format_html

from core.common.forms import BaseForm
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Layout, Submit
from crispy_forms_gds.choices import Choice

from core.forms.layouts import (
    ConditionalCheckboxes,
    ConditionalCheckboxesQuestion,
    ConditionalRadios,
    ConditionalRadiosQuestion,
    ExpandingFieldset,
    RadioTextArea,
)
from core.forms.utils import coerce_str_to_bool
from caseworker.tau.summaries import get_good_on_application_tau_summary
from caseworker.tau.widgets import GoodsMultipleSelect
from core.forms.widgets import GridmultipleSelect


def get_approval_advice_form_factory(advice, approval_reason, proviso, footnote_details, data=None):
    data = data or {
        "proviso": advice["proviso"],
        "approval_reasons": advice["text"],
        "instructions_to_exporter": advice["note"],
        "footnote_details": advice["footnote"],
    }
    return GiveApprovalAdviceForm(
        approval_reason=approval_reason, proviso=proviso, footnote_details=footnote_details, data=data
    )


def get_refusal_advice_form_factory(advice, denial_reasons_choices, refusal_reasons, data=None):
    data = data or {
        "refusal_reasons": advice["text"],
        "denial_reasons": [r for r in advice["denial_reasons"]],
    }
    return RefusalAdviceForm(data=data, choices=denial_reasons_choices, refusal_reasons=refusal_reasons)


class PicklistCharField(forms.CharField):
    def get_help_html(self, picklist_attrs, help_link_text, help_text_extra=None):
        picklist_tags = f'picklist_type="{picklist_attrs.get("type")}" picklist_name="{picklist_attrs.get("name")}" target="{picklist_attrs.get("target")}"'
        help_html = f'<a class="govuk-link govuk-link--no-visited-state" href="#" {picklist_tags}>{help_link_text}</a>'
        if help_text_extra:
            help_html = f"{help_text_extra}<br/>{help_html}"
        return help_html

    def __init__(self, picklist_attrs, label, help_link_text, help_text_extra=None, **kwargs):
        min_rows = kwargs.pop("min_rows", 10)
        help_link = self.get_help_html(picklist_attrs, help_link_text, help_text_extra)
        widget = forms.Textarea(attrs={"rows": str(min_rows), "class": "govuk-!-margin-top-4"})
        super().__init__(label=label, help_text=help_link, widget=widget, **kwargs)


class SelectAdviceForm(forms.Form):
    CHOICES = [("approve_all", "Approve all"), ("refuse_all", "Refuse all")]

    recommendation = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select if you approve all or refuse all"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Continue"))


class ConsolidateSelectAdviceForm(SelectAdviceForm):
    DOCUMENT_TITLE = "Recommend and combine case recommendation case"
    CHOICES = [("approve", "Approve"), ("refuse", "Refuse")]
    recommendation = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select if you approve or refuse"},
    )

    def __init__(self, team_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        recommendation_label = "What is the combined recommendation"
        if team_name:
            recommendation_label = f"{recommendation_label} for {team_name}"
        self.fields["recommendation"].label = f"{recommendation_label}?"


class PicklistAdviceForm(forms.Form):
    def _picklist_to_choices(self, picklist_data):
        reasons_choices = []
        reasons_text = {"other": ""}

        for result in picklist_data["results"]:
            key = "_".join(result.get("name").lower().split())
            choice = Choice(key, result.get("name"))
            if result == picklist_data["results"][-1]:
                choice = Choice(key, result.get("name"), divider="or")
            reasons_choices.append(choice)
            reasons_text[key] = result.get("text")
        reasons_choices.append(Choice("other", "Other"))
        return reasons_choices, reasons_text


class GiveApprovalAdviceForm(PicklistAdviceForm):
    DOCUMENT_TITLE = "Recommend approval for this case"
    approval_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7, "class": "govuk-!-margin-top-4"}),
        label="",
        error_messages={"required": "Enter a reason for approving"},
    )
    proviso = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7, "class": "govuk-!-margin-top-4"}),
        label="",
        required=False,
    )
    instructions_to_exporter = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "3"}),
        label="Add any instructions for the exporter (optional)",
        help_text="These may be added to the licence cover letter, subject to review by the Licensing Unit.",
        required=False,
    )

    footnote_details_radios = forms.ChoiceField(
        label="Add a reporting footnote (optional)",
        required=False,
        widget=forms.RadioSelect,
        choices=(),
    )
    footnote_details = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "govuk-!-margin-top-4"}),
        label="",
        required=False,
    )

    approval_radios = forms.ChoiceField(
        label="What is your reason for approving?",
        required=False,
        widget=forms.RadioSelect,
        choices=(),
    )
    proviso_radios = forms.ChoiceField(
        label="Add a licence condition (optional)",
        required=False,
        widget=forms.RadioSelect,
        choices=(),
    )

    def __init__(self, *args, **kwargs):
        approval_reason = kwargs.pop("approval_reason")
        proviso = kwargs.pop("proviso")
        footnote_details = kwargs.pop("footnote_details")
        super().__init__(*args, **kwargs)
        # this follows the same pattern as denial_reasons.
        approval_choices, approval_text = self._picklist_to_choices(approval_reason)
        self.approval_text = approval_text

        proviso_choices, proviso_text = self._picklist_to_choices(proviso)
        self.proviso_text = proviso_text

        footnote_details_choices, footnote_text = self._picklist_to_choices(footnote_details)
        self.footnote_text = footnote_text

        self.fields["approval_radios"].choices = approval_choices
        self.fields["proviso_radios"].choices = proviso_choices
        self.fields["footnote_details_radios"].choices = footnote_details_choices

        self.helper = FormHelper()
        self.helper.layout = Layout(
            RadioTextArea("approval_radios", "approval_reasons", self.approval_text),
            ExpandingFieldset(
                RadioTextArea("proviso_radios", "proviso", self.proviso_text),
                "instructions_to_exporter",
                RadioTextArea("footnote_details_radios", "footnote_details", self.footnote_text),
                legend="Add a licence condition, instruction to exporter or footnote",
                summary_css_class="supplemental-approval-fields",
            ),
            Submit("submit", "Submit recommendation"),
        )


class ConsolidateApprovalForm(GiveApprovalAdviceForm):
    """Approval form minus some fields."""

    def __init__(self, team_alias, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            RadioTextArea("approval_radios", "approval_reasons", self.approval_text),
            RadioTextArea("proviso_radios", "proviso", self.proviso_text),
            Submit("submit", "Submit recommendation"),
        )


class RefusalAdviceForm(PicklistAdviceForm):
    denial_reasons = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(),
        label="What is the refusal criteria?",
        help_text=format_html(
            f'Select all <a class="govuk-link" '
            f'href="https://questions-statements.parliament.uk/written-statements/detail/2021-12-08/hcws449" '
            f'target="_blank">refusal criteria (opens in a new tab)</a> that apply'
        ),
        error_messages={"required": "Select at least one refusal criteria"},
    )
    refusal_reasons_radios = forms.ChoiceField(
        label="What are your reasons for this refusal?",
        widget=forms.RadioSelect,
        required=False,
        choices=(),
    )
    refusal_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7, "class": "govuk-!-margin-top-4"}),
        label="",
        error_messages={"required": "Enter a reason for refusing"},
    )

    def __init__(self, choices, *args, **kwargs):
        refusal_reasons = kwargs.pop("refusal_reasons")
        super().__init__(*args, **kwargs)
        self.fields["denial_reasons"].choices = choices
        label_size = {"label_size": "govuk-label--s"}

        refusal_reasons_choices, refusal_text = self._picklist_to_choices(refusal_reasons)
        self.refusal_text = refusal_text

        self.fields["refusal_reasons_radios"].choices = refusal_reasons_choices

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("denial_reasons", context=label_size),
            RadioTextArea("refusal_reasons_radios", "refusal_reasons", refusal_text),
            Submit("submit", "Submit recommendation"),
        )


class LUConsolidateRefusalForm(forms.Form):
    refusal_note = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "7"}),
        label="Enter the refusal note as agreed in the refusal meeting",
        error_messages={"required": "Enter the refusal meeting note"},
    )

    denial_reasons = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(),
        label="What is the refusal criteria?",
        help_text=format_html(
            f'Select all <a class="govuk-link" '
            f'href="https://questions-statements.parliament.uk/written-statements/detail/2021-12-08/hcws449" '
            f'target="_blank">refusal criteria (opens in a new tab)</a> that apply'
        ),
        error_messages={"required": "Select at least one refusal criteria"},
    )

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["denial_reasons"].choices = choices
        self.helper = FormHelper()
        self.helper.layout = Layout("denial_reasons", "refusal_note", Submit("submit", "Submit recommendation"))


class DeleteAdviceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("confirm", "Confirm"))


def get_formset(form_class, num=1, data=None, initial=None):
    factory = formset_factory(form_class, extra=num, min_num=num, max_num=num)
    return factory(data=data, initial=initial)


class CountersignAdviceForm(forms.Form):
    DOCUMENT_TITLE = "Review and countersign this case"
    approval_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "10"}),
        label="Explain why you are agreeing with this recommendation",
        error_messages={"required": "Enter why you agree with the recommendation"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout("approval_reasons")


class CountersignDecisionAdviceForm(forms.Form):
    DECISION_CHOICES = [(True, "Yes"), (False, "No")]

    outcome_accepted = forms.TypedChoiceField(
        choices=DECISION_CHOICES,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        label="Do you agree with this recommendation?",
        error_messages={"required": "Select yes if you agree with the recommendation"},
    )
    approval_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "10"}),
        label="Explain your reasons",
        required=False,
    )
    rejected_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "10"}),
        label="Message to the case officer (explaining why the case is being returned)",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            ConditionalRadios(
                "outcome_accepted",
                ConditionalRadiosQuestion("Yes", Field("approval_reasons")),
                ConditionalRadiosQuestion("No", Field("rejected_reasons")),
            ),
        )

    def clean_approval_reasons(self):
        outcome_accepted = self.cleaned_data.get("outcome_accepted")
        approval_reasons = self.cleaned_data.get("approval_reasons")
        if outcome_accepted and not self.cleaned_data.get("approval_reasons"):
            self.add_error("approval_reasons", "Enter a reason for countersigning")

        return approval_reasons

    def clean_rejected_reasons(self):
        outcome_accepted = self.cleaned_data.get("outcome_accepted")
        rejected_reasons = self.cleaned_data.get("rejected_reasons")
        if outcome_accepted is False and not self.cleaned_data.get("rejected_reasons"):
            self.add_error("rejected_reasons", "Enter a message explaining why the case is being returned")

        return rejected_reasons


class FCDOApprovalAdviceForm(GiveApprovalAdviceForm):
    def __init__(self, countries, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["countries"] = forms.MultipleChoiceField(
            choices=countries.items(),
            widget=GridmultipleSelect(),
            label="Select countries for which you want to give advice",
            error_messages={"required": "Select the destinations you want to make recommendations for"},
        )
        parent_layout = self.helper.layout
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "countries",
            parent_layout,
        )


class FCDORefusalAdviceForm(RefusalAdviceForm):
    def __init__(self, choices, countries, *args, **kwargs):
        super().__init__(choices, *args, **kwargs)
        self.fields["countries"] = forms.MultipleChoiceField(
            choices=countries.items(),
            widget=GridmultipleSelect(),
            label="Select countries for which you want to give advice",
            error_messages={"required": "Select the destinations you want to make recommendations for"},
        )
        self.helper.layout = Layout(
            "countries",
            "denial_reasons",
            RadioTextArea("refusal_reasons_radios", "refusal_reasons", self.refusal_text),
            Submit("submit", "Submit recommendation"),
        )


class MoveCaseForwardForm(forms.Form):
    def __init__(self, move_case_button_label="Move case forward", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(Submit("submit", move_case_button_label, css_id="move-case-forward-button"))


class DESNZTriggerListFormBase(forms.Form):
    TRIGGER_LIST_GUIDELINES_CHOICES = [(True, "Yes"), (False, "No")]
    NCA_CHOICES = [(True, "Yes"), (False, "No")]

    is_trigger_list_guidelines_applicable = forms.TypedChoiceField(
        choices=TRIGGER_LIST_GUIDELINES_CHOICES,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        label="Do the trigger list guidelines apply to this product?",
        help_text="Select no if the product is on the trigger list but falls outside the guidelines",
        error_messages={
            "required": "Select yes if the trigger list guidelines apply to this product",
        },
    )

    is_nca_applicable = forms.TypedChoiceField(
        choices=NCA_CHOICES,
        coerce=coerce_str_to_bool,
        error_messages={
            "required": "Select yes if a Nuclear Cooperation Agreement applies to the product",
        },
        label="Does a Nuclear Cooperation Agreement apply?",
        widget=forms.RadioSelect,
    )

    nsg_assessment_note = forms.CharField(
        label="Add an assessment note (optional)",
        required=False,
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "is_trigger_list_guidelines_applicable",
            "is_nca_applicable",
            "nsg_assessment_note",
            Submit("submit", "Continue"),
        )


class DESNZTriggerListAssessmentForm(DESNZTriggerListFormBase):
    def __init__(
        self,
        request,
        queue_pk,
        goods,
        application_pk,
        is_user_rfd,
        organisation_documents,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.request = request
        self.queue_pk = queue_pk
        self.application_pk = application_pk
        self.is_user_rfd = is_user_rfd
        self.organisation_documents = organisation_documents
        self.fields["goods"] = forms.MultipleChoiceField(
            choices=self.get_goods_choices(goods),
            widget=GoodsMultipleSelect(),
            label=(
                "Select a product to begin. Or you can select multiple products to give them the same assessment.<br><br>"
                "<strong>You will then be asked to make a recommendation for all products on this application.</strong>"
            ),
            error_messages={"required": "Select the products that you want to assess"},
        )

    def get_goods_choices(self, goods):
        return [
            (
                good_on_application_id,
                {
                    "good_on_application": good_on_application,
                    "summary": get_good_on_application_tau_summary(
                        self.request,
                        good_on_application,
                        self.queue_pk,
                        self.application_pk,
                        self.is_user_rfd,
                        self.organisation_documents,
                    ),
                },
            )
            for good_on_application_id, good_on_application in goods.items()
        ]


class DESNZTriggerListAssessmentEditForm(DESNZTriggerListFormBase):
    def __init__(
        self,
        request,
        queue_pk,
        application_pk,
        is_user_rfd,
        organisation_documents,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.request = request
        self.queue_pk = queue_pk
        self.application_pk = application_pk
        self.is_user_rfd = is_user_rfd
        self.organisation_documents = organisation_documents


class DESNZRecommendAnApproval(PicklistAdviceForm, BaseForm):
    DOCUMENT_TITLE = "Recommend approval for this case"

    class Layout:
        TITLE = "Recommend an approval"

    approval_reasons = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7, "class": "govuk-!-margin-top-4"}),
        label="",
        error_messages={"required": "Enter a reason for approving"},
    )
    approval_radios = forms.ChoiceField(
        label="What is your reason for approving?",
        required=False,
        widget=forms.RadioSelect,
        choices=(),
    )
    add_licence_conditions = forms.BooleanField(
        label="Add licence conditions, instructions to exporter or footnotes (optional)",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.pop("proviso")
        kwargs.pop("footnote_details")
        approval_reason = kwargs.pop("approval_reason")
        # this follows the same pattern as denial_reasons.
        approval_choices, approval_text = self._picklist_to_choices(approval_reason)
        self.approval_text = approval_text
        super().__init__(*args, **kwargs)

        self.fields["approval_radios"].choices = approval_choices

    def get_layout_fields(self):
        return (
            RadioTextArea("approval_radios", "approval_reasons", self.approval_text),
            "add_licence_conditions",
        )


class PicklistApprovalAdviceFormEdit(BaseForm):
    DOCUMENT_TITLE = "Recommend approval for this case"

    class Layout:
        TITLE = "Add licence conditions, instructions to exporter or footnotes (optional)"

    DOCUMENT_TITLE = "Recommend approval for this case"
    proviso = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 30, "class": "govuk-!-margin-top-4"}),
        label="",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.pop("approval_reason")
        kwargs.pop("proviso")
        kwargs.pop("footnote_details")
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return ("proviso",)


class PicklistApprovalAdviceForm(PicklistAdviceForm, BaseForm):
    DOCUMENT_TITLE = "Recommend approval for this case"

    class Layout:
        TITLE = "Add licence conditions, instructions to exporter or footnotes (optional)"

    DOCUMENT_TITLE = "Recommend approval for this case"
    proviso = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7, "class": "govuk-!-margin-top-4"}),
        label="",
        required=False,
    )

    approval_radios = forms.ChoiceField(
        label="What is your reason for approving?",
        required=False,
        widget=forms.RadioSelect,
        choices=(),
    )
    proviso_radios = forms.MultipleChoiceField(
        label="Add a licence condition (optional)",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=(),
    )

    def clean(self):
        cleaned_data = super().clean()
        # only return proviso (text) for selected radios, nothing else matters, join by 2 newlines
        return {"proviso": "\r\n\r\n".join([cleaned_data[selected] for selected in cleaned_data["proviso_radios"]])}

    def __init__(self, *args, **kwargs):
        kwargs.pop("approval_reason")
        kwargs.pop("footnote_details")
        proviso = kwargs.pop("proviso")

        proviso_choices, proviso_text = self._picklist_to_choices(proviso)
        self.proviso_text = proviso_text

        self.conditional_checkbox_choices = (
            ConditionalCheckboxesQuestion(choices.label, choices.value) for choices in proviso_choices
        )

        super().__init__(*args, **kwargs)

        self.fields["proviso_radios"].choices = proviso_choices
        for choices in proviso_choices:
            self.fields[choices.value] = forms.CharField(
                widget=forms.Textarea(attrs={"rows": 3, "class": "govuk-!-margin-top-4"}),
                label="Description",
                required=False,
                initial=proviso_text[choices.value],
            )

    def get_layout_fields(self):

        return (ConditionalCheckboxes("proviso_radios", *self.conditional_checkbox_choices),)


class FootnotesApprovalAdviceForm(PicklistAdviceForm, BaseForm):

    DOCUMENT_TITLE = "Recommend approval for this case"

    class Layout:
        TITLE = "Instructions for the exporter (optional)"

    instructions_to_exporter = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "3"}),
        label="Add any instructions for the exporter (optional)",
        help_text="These may be added to the licence cover letter, subject to review by the Licensing Unit.",
        required=False,
    )

    footnote_details_radios = forms.ChoiceField(
        label="Add a reporting footnote (optional)",
        required=False,
        widget=forms.RadioSelect,
        choices=(),
    )
    footnote_details = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "govuk-!-margin-top-4"}),
        label="",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.pop("approval_reason")
        kwargs.pop("proviso")
        footnote_details = kwargs.pop("footnote_details")
        footnote_details_choices, footnote_text = self._picklist_to_choices(footnote_details)
        self.footnote_text = footnote_text

        super().__init__(*args, **kwargs)

        self.fields["footnote_details_radios"].choices = footnote_details_choices

    def get_layout_fields(self):
        return (
            "instructions_to_exporter",
            RadioTextArea("footnote_details_radios", "footnote_details", self.footnote_text),
        )
