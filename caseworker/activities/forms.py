from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit, Field, HTML, Div
from django import forms
from django.conf import settings

from caseworker.users.services import get_gov_users, convert_users_to_choices


class NotesAndTimelineForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "2", "class": "case-note__textarea"}),
        error_messages={"required": "Case Notes are Required"},
        label="Add a case note",
    )
    mentions = forms.MultipleChoiceField(
        choices=(),
        widget=forms.SelectMultiple(),
        label="Mention a co-worker or team to notify them, or ask a question (optional)",
        help_text="Type for suggestions. For example 'Technical Assessment Unit', NSCS, or 'Olivia Smith'",
        required=False,
    )
    is_urgent = forms.BooleanField(label="Mark as urgent", initial=False, required=False)

    def clean_mentions(self):
        mentions = self.cleaned_data["mentions"]
        data = [{"user": user_id} for user_id in mentions]
        return data

    def clean_is_urgent(self):
        return bool(self.cleaned_data.get("is_urgent", False))

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        users_data, _ = get_gov_users(request)
        user_choices = convert_users_to_choices(users_data["results"])

        self.fields["mentions"].choices += user_choices

        self.helper = FormHelper()
        self.helper.form_id = "case_notes"
        self.helper.layout = Layout(
            "text",
            "mentions",
            Field.checkboxes("is_urgent", small=True),
            Div(
                Submit("submit", "Add a case note"),
                HTML(
                    '<a id="id_cancel" href={% url "cases:activities:notes-and-timeline" pk=case.id queue_pk=queue.id %} class="govuk-body govuk-link govuk-link--no-visited-state case-note__cancel-button" type="button" draggable="false">Cancel</a>'
                ),
                css_class="case-note__controls-buttons",
            ),
        )

        if not settings.FEATURE_MENTIONS_ENABLED:
            del self.fields["mentions"]
            del self.fields["is_urgent"]
