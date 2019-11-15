from django.urls import reverse_lazy
from lite_forms.components import TextInput, Select, Option, BackLink, Form

from core.builtins.custom_tags import get_string

_name = TextInput(title="Name", name="name")

_level = Select(
    name="level",
    options=[
        Option("Case", "Case"),
        Option("Organisation", "Organisation"),
        Option("Destination", "Destination"),
        Option("Good", "Good"),
    ],
    title="Level",
)

_back_link = BackLink("Back to Flags", reverse_lazy("flags:flags"))


def add_flag_form():
    return Form(
        title=get_string("flags.create"), questions=[_name, _level,], back_link=_back_link, default_button_name="Create"
    )


def edit_flag_form():
    return Form(title="Edit Flag", questions=[_name, _level,], back_link=_back_link, default_button_name="Save")
