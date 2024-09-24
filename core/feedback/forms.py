from django import forms
from crispy_forms_gds.layout import HTML

from core.common.forms import BaseForm


class FeedbackForm(BaseForm):
    class Layout:
        TITLE = "Leave Feedback"
        SUBMIT_BUTTON_TEXT = "Submit"

    feedback = forms.CharField(label="", widget=forms.Textarea)

    text_p1 = """
                Use this form to give general feedback about your experience. We do not reply to feedback comments.
             """

    def get_layout_fields(self):
        return (HTML.p(self.text_p1), "feedback")
