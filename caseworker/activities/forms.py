from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit, Field, HTML, Div
from django import forms
from caseworker.core.constants import UserStatuses
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
        label="Mention a co-worker to notify them, or ask a question (optional)",
        help_text="""Type for suggestions. For example 'Olivia Smith', or
        'Technical Assessment Unit' to choose from members of that team""",
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
        view_url = kwargs.pop("view_url", "")
        super().__init__(*args, **kwargs)

        users_data, _ = get_gov_users(request, {"disable_pagination": True, "status": UserStatuses.ACTIVE})
        user_choices = convert_users_to_choices(users_data["results"])

        self.fields["mentions"].choices += user_choices

        self.helper = FormHelper()
        self.helper.attrs = {"data-module": "case-note"}
        self.helper.layout = Layout(
            "text",
            Div("mentions", Field.checkboxes("is_urgent", small=True), css_class="case-note-mentions"),
            Div(
                Submit("submit", "Add a case note"),
                HTML(
                    f"""
                    <a id="id_cancel"
                        href={view_url}
                        class="govuk-body govuk-link govuk-link--no-visited-state case-note-cancel"
                        type="button"
                        draggable="false">
                        Cancel
                    </a>
                    """
                ),
                css_class="case-note__controls-buttons",
            ),
        )
