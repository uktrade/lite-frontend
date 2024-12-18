from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit

from core.forms.utils import coerce_str_to_bool
from caseworker.tau.summaries import get_good_on_application_tau_summary
from caseworker.tau.widgets import GoodsMultipleSelect


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
