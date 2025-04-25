from core.common.forms import BaseForm
from crispy_forms_gds.layout import HTML


class FinaliseForm(BaseForm):

    class Layout:
        TITLE = ""
        SUBMIT_BUTTON_TEXT = "Finalise and publish to exporter"

    def get_layout_fields(self):
        return []


class GenerateDocumentForm(BaseForm):
    class Layout:
        TITLE = "Generate document"
        SUBMIT_BUTTON_TEXT = "Generate"

    def __init__(self, *args, cancel_url, **kwargs):
        self.cancel_url = cancel_url
        super().__init__(*args, **kwargs)

    def get_layout_actions(self):
        layout_actions = super().get_layout_actions()
        layout_actions.append(
            HTML(
                f'<a class="govuk-button govuk-button--secondary" href="{self.cancel_url}" id="cancel-id-cancel">Cancel</a>'
            ),
        )
        return layout_actions

    def get_layout_fields(self):
        return [
            HTML.p(
                """
                This is a preview of the letter.  Check the preview is correct and then hit “Generate”.
                """
            ),
            HTML.p(
                """
                If anything is incorrect in the letter, update the incorrect content in the ‘Recommendations’ section and generate another letter.
                """
            ),
            HTML('<div class="app-letter-preview__page" id="preview">{{ preview|safe }}</div><br>'),
        ]
