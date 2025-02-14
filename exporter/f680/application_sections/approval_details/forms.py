from django import forms
from django.utils.html import format_html

from core.common.forms import BaseForm


class ProductNameForm(BaseForm):
    class Layout:
        TITLE = "Give the item a descriptive name"
        TITLE_AS_LABEL_FOR = "product_name"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    product_name = forms.CharField(
        label=format_html(
            '<p class="govuk-body">We need to understand what you will be sharing with non-uk entities.  '
            'This includes: <br><ul class="govuk-body"><li>physical products</li>'
            "<li>substitute products</li><li>agreements</li><li>brochures</li><li>manuals</li>"
            "<li>training guides</li></ul></p>"
        ),
        help_text="Where possible include the make, model and type of the item",
    )

    def get_layout_fields(self):
        return ("product_name",)
