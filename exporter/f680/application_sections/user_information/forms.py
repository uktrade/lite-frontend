from django import forms

from core.common.forms import BaseForm


class EntityTypeForm(BaseForm):
    class Layout:
        TITLE = "Select type of entity"
        TITLE_AS_LABEL_FOR = "entity_type"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    entity_type = forms.ChoiceField(
        choices=(
            ("end-user", "End user"),
            ("ultimate-end-user", "Ultimate end-user"),
            ("third-party", "Third party"),
        ),
        label="Select type of entity",
        widget=forms.RadioSelect,
    )

    def get_layout_fields(self):
        return ("entity_type",)
