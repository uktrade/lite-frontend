from collections import defaultdict

from django import forms
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from django.utils.html import format_html

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit, HTML

from core.forms.widgets import GridmultipleSelect


def get_approval_advice_form_factory(advice, data=None):
    data = data or {
        "proviso": advice["proviso"],
        "approval_reasons": advice["text"],
        "instructions_to_exporter": advice["note"],
        "footnote_details": advice["footnote"],
    }
    return GiveApprovalAdviceForm(data=data)


def get_refusal_advice_form_factory(advice, denial_reasons_choices, data=None):
    data = data or {
        "refusal_reasons": advice["text"],
        "denial_reasons": [r for r in advice["denial_reasons"]],
    }
    return RefusalAdviceForm(data=data, denial_reasons=denial_reasons_choices)


class PicklistCharField(forms.CharField):
    def get_help_link(self, picklist_attrs, help_text):
        picklist_tags = f'picklist_type="{picklist_attrs.get("type")}" picklist_name="{picklist_attrs.get("name")}" target="{picklist_attrs.get("target")}"'
        return f'<a class="govuk-link govuk-link--no-visited-state" href="#" {picklist_tags}>{help_text}</a>'

    def __init__(self, picklist_attrs, label, help_text, **kwargs):
        min_rows = kwargs.pop("min_rows", 10)
        help_link = self.get_help_link(picklist_attrs, help_text)
        widget = forms.Textarea(attrs={"rows": str(min_rows), "class": "govuk-!-margin-top-4"})
        super().__init__(label=label, help_text=help_link, widget=widget, **kwargs)


class SelectAdviceForm(forms.Form):

    CHOICES = [("approve_all", "Approve all"), ("refuse_all", "Refuse all")]

    recommendation = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Continue"))


class ConsolidateSelectAdviceForm(SelectAdviceForm):
    CHOICES = [("approve", "Approve"), ("refuse", "Refuse")]
    recommendation = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="")


class GiveApprovalAdviceForm(forms.Form):

    approval_reasons = PicklistCharField(
        picklist_attrs={"target": "approval_reasons", "type": "standard_advice", "name": "Standard Advice"},
        label="What are your reasons for approving?",
        help_text="Choose an approval reason from the template list",
        error_messages={"required": "Enter a reason for approving"},
    )
    proviso = PicklistCharField(
        picklist_attrs={"target": "proviso", "type": "proviso", "name": "Provisos"},
        label="Add a licence condition (optional)",
        help_text="Choose a licence condition from the template list",
        required=False,
    )
    instructions_to_exporter = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "10"}),
        label="Add any instructions for the exporter (optional)",
        help_text="These may be added to licence cover letter, subject to review by Licencing Unit.",
        required=False,
    )
    footnote_details = PicklistCharField(
        picklist_attrs={"target": "footnote_details", "type": "footnotes", "name": "Footnotes"},
        label="Add a reporting footnote (optional)",
        help_text="Choose a reporting footnote from the template list",
        min_rows=5,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "approval_reasons",
            "proviso",
            "instructions_to_exporter",
            "footnote_details",
            HTML.details(
                "What is a footnote?",
                "Footnotes explain why products to a destination have been approved or refused. "
                "They will be publicly available in reports and data tables.",
            ),
            Submit("submit", "Submit"),
        )


