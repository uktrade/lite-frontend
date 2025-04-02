from core.common.forms import BaseForm


class ApplicationPresubmissionForm(BaseForm):
    class Layout:
        TITLE = ""
        SUBMIT_BUTTON_TEXT = "Save and continue"

    def get_layout_fields(self):
        return []


class ApplicationSubmissionForm(BaseForm):
    class Layout:
        TITLE = ""
        SUBMIT_BUTTON_TEXT = "Submit"

    def get_layout_fields(self):
        return []
