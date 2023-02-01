from collections import defaultdict

from django import forms
from django.forms.formsets import formset_factory
from django.utils.html import format_html

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit, HTML

from core.forms.utils import coerce_str_to_bool

from caseworker.advice import services
from caseworker.tau.summaries import get_good_on_application_tau_summary
from caseworker.tau.widgets import GoodsMultipleSelect

from core.forms.widgets import GridmultipleSelect

from .enums import NSGListTypes


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


class GiveApprovalAdviceForm(forms.Form):

    approval_reasons = PicklistCharField(
        picklist_attrs={"target": "approval_reasons", "type": "standard_advice", "name": "standard advice"},
        label="What are your reasons for approving?",
        help_text="Choose an approval reason from the template list",
        error_messages={"required": "Enter a reason for approving"},
    )
    proviso = PicklistCharField(
        picklist_attrs={"target": "proviso", "type": "proviso", "name": "licence condition"},
        label="Add a licence condition (optional)",
        help_text="Choose a licence condition from the template list",
        required=False,
    )
    instructions_to_exporter = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "10"}),
        label="Add any instructions for the exporter (optional)",
        help_text="These may be added to the licence cover letter, subject to review by the Licensing Unit.",
        required=False,
    )
    footnote_details = PicklistCharField(
        picklist_attrs={"target": "footnote_details", "type": "footnotes", "name": "reporting footnote"},
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
            Submit("submit", "Submit recommendation"),
        )


class ConsolidateApprovalForm(GiveApprovalAdviceForm):
    """Approval form minus some fields."""

    ALIAS_LABELS = {
        services.MOD_ECJU_TEAM: "Enter MOD’s overall reason for approval",
        services.LICENSING_UNIT_TEAM: "Enter Licensing Unit’s reason for approval",
    }

    def __init__(self, team_alias, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if team_alias in self.ALIAS_LABELS:
            self.fields["approval_reasons"].label = self.ALIAS_LABELS[team_alias]

        self.helper = FormHelper()
        self.helper.layout = Layout("approval_reasons", "proviso", Submit("submit", "Submit recommendation"))


class RefusalAdviceForm(forms.Form):
    def _group_denial_reasons(self, denial_reasons):
        grouped = defaultdict(list)
        for item in denial_reasons:
            # skip the ones that are not active anymore
            if item["deprecated"]:
                continue
            grouped[item["id"][0]].append((item["id"], item.get("display_value") or item["id"]))
        return grouped.items()

    def __init__(self, denial_reasons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        refusal_criteria_link = (
            "https://questions-statements.parliament.uk/written-statements/detail/2021-12-08/hcws449"
        )
        choices = self._group_denial_reasons(denial_reasons)
        self.fields["denial_reasons"] = forms.MultipleChoiceField(
            choices=choices,
            widget=GridmultipleSelect(),
            label=format_html(
                f'Select all <a class="govuk-link" href={refusal_criteria_link} target="_blank">refusal criteria (opens in a new tab)</a> that apply'
            ),
            error_messages={"required": "Select at least one refusal criteria"},
        )
        self.fields["refusal_reasons"] = PicklistCharField(
            picklist_attrs={"target": "refusal_reasons", "type": "standard_advice", "name": "standard advice"},
            label="What are your reasons for this refusal?",
            help_text="Choose a refusal reason from the template list",
            error_messages={"required": "Enter a reason for refusing"},
        )
        self.helper = FormHelper()
        self.helper.layout = Layout("denial_reasons", "refusal_reasons", Submit("submit", "Submit recommendation"))


class DeleteAdviceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("confirm", "Confirm"))


def get_formset(form_class, num=1, data=None, initial=None):
    factory = formset_factory(form_class, extra=num, min_num=num, max_num=num)
    return factory(data=data, initial=initial)


class CountersignAdviceForm(forms.Form):
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


class FCDOApprovalAdviceForm(GiveApprovalAdviceForm):
    def __init__(self, countries, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["countries"] = forms.MultipleChoiceField(
            choices=countries.items(),
            widget=GridmultipleSelect(),
            label="Select countries for which you want to give advice",
            error_messages={"required": "Select the destinations you want to make recommendations for"},
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
            Submit("submit", "Submit recommendation"),
        )


class FCDORefusalAdviceForm(RefusalAdviceForm):
    def __init__(self, denial_reasons, countries, *args, **kwargs):
        super().__init__(denial_reasons, *args, **kwargs)
        self.fields["countries"] = forms.MultipleChoiceField(
            choices=countries.items(),
            widget=GridmultipleSelect(),
            label="Select countries for which you want to give advice",
            error_messages={"required": "Select the destinations you want to make recommendations for"},
        )
        self.helper.layout = Layout(
            "countries", "denial_reasons", "refusal_reasons", Submit("submit", "Submit recommendation")
        )


class MoveCaseForwardForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(Submit("submit", "Move case forward"))


class BEISTriggerListFormBase(forms.Form):
    NSG_LIST_TYPE_CHOICES = [
        (NSGListTypes.TRIGGER_LIST.value, "Trigger list"),
        (NSGListTypes.DUAL_USE.value, "Dual use"),
    ]
    NCA_CHOICES = [(True, "Yes"), (False, "No")]

    nsg_list_type = forms.ChoiceField(
        choices=NSG_LIST_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Is the product on the trigger list or dual use?",
        error_messages={
            "required": "Select whether the product/s appear on the trigger list or are for dual use",
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
            "nsg_list_type",
            "is_nca_applicable",
            "nsg_assessment_note",
            Submit("submit", "Continue"),
        )


class BEISTriggerListAssessmentForm(BEISTriggerListFormBase):
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
            label="Select a product to begin. Or you can select multiple products to give them the same assessment.",
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


class BEISTriggerListAssessmentEditForm(BEISTriggerListFormBase):
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
