from django import forms

from core.common.forms import BaseForm


class NoteWidget(forms.Textarea):
    template_name = "applications/f680case-notes.html"  # /PS-IGNORE


class NotesForCaseOfficerForm(BaseForm):
    class Layout:
        TITLE = "Notes"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    note = forms.CharField(
        label="Add note",
        widget=NoteWidget(attrs={"cols": "80"}),
    )

    def get_context(self):
        return super().get_context()

    def get_layout_fields(self):
        return ("note",)
