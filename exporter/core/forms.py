from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit, Layout, HTML

from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput


class RegisterNameForm(forms.Form):
    class Layout:
        TITLE = "What is your name?"

    first_name = forms.CharField(
        label="First name",
        required=True,
        error_messages={"required": "Enter your first name"},
    )
    last_name = forms.CharField(label="Last name", required=True, error_messages={"required": "Enter your last name"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
            "first_name",
            "last_name",
            Submit("submit", "Continue"),
        )


class CurrentFile:
    def __init__(self, name, url, safe):
        self.name = name
        self.url = url
        self.safe = safe

    def __str__(self):
        return self.name


class PotentiallyUnsafeClearableFileInput(ClearableFileInput):
    template_name = "core/widgets/potentially_unsafe_clearable_file_input.html"

    def __init__(self, *args, force_required=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.force_required = force_required

    def is_initial(self, value):
        return isinstance(value, CurrentFile)

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)

        if self.force_required is not None:
            context["widget"]["required"] = self.force_required

        return context


class CustomErrorDateInputField(DateInputField):
    def __init__(self, error_messages, **kwargs):
        super().__init__(**kwargs)

        self.custom_messages = {}

        for key, field in zip(["day", "month", "year"], self.fields):
            field_error_messages = error_messages.pop(key)
            field.error_messages["incomplete"] = field_error_messages["incomplete"]

            regex_validator = field.validators[0]
            regex_validator.message = field_error_messages["invalid"]

            self.custom_messages[key] = field_error_messages

        self.error_messages = error_messages

    def compress(self, data_list):
        try:
            return super().compress(data_list)
        except ValidationError as e:
            # These are the error strings that come back from the datetime
            # library that then get bundled into a ValidationError from the
            # parent.
            # In this case the best we can do is to match on these strings
            # and then give back the error message that makes the most sense.
            # If we fail to find a matching message we will still give back a
            # user friendly message.
            if e.message == "day is out of range for month":
                raise ValidationError(self.custom_messages["day"]["invalid"])
            if e.message == "month must be in 1..12":
                raise ValidationError(self.custom_messages["month"]["invalid"])
            if e.message == f"year {data_list[2]} is out of range":
                raise ValidationError(self.custom_messages["year"]["invalid"])
            raise ValidationError(self.error_messages["invalid"])
