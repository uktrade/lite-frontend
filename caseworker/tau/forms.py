from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit

from core.constants import ProductCategories

from caseworker.cases.helpers.summaries import (
    material_summary,
    material_product_on_application_summary,
    platform_summary,
    platform_product_on_application_summary,
    software_summary,
    software_product_on_application_summary,
)
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

    def __init__(self, goods, control_list_entries_choices, queue_pk, application_pk, *args, **kwargs):
        super().__init__(control_list_entries_choices, *args, **kwargs)

        self.queue_pk = queue_pk
        self.application_pk = application_pk

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

    def get_good_on_application_summary(self, good_on_application):
        if not good_on_application.get("firearm_details"):
            good = good_on_application.get("good")
            if not good:
                return None

            item_category = good.get("item_category")
            if not item_category:
                return None

            item_category = item_category["key"]
            try:
                _product_summary, _product_on_application_summary = {
                    ProductCategories.PRODUCT_CATEGORY_PLATFORM: (
                        platform_summary,
                        platform_product_on_application_summary,
                    ),
                    ProductCategories.PRODUCT_CATEGORY_MATERIAL: (
                        material_summary,
                        material_product_on_application_summary,
                    ),
                    ProductCategories.PRODUCT_CATEGORY_SOFTWARE: (
                        software_summary,
                        software_product_on_application_summary,
                    ),
                }[item_category]
            except KeyError:
                return None

            product_summary = _product_summary(
                good_on_application["good"],
                self.queue_pk,
                self.application_pk,
            )
            product_on_application_summary = _product_on_application_summary(
                good_on_application,
                self.queue_pk,
                self.application_pk,
            )

            return product_summary + product_on_application_summary

        return None

    def get_goods_choices(self, goods):
        return [
            (
                good_on_application_id,
                {
                    "good_on_application": good_on_application,
                    "summary": self.get_good_on_application_summary(good_on_application),
                },
            )
            for good_on_application_id, good_on_application in goods.items()
        ]
