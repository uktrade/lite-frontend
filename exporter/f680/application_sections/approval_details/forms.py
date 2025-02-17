from django import forms
from django.template.loader import render_to_string

from crispy_forms_gds.layout.content import HTML

from core.common.forms import BaseForm
from core.forms.utils import coerce_str_to_bool


class ProductNameForm(BaseForm):
    class Layout:
        TITLE = "Give the item a descriptive name"
        TITLE_AS_LABEL_FOR = "product_name"
        SUBTITLE = (
            '<p class="govuk-body">We need to understand what you will be sharing with non-uk entities.  '
            'This includes: <br><ul class="govuk-body"><li>physical products</li>'
            "<li>substitute products</li><li>agreements</li><li>brochures</li><li>manuals</li>"
            "<li>training guides</li></ul></p>"
        )
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
        ITLE_AS_LABEL_FOR = "foreign_or_shared_information"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    foreign_or_shared_information = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label=Layout.TITLE,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
    )

    def get_layout_fields(self):
        return ("foreign_or_shared_information",)
