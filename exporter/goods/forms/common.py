from crispy_forms_gds.layout import HTML

from django import forms
from django.template.loader import render_to_string

from core.forms.layouts import (
    ConditionalQuestion,
    ConditionalRadios,
)
from exporter.core.common.forms import (
    BaseForm,
    coerce_str_to_bool,
)
from exporter.core.services import get_control_list_entries


class ProductNameForm(BaseForm):
    class Layout:
        TITLE = "Give the product a descriptive name"

    name = forms.CharField(
        label="",
        error_messages={
            "required": "Enter a descriptive name",
        },
    )

    def get_layout_fields(self):
        return (
            HTML.p(
                "Try to match the name as closely as possible to any documentation such as the technical "
                "specification, end user certificate or firearm certificate.",
            ),
            "name",
            HTML.details(
                "Help with naming your product",
                render_to_string("goods/forms/common/help_with_naming_your_product.html"),
            ),
        )


class ProductControlListEntryForm(BaseForm):
    class Layout:
        TITLE = "Do you know the product's control list entry?"

    is_good_controlled = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        error_messages={
            "required": "Select yes if you know the product's control list entry",
        },
    )

    control_list_entries = forms.MultipleChoiceField(
        choices=[],  # set in __init__
        label="Enter the control list entry (type to get suggestions)",
        required=False,
        # setting id for javascript to use
        widget=forms.SelectMultiple(attrs={"id": "control_list_entries"}),
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        clc_list = get_control_list_entries(request)
        self.fields["control_list_entries"].choices = [(entry["rating"], entry["rating"]) for entry in clc_list]

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_good_controlled",
                ConditionalQuestion(
                    "Yes",
                    "control_list_entries",
                ),
                ConditionalQuestion(
                    "No",
                    HTML.p(
                        "The product will be assessed and given a control list entry. "
                        "If the product isn't subject to any controls, you'll be issued "
                        "with a 'no licence required' document."
                    ),
                ),
            ),
            HTML.details(
                "Help with control list entries",
                render_to_string("goods/forms/common/help_with_control_list_entries.html"),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        is_good_controlled = cleaned_data.get("is_good_controlled")
        control_list_entries = cleaned_data.get("control_list_entries")

        if is_good_controlled and not control_list_entries:
            self.add_error("control_list_entries", "Enter the control list entry")

        return cleaned_data
