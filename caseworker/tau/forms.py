from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet

from requests.exceptions import HTTPError

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import (
    HTML,
    Layout,
)

from core.forms.layouts import (
    ConditionalCheckboxes,
    ConditionalCheckboxesQuestion,
)

from caseworker.regimes.enums import Regimes

from .summaries import get_good_on_application_tau_summary
from .widgets import GoodsMultipleSelect
from ..report_summary.services import get_report_summary_prefix, get_report_summary_subject

REPORT_SUMMARY_SUBJECT_KEY = "report_summary_subject"
REPORT_SUMMARY_PREFIX_KEY = "report_summary_prefix"
MISSING_REPORT_SUMMARY_SUBJECT = "Enter a report summary subject"
INVALID_REPORT_SUMMARY_SUBJECT = "Enter a valid report summary subject"
INVALID_REPORT_SUMMARY_PREFIX = "Enter a valid report summary prefix"


class TAUEditForm(forms.Form):
    """
    This is for editing product assessment.
    """

    MESSAGE_NO_CLC_MUTEX = "This is mutually exclusive with control list entries"
    MESSAGE_NO_CLC_REQUIRED = "Select a control list entry or select 'This product does not have a control list entry'"

    control_list_entries = forms.MultipleChoiceField(
        label="Add a control list entry or end-use control",
        choices=(),  # set in __init__
        required=False,
    )

    does_not_have_control_list_entries = forms.BooleanField(
        label="Select that this product is not on the control list",
        required=False,
    )

    report_summary_prefix = forms.CharField(
        label="Add a prefix for report summary (optional)",
        help_text="For example 'components for'. Type for suggestions.",
        # setting id for javascript to use
        widget=forms.TextInput(attrs={"id": REPORT_SUMMARY_PREFIX_KEY}),
        required=False,
    )

    report_summary_subject = forms.CharField(
        label="Add a subject for the report summary",
        help_text="For example 'sniper rifles'. Type for suggestions.",
        # setting id for javascript to use
        widget=forms.TextInput(attrs={"id": REPORT_SUMMARY_SUBJECT_KEY}),
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
    is_ncsc_military_information_security = forms.BooleanField(
        label="Yes, refer to NCSC for a recommendation",
        help_text="Are there potential cryptography or information security features?",
        required=False,
    )
    comment = forms.CharField(
        label="Add an assessment note (optional)",
        required=False,
        widget=forms.Textarea,
    )

    def __init__(
        self,
        request,
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
        self.request = request
        self.document = document
        self.fields["control_list_entries"].choices = control_list_entries_choices
        self.fields["wassenaar_entries"].choices = wassenaar_entries
        self.fields["mtcr_entries"].choices = mtcr_entries
        self.fields["nsg_entries"].choices = nsg_entries
        self.fields["cwc_entries"].choices = cwc_entries
        self.fields["ag_entries"].choices = ag_entries

        # When we get back the report summary prefix and subject values we get the pks of the objects as this is what
        # is sent through from the form, however we need to pass the name back to the frontend so that the JS component
        # can use this to populate the autocomplete field
        # To handle this we grab the item data from the API using the pk that we have so that we can store the name in
        # a data attribute that the frontend can then present to the user
        report_summary_prefix_value = self.data.get(REPORT_SUMMARY_PREFIX_KEY)
        if report_summary_prefix_value:
            try:
                report_summary_prefix = get_report_summary_prefix(request, report_summary_prefix_value)
            except HTTPError:
                # If we get here then we've ended up with a pk that we can't get any information about so the best
                # we can do is just present a blank name back to the user
                report_summary_prefix_name = ""
            else:
                report_summary_prefix_name = report_summary_prefix["report_summary_prefix"]["name"]
            self.fields[REPORT_SUMMARY_PREFIX_KEY].widget.attrs["data-name"] = report_summary_prefix_name

        report_summary_subject_value = self.data.get(REPORT_SUMMARY_SUBJECT_KEY)
        if report_summary_subject_value:
            try:
                report_summary_subject = get_report_summary_subject(request, report_summary_subject_value)
            except HTTPError:
                # If we get here then we've ended up with a pk that we can't get any information about so the best
                # we can do is just present a blank name back to the user
                report_summary_subject_name = ""
            else:
                report_summary_subject_name = report_summary_subject["report_summary_subject"]["name"]
            self.fields[REPORT_SUMMARY_SUBJECT_KEY].widget.attrs["data-name"] = report_summary_subject_name

        self.helper = FormHelper()
        self.helper.form_tag = False

        fields = [
            "control_list_entries",
            HTML.p("Or"),
            "does_not_have_control_list_entries",
            REPORT_SUMMARY_PREFIX_KEY,
            REPORT_SUMMARY_SUBJECT_KEY,
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
                "None",
            ),
            "is_ncsc_military_information_security",
            "comment",
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

        # We pass in has_no_cle_entries here because throwing the errors above will clear out the value from
        # cleaned_data so if we try to get it in the below method we won't have the original value which we want to be
        # able to set the right validation for the report summary subject
        self.validate_report_summary_subject(cleaned_data, not has_no_cle_entries)
        self.validate_report_summary_prefix(cleaned_data)

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

    def validate_report_summary_subject(self, cleaned_data, has_cle_entries):
        subject_id = cleaned_data.get(REPORT_SUMMARY_SUBJECT_KEY)
        subject_name_as_typed = self.data.get("_report_summary_subject")

        if has_cle_entries and not subject_id:
            self.add_error(REPORT_SUMMARY_SUBJECT_KEY, MISSING_REPORT_SUMMARY_SUBJECT)
            return

        if not subject_id:
            if subject_name_as_typed:
                self.add_error(REPORT_SUMMARY_SUBJECT_KEY, INVALID_REPORT_SUMMARY_SUBJECT)
            return

        try:
            actual_name = get_report_summary_subject(self.request, subject_id)[REPORT_SUMMARY_SUBJECT_KEY]["name"]
            if "_report_summary_subject" in self.data and subject_name_as_typed != actual_name:
                self.add_error(REPORT_SUMMARY_SUBJECT_KEY, INVALID_REPORT_SUMMARY_SUBJECT)
        except HTTPError:
            self.add_error(REPORT_SUMMARY_SUBJECT_KEY, INVALID_REPORT_SUMMARY_SUBJECT)

    def validate_report_summary_prefix(self, cleaned_data):
        prefix_id = cleaned_data.get(REPORT_SUMMARY_PREFIX_KEY)
        prefix_name_as_typed = self.data.get("_report_summary_prefix")

        if not prefix_id:
            if prefix_name_as_typed:
                self.add_error(REPORT_SUMMARY_PREFIX_KEY, INVALID_REPORT_SUMMARY_PREFIX)
            return

        try:
            actual_name = get_report_summary_prefix(self.request, prefix_id)[REPORT_SUMMARY_PREFIX_KEY]["name"]
            if "_report_summary_prefix" in self.data:
                if prefix_name_as_typed != actual_name:
                    self.add_error(REPORT_SUMMARY_PREFIX_KEY, INVALID_REPORT_SUMMARY_PREFIX)
        except HTTPError:
            self.add_error(REPORT_SUMMARY_PREFIX_KEY, INVALID_REPORT_SUMMARY_PREFIX)


class TAUAssessmentForm(TAUEditForm):
    """
    This is replacing caseworker.cases.forms.review_goods.ExportControlCharacteristicsForm.

    TODO: Delete ExportControlCharacteristicsForm after this goes live.
    """

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
        super().__init__(request, control_list_entries_choices, wassenaar_entries, mtcr_entries, *args, **kwargs)

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


class TAUPreviousAssessmentForm(forms.Form):
    good_on_application_id = forms.UUIDField(
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, good_on_application, **kwargs):
        super().__init__(*args, **kwargs)
        self.good_on_application = good_on_application

        # Only add the 'use_latest_precedent' field if 'latest_precedent' is present
        if good_on_application.get("latest_precedent"):
            self.fields["use_latest_precedent"] = forms.BooleanField(
                initial=True,
                label="",
                required=False,
                widget=forms.CheckboxInput(attrs={"class": "previous-assessment-checkbox-cell"}),
            )
            self.fields["latest_precedent_id"] = forms.UUIDField(
                widget=forms.HiddenInput(),
            )

            latest_precedent = good_on_application.get("latest_precedent", {})
            if latest_precedent:
                self.fields["comment"] = forms.CharField(
                    widget=forms.Textarea(attrs={"rows": 7}),
                    required=False,
                    label="",
                    initial=latest_precedent.get("comment", ""),
                )


class BaseTAUPreviousAssessmentFormSet(BaseFormSet):
    def __init__(self, *args, goods_on_applications, **kwargs):
        super().__init__(*args, **kwargs)
        self.goods_on_applications = goods_on_applications

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["good_on_application"] = self.goods_on_applications[index]
        return kwargs

    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            if "use_latest_precedent" not in form.fields:
                continue

            if form.cleaned_data["use_latest_precedent"] and form.good_on_application["latest_precedent"]["id"] != str(
                form.cleaned_data["latest_precedent_id"]
            ):
                # Error out if the latest precedent ID that we have does not match the one
                # submitted in the form; we do not want to assess a product with values that
                # a caseworker has not verified themselves.
                raise ValidationError("A new assessment was made which supersedes your chosen previous assessment.")


class TAUEditAssessmentChoiceForm(forms.Form):
    good_on_application_id = forms.UUIDField(
        widget=forms.HiddenInput(),
    )
    selected = forms.BooleanField(
        required=False,
        initial=True,
    )

    def __init__(self, *args, good_on_application, **kwargs):
        super().__init__(*args, **kwargs)
        self.good_on_application = good_on_application


class TAUEditAssessmentChoiceFormSet(BaseFormSet):
    def __init__(self, *args, goods_on_applications, **kwargs):
        super().__init__(*args, **kwargs)
        self.goods_on_applications = goods_on_applications

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["good_on_application"] = self.goods_on_applications[index]
        return kwargs


class CachedSelectMultiple(forms.SelectMultiple):
    """
    A SelectMultiple widget that takes advantage of django template fragment
    caching to avoid re-rendering the same options blocks over and over.

    The fragment cache within the template is keyed by widget class name AND
    selected values; such that the rendering of options choices for a particular
    multiselect with a particular choice of values is not rendered more than once.
    """

    template_name = "widgets/select_multiple_cached.html"


class TAUMultipleEditForm(forms.Form):
    id = forms.UUIDField(
        widget=forms.HiddenInput(),
    )
    licence_required = forms.BooleanField(
        label="",
        required=False,
    )
    refer_to_ncsc = forms.BooleanField(
        label="",
        required=False,
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 7}),
        required=False,
        label="",
    )
    control_list_entries = forms.MultipleChoiceField(
        label="",
        choices=(),  # set in __init__
        required=False,
        # setting class for javascript to use
        widget=CachedSelectMultiple(attrs={"class": "control-list-entries"}),
    )
    report_summary_prefix = forms.CharField(
        label="",
        # setting class for javascript to use
        widget=forms.TextInput(attrs={"class": "report-summary-prefix"}),
        required=False,
    )
    report_summary_subject = forms.CharField(
        label="",
        # setting class for javascript to use
        widget=forms.TextInput(attrs={"class": "report-summary-subject"}),
        required=False,
    )
    regimes = forms.MultipleChoiceField(
        label="",
        choices=(),  # set in __init__
        required=False,
        # setting class for javascript to use
        widget=CachedSelectMultiple(attrs={"class": "regime-entries"}),
    )

    def __init__(self, *args, control_list_entries_choices, regime_choices, good_on_application, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["control_list_entries"].choices = control_list_entries_choices
        self.fields["regimes"].choices = regime_choices
        self.good_on_application = good_on_application
        if self.initial.get("report_summary_prefix_name"):
            self.fields["report_summary_prefix"].widget.attrs["data-name"] = self.initial["report_summary_prefix_name"]
        if self.initial.get("report_summary_subject_name"):
            self.fields["report_summary_subject"].widget.attrs["data-name"] = self.initial[
                "report_summary_subject_name"
            ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("licence_required"):
            if not cleaned_data.get("control_list_entries"):
                self.add_error("control_list_entries", "Enter a control list entry or unselect 'Licence required'")
            if not cleaned_data.get("report_summary_subject"):
                self.add_error("report_summary_subject", "Enter a report summary or unselect 'Licence required'")
        if not cleaned_data.get("licence_required") and cleaned_data.get("control_list_entries"):
            self.add_error("control_list_entries", "Remove control list entries or select 'Licence required'")


class TAUMultipleEditFormSet(BaseFormSet):
    def __init__(self, *args, goods_on_applications, **kwargs):
        super().__init__(*args, **kwargs)
        self.goods_on_applications = goods_on_applications

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["good_on_application"] = self.goods_on_applications[index]
        return kwargs
