from crispy_forms_gds.layout import HTML

from core.feedback.forms import FeedbackForm


class ExporterFeedbackForm(FeedbackForm):

    def __init__(self, help_support_url, *args, **kwargs):
        self.text_p2 = f"""
            <a class="govuk-link" href='{help_support_url}'>
            Get help with your application</a> on our support page if you have a specific problem or need a reply.
            """
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return (HTML.p(self.text_p1), HTML.p(self.text_p2), "feedback")
