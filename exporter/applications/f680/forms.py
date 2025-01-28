from core.common.forms import BaseForm
from django import forms


class F680NameForm(BaseForm):  # /PS-IGNORE

    class Layout:
        TITLE = "F680 application name"  # /PS-IGNORE
        TITLE_AS_LABEL_FOR = "name"

    name = forms.CharField(
        label="",
        error_messages={"required": "Enter a name"},
    )

    def get_layout_fields(self):
        return ("name",)


class f680InitialForm(BaseForm):  # /PS-IGNORE
    class Layout:
        TITLE = "Do you want an F680?"  # /PS-IGNORE
        TITLE_AS_LABEL_FOR = "f680"  # /PS-IGNORE

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
        return ("f680",)  # /PS-IGNORE
