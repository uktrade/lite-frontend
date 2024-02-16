from django import forms

from crispy_forms_gds.layout import Field, HTML

from core.common.forms import (
    BaseForm,
    MultipleFileField,
)


class AppealForm(BaseForm):
    class Layout:
        TITLE = "Appeal refusal decision"
        SUBMIT_BUTTON_TEXT = "Submit appeal request"

    grounds_for_appeal = forms.CharField(
        label="Describe your grounds for appeal",
        widget=forms.Textarea(),
    )
    documents = MultipleFileField(
        label="Attach any supporting documents",
    )

    def __init__(self, *args, cancel_url, **kwargs):
        self.cancel_url = cancel_url
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return [
            HTML.p(
                "You have the right to appeal if your export licence application has been refused. "
                "We cannot accept business-related factors as valid reasons for appeal."
            ),
            HTML.p("Examples of these would be contractual losses, economic concerns, loss of staff or site closures."),
            "grounds_for_appeal",
            Field(
                "documents",
                css_class="govuk-file-upload",
            ),
        ]

    def get_layout_actions(self):
        layout_actions = super().get_layout_actions()

        layout_actions.append(
            HTML(
                f'<a class="govuk-button govuk-button--secondary" href="{self.cancel_url}" id="cancel-id-cancel">Cancel</a>'
            ),
        )

        return layout_actions
