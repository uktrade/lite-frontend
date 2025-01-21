from core.common.forms import BaseForm
from django import forms


class f680InitialForm(BaseForm):
    class Layout:
        TITLE = "Do you want an F680?"
        # TITLE_AS_LABEL_FOR = "reuse_party"

    f680 = forms.ChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if you want an f680",
        },
    )

    def get_layout_fields(self):
        return ("f680",)
