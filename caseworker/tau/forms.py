from django import forms
from django.conf import settings

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import (
    HTML,
    Layout,
    Submit,
)

from core.forms.layouts import (
    ConditionalCheckboxes,
    ConditionalCheckboxesQuestion,
)

from caseworker.regimes.enums import Regimes

from .summaries import get_good_on_application_tau_summary
from .widgets import GoodsMultipleSelect


class TAUEditForm(forms.Form):
    """
    This is for editing product assessment.
    """

    MESSAGE_NO_CLC_MUTEX = "This is mutually exclusive with control list entries"
    MESSAGE_NO_CLC_REQUIRED = "Select a control list entry or select 'This product does not have a control list entry'"

    SUBMIT_BUTTON_TEXT = "Submit"

    control_list_entries = forms.MultipleChoiceField(
        label="Add a control list entry or end-use control",
        help_text="Or type for suggestions",
        choices=(),  # set in __init__
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

    report_summary_prefix = forms.CharField(
        label="Add a report summary prefix",
        help_text="Type for suggestions",
        # setting id for javascript to use
        widget=forms.TextInput(attrs={"id": "report_summary_prefix"}),
        required=False,
    )

    regimes = forms.MultipleChoiceField(
        label="Add regimes",
        choices=(
            (Regimes.WASSENAAR.value, "Wassenaar Arrangement"),
            (Regimes.MTCR.value, "Missile Technology Control Regime"),
            (Regimes.NSG.value, "Nuclear Suppliers Group"),
            (Regimes.CWC.value, "Chemical Weapons Convention"),
            (Regimes.AG.value, "Australia Group"),
            ("NONE", "None"),
        ),
        error_messages={
            "required": "Add a regime, or select none",
        },
        widget=forms.CheckboxSelectMultiple,
    )

    wassenaar_entries = forms.ChoiceField(
        label="Choose the highest applicable sensitivity level",
        choices=(),  # set in __init__
        required=False,
        widget=forms.RadioSelect,
    )

    mtcr_entries = forms.MultipleChoiceField(
        label="What is the entry (for example M1A2)? Type for suggestions",
        choices=(),  # set in __init__
        required=False,
        # setting id for javascript to use
        widget=forms.SelectMultiple(
            attrs={
                "id": "mtcr_entries",
                "data-module": "regimes-multi-select",
            }
        ),
    )

    nsg_entries = forms.MultipleChoiceField(
        label="What is the entry (for example M1A2)? Type for suggestions",
        choices=(),  # set in __init__
        required=False,
        # setting id for javascript to use
        widget=forms.SelectMultiple(
            attrs={
                "id": "nsg_entries",
                "data-module": "regimes-multi-select",
            }
        ),
    )

    cwc_entries = forms.ChoiceField(
        label="",
        choices=(),  # set in __init__
        required=False,
        widget=forms.RadioSelect,
    )

    ag_entries = forms.ChoiceField(
        label="",
        choices=(),  # set in __init__
        required=False,
        widget=forms.RadioSelect,
    )

    comment = forms.CharField(
        label="Add an assessment note (optional)",
        required=False,
        widget=forms.Textarea,
    )

    def __init__(
        self,
        control_list_entries_choices,
        wassenaar_entries,
        mtcr_entries,
        nsg_entries,
        cwc_entries,
        ag_entries,
        document=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.document = document
        self.fields["control_list_entries"].choices = control_list_entries_choices
        self.fields["wassenaar_entries"].choices = wassenaar_entries
        self.fields["mtcr_entries"].choices = mtcr_entries
        self.fields["nsg_entries"].choices = nsg_entries
        self.fields["cwc_entries"].choices = cwc_entries
        self.fields["ag_entries"].choices = ag_entries

        self.helper = FormHelper()

        feature_flagged_regimes = []
        if settings.FEATURE_C6_REGIMES:
            feature_flagged_regimes = [
                ConditionalCheckboxesQuestion(
                    "Chemical Weapons Convention",
                    "cwc_entries",
                ),
                ConditionalCheckboxesQuestion(
                    "Nuclear Suppliers Group",
                    "nsg_entries",
                ),
                ConditionalCheckboxesQuestion(
                    "Australia Group",
                    "ag_entries",
                ),
            ]

        fields = [
            "control_list_entries",
            HTML.p("Or"),
            "does_not_have_control_list_entries",
            "report_summary",
            "report_summary_prefix",
            ConditionalCheckboxes(
                "regimes",
                ConditionalCheckboxesQuestion(
                    "Wassenaar Arrangement",
                    "wassenaar_entries",
                ),
                ConditionalCheckboxesQuestion(
                    "Missile Technology Control Regime",
                    "mtcr_entries",
                ),
                *feature_flagged_regimes,
                "None",
            ),
            "comment",
            Submit("submit", self.SUBMIT_BUTTON_TEXT),
        ]
        self.helper.layout = Layout(*fields)

    def validate_single_regime_choice(self, cleaned_data, selected_regimes, regime, field_name, error_message):
        is_regime_selected = regime in selected_regimes
        regime_entries = cleaned_data.get(field_name)
        if is_regime_selected and not regime_entries:
            self.add_error(field_name, error_message)

    def validate_multi_regime_choices(self, cleaned_data, selected_regimes, regime, field_name, error_message):
        is_regime_selected = regime in selected_regimes
        regime_entries = cleaned_data.get(field_name, [])
        if is_regime_selected and not regime_entries:
            self.add_error(field_name, error_message)

    def clean(self):
        cleaned_data = super().clean()

        has_no_cle_entries = cleaned_data["does_not_have_control_list_entries"]
        has_some_cle_entries = bool(cleaned_data.get("control_list_entries"))
        if has_no_cle_entries and has_some_cle_entries:
            self.add_error("does_not_have_control_list_entries", self.MESSAGE_NO_CLC_MUTEX)
        elif not has_no_cle_entries and not has_some_cle_entries:
            self.add_error("does_not_have_control_list_entries", self.MESSAGE_NO_CLC_REQUIRED)
        # report summary is required when there are CLEs
        no_report_summary = cleaned_data.get("report_summary", "") == ""
        if has_some_cle_entries and no_report_summary:
            self.add_error("report_summary", "This field is required")

        regimes = cleaned_data.get("regimes", [])

        has_selected_none = "NONE" in regimes
        only_selected_none = regimes == ["NONE"]
        if has_selected_none and not only_selected_none:
            self.add_error("regimes", "Add a regime, or select none")
        else:
            self.validate_single_regime_choice(
                cleaned_data,
                regimes,
                Regimes.WASSENAAR,
                "wassenaar_entries",
                "Select a Wassenaar Arrangement subsection",
            )
            self.validate_single_regime_choice(
                cleaned_data,
                regimes,
                Regimes.CWC,
                "cwc_entries",
                "Select a Chemical Weapons Convention subsection",
            )
            self.validate_single_regime_choice(
                cleaned_data,
                regimes,
                Regimes.AG,
                "ag_entries",
                "Select an Australia Group subsection",
            )
            self.validate_multi_regime_choices(
                cleaned_data,
                regimes,
                Regimes.MTCR,
                "mtcr_entries",
                "Type an entry for the Missile Technology Control Regime",
            )
            self.validate_multi_regime_choices(
                cleaned_data,
                regimes,
                Regimes.NSG,
                "nsg_entries",
                "Type an entry for the Nuclear Suppliers Group Regime",
            )

        return cleaned_data


class TAUAssessmentForm(TAUEditForm):
    """
    This is replacing caseworker.cases.forms.review_goods.ExportControlCharacteristicsForm.

    TODO: Delete ExportControlCharacteristicsForm after this goes live.
    """

    SUBMIT_BUTTON_TEXT = "Save and continue"

    def __init__(
        self,
        request,
        goods,
        control_list_entries_choices,
        wassenaar_entries,
        mtcr_entries,
        queue_pk,
        application_pk,
        is_user_rfd,
        organisation_documents,
        *args,
        **kwargs,
    ):
        super().__init__(control_list_entries_choices, wassenaar_entries, mtcr_entries, *args, **kwargs)

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
