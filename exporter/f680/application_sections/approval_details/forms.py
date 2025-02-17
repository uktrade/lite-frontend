from django import forms
from django.template.loader import render_to_string

from crispy_forms_gds.layout.content import HTML

from core.common.forms import BaseForm
from core.forms.utils import coerce_str_to_bool


class ProductNameForm(BaseForm):
    class Layout:
        TITLE = "Give the item a descriptive name"
        TITLE_AS_LABEL_FOR = "product_name"
        SUBTITLE = render_to_string("f680/forms/subtitle_product_name.html")
        SUBMIT_BUTTON_TEXT = "Save and continue"

    product_name = forms.CharField(
        label=Layout.TITLE,
        help_text="Where possible include the make, model and type of the item",
    )

    def get_layout_fields(self):
        return ("product_name",)


class ProductDescription(BaseForm):
    class Layout:
        TITLE = "Describe the item"
        TITLE_AS_LABEL_FOR = "product_description"
        SUBTITLE = render_to_string("f680/forms/subtitle_product_description.html")
        SUBMIT_BUTTON_TEXT = "Save and continue"

    product_description = forms.CharField(
        label=Layout.TITLE,
        help_text="Where possible include the make, model and type of the item",
    )

    def get_layout_fields(self):
        return (
            "product_description",
            HTML.details(
                "Help with incorporating an item",
                render_to_string("f680/forms/help_product_description.html"),
            ),
        )


class ForeignTechOrSharedInformation(BaseForm):
    class Layout:
        TITLE = "Will any foreign technology or information be shared with the item?"
        TITLE_AS_LABEL_FOR = "is_foreign_tech_or_information_shared"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    is_foreign_tech_or_information_shared = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label=Layout.TITLE,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
    )

    def get_layout_fields(self):
        return ("is_foreign_tech_or_information_shared",)


class ControlledUnderItar(BaseForm):
    class Layout:
        TITLE = (
            "Is the technology or information controlled under the US International Traffic in Arms Regulations (ITAR)?"
        )
        TITLE_AS_LABEL_FOR = "is_controlled_under_itar"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    is_controlled_under_itar = forms.TypedChoiceField(
        choices=(
            (True, "Yes, it's controlled under  ITAR"),
            (False, "No"),
        ),
        help_text="We need to know about any items classified as Defence Articles or Technical Data.",
        label=Layout.TITLE,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
    )

    def get_layout_fields(self):
        return (
            "is_controlled_under_itar",
            HTML.details(
                "Help with ITAR",
                render_to_string("f680/forms/help_ITAR.html"),
            ),
        )
