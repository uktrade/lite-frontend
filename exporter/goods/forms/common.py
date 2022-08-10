from crispy_forms_gds.layout import HTML

from django import forms
from django.template.loader import render_to_string

from exporter.core.common.forms import BaseForm


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
