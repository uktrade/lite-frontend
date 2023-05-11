from crispy_forms_gds.choices import Choice
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit, HTML, Field, Button
from django import forms
from django.core.validators import MaxLengthValidator
from django.urls import reverse_lazy

from core.forms.widgets import Autocomplete

from caseworker.users.services import get_gov_users
import logging


class NotesAndTimelineForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "2", "class": "case-note__textarea"}),
        error_messages={"required": "Case Notes are Required"},
        label="Add a case note",
    )
    mentions = forms.MultipleChoiceField(
        choices=(),
        error_messages={"required": "Select the User"},
        label="Mention a co-worker or team to notify them, or ask a question.",
        help_text="Type for suggestions. For example 'Technical Assessment Unit', NSCS, or 'Olivia Smith'",
    )

    is_urgent = forms.BooleanField(label="Mark as urgent", initial=False, required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        self.fields["mentions"].widget = forms.SelectMultiple()

        users = get_gov_users(request, convert_to_choices=True)
        self.fields["mentions"].choices += users

        self.helper = FormHelper()
        self.helper.layout = Layout(
            "text",
            "mentions",
            Field.checkboxes("is_visible_to_exporter", small=True),
            Field.checkboxes("is_urgent", small=True),
            Submit("submit", "Add a case note", disabled=True),
            Button.secondary("cancel", "Cancel"),
        )
