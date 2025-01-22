from core.common.forms import BaseForm
from django import forms


class F680NameForm(BaseForm):

    class Layout:
        TITLE = "F680 application name"
        TITLE_AS_LABEL_FOR = "name"

    name = forms.CharField(
        label="",
        error_messages={"required": "Enter a name"},
    )

    def get_layout_fields(self):
        return ("name",)


class f680InitialForm(BaseForm):
    class Layout:
        TITLE = "Do you want an F680?"
        TITLE_AS_LABEL_FOR = "f680"

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