class ConsolidateApprovalForm(GiveApprovalAdviceForm):
    """Approval form minus some fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout("approval_reasons", "proviso", Submit("submit", "Submit"))


class RefusalAdviceForm(forms.Form):
    def _group_denial_reasons(self, denial_reasons):
        grouped = defaultdict(list)
        for item in denial_reasons:
            grouped[item["id"][0]].append((item["id"], item["id"]))
        return grouped.items()

    def __init__(self, denial_reasons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        refusal_criteria_link = (
            "https://publications.parliament.uk/pa/cm201314/cmhansrd/cm140325/wmstext/140325m0001.htm#14032566000018"
        )
        choices = self._group_denial_reasons(denial_reasons)
        self.fields["denial_reasons"] = forms.MultipleChoiceField(
            choices=choices,
            widget=GridmultipleSelect(),
            label=format_html(
                f'Select all <a href={refusal_criteria_link} target="_blank">refusal criteria (opens in new tab)</a> that apply'
            ),
            error_messages={"required": "Select at least one refusal criteria"},
        )
        self.fields["refusal_reasons"] = PicklistCharField(
            picklist_attrs={"target": "refusal_reasons", "type": "standard_advice", "name": "Standard Advice"},
            label="What are your reasons for this refusal?",
            help_text="Choose a refusal reason from the template list",
            error_messages={"required": "Enter a reason for refusing"},
        )
        self.helper = FormHelper()
        self.helper.layout = Layout("denial_reasons", "refusal_reasons", Submit("submit", "Submit"))


class DeleteAdviceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("confirm", "Confirm"))


class QueueFormset(BaseFormSet):
    """We have a few views that render a list of user-advice with formsets.
    Each form in the formset renders a `ChoiceField` of queues that are
    accessble to the user.
    This class implements the functionality of passing the right list of
    queues through to the respective forms via the kwargs.
    """

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["queues"] = [("", "")] + kwargs["queues"][index]
        return kwargs


def get_queue_formset(form_class, queues, data=None):
    """This is a helper function for rendering QueueFormsets
    """
    num = len(queues)
    factory = formset_factory(form_class, formset=QueueFormset, extra=num, min_num=num, max_num=num)
    return factory(data=data, form_kwargs={"queues": queues})


class CountersignAdviceForm(forms.Form):
    CHOICES = [("yes", "Yes"), ("no", "No")]

    agree_with_recommendation = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select yes if you agree with the recommendation"},
    )
    approval_reasons = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": "10"}), label="Explain your reasons",
    )
    refusal_reasons = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": "10"}),
        label="Explain why this recommendation needs to be sent back to an adviser",
    )

    conditional_radio = {"yes": ["approval_reasons"], "no": ["refusal_reasons", "queue_to_return"]}

    def __init__(self, queues, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields["queue_to_return"] = forms.ChoiceField(
            required=False, label="Choose where to return this recommendation", choices=queues
        )

    def clean(self):
        cleaned_data = super().clean()
        option_selected = cleaned_data.get("agree_with_recommendation")
        if option_selected == "yes" and cleaned_data.get("approval_reasons") == "":
            self.add_error("approval_reasons", "Enter your reasons for agreeing with the recommendation")
        if option_selected == "no":
            if cleaned_data.get("refusal_reasons") == "":
                self.add_error("refusal_reasons", "Enter why you do not agree with the recommendation")
            if cleaned_data.get("queue_to_return") == "":
                self.add_error("queue_to_return", "Select where you want to return this recommendation")


class FCDOApprovalAdviceForm(GiveApprovalAdviceForm):
    def __init__(self, countries, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["countries"] = forms.MultipleChoiceField(
            choices=countries.items(),
            widget=GridmultipleSelect(),
            label="Select countries for which you want to give advice",
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "countries",
            "approval_reasons",
            "proviso",
            "instructions_to_exporter",
            "footnote_details",
            HTML.details(
                "What is a footnote?",
                "Footnotes explain why products to a destination have been approved or refused. "
                "They will be publicly available in reports and data tables.",
            ),
            Submit("submit", "Submit"),
        )


class FCDORefusalAdviceForm(RefusalAdviceForm):
    def __init__(self, denial_reasons, countries, *args, **kwargs):
        super().__init__(denial_reasons, *args, **kwargs)
        self.fields["countries"] = forms.MultipleChoiceField(
            choices=countries.items(),
            widget=GridmultipleSelect(),
            label="Select countries for which you want to give advice",
        )
        self.helper.layout = Layout("countries", "denial_reasons", "refusal_reasons", Submit("submit", "Submit"))


class MoveCaseForwardForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(Submit("submit", "Move case forward"))
