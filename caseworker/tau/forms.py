from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit

from caseworker.cases.helpers.summaries import get_good_on_application_summary
from caseworker.tau.widgets import GoodsMultipleSelect


class TAUEditForm(forms.Form):
    """
    This is for editing product assessment.
    """

    MESSAGE_NO_CLC_MUTEX = "This is mutually exclusive with control list entries"
    MESSAGE_NO_CLC_REQUIRED = "Select a control list entry or select 'This product does not have a control list entry'"

    control_list_entries = forms.MultipleChoiceField(
        label="",
        choices=[],  # set in __init__
        required=False,
        # setting id for javascript to use
        widget=forms.SelectMultiple(attrs={"id": "control_list_entries"}),
    )

    does_not_have_control_list_entries = forms.BooleanField(
        label="Select that this product is not on the control list",
        required=False,
    )
    report_summary = forms.CharField(
        label="Add a report summary",
        help_text="Type for suggestions",
        # setting id for javascript to use
        widget=forms.TextInput(attrs={"id": "report_summary"}),
        required=False,
    )

    is_wassenaar = forms.BooleanField(
        label="This product falls under the WASSENAAR regime",
        required=False,
    )

    comment = forms.CharField(
        label="Add an assessment note (optional)",
        required=False,
        widget=forms.Textarea,
    )

    def __init__(self, control_list_entries_choices, document=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = document
        self.fields["control_list_entries"].choices = control_list_entries_choices
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "control_list_entries",
            "does_not_have_control_list_entries",
            "is_wassenaar",
            "report_summary",
            "comment",
            Submit("submit", "Submit"),
        )

    def clean(self):
        cleaned_data = super().clean()
        has_none = cleaned_data["does_not_have_control_list_entries"]
        has_some = bool(cleaned_data.get("control_list_entries"))
        if has_none and has_some:
            raise forms.ValidationError({"does_not_have_control_list_entries": self.MESSAGE_NO_CLC_MUTEX})
        elif not has_none and not has_some:
            raise forms.ValidationError({"does_not_have_control_list_entries": self.MESSAGE_NO_CLC_REQUIRED})
        # report summary is required when there are CLEs
        no_report_summary = cleaned_data.get("report_summary", "") == ""
        if has_some and no_report_summary:
            raise forms.ValidationError({"report_summary": "This field is required."})
        return cleaned_data


class TAUAssessmentForm(TAUEditForm):
    """
    This is replacing caseworker.cases.forms.review_goods.ExportControlCharacteristicsForm.

    TODO: Delete ExportControlCharacteristicsForm after this goes live.
    """

    MESSAGE_NO_CLC_MUTEX = "This is mutually exclusive with control list entries"
    MESSAGE_NO_CLC_REQUIRED = "Select a control list entry or select 'This product does not have a control list entry'"

    def __init__(
        self,
        request,
        goods,
        control_list_entries_choices,
        queue_pk,
        application_pk,
        is_user_rfd,
        organisation_documents,
        *args,
        **kwargs,
    ):
        super().__init__(control_list_entries_choices, *args, **kwargs)

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

        self.helper.form_tag = False
        self.helper.layout = Layout(
            "goods",
            *self.helper.layout.fields,
        )

    def get_goods_choices(self, goods):
        return [
            (
                good_on_application_id,
                {
                    "good_on_application": good_on_application,
                    "summary": get_good_on_application_summary(
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
