from django import forms
from django.template.loader import render_to_string

from crispy_forms_gds.layout import HTML

from core.common.forms import BaseForm
from core.forms.layouts import (
    ConditionalRadiosQuestion,
    ConditionalRadios,
)
from core.forms.utils import coerce_str_to_bool


class ApplicationDeclarationForm(BaseForm):
    class Layout:
        TITLE = "Submit your application"
        BACK_LINK_TEXT = "Back to check your answers"
        SUBMIT_BUTTON_TEXT = "Accept and submit"

    # TODO: we should rename agreed_to_foi to be less confusing. The old
    # question asked if the exporter would find an FOI harmful to their
    # interests, but the variable name agreed_to_foi suggests the opposite,
    # that they agree to have their application be made public under FOI.
    # Maybe agreed_that_foi_harmful would be less confusing. Also,
    # the new question asks if the exporter agrees to make their application
    # publicly available, and the variable name should reflect that.
    agreed_to_foi = forms.TypedChoiceField(
        choices=((False, "Yes"), (True, "No")),
        coerce=coerce_str_to_bool,
        widget=forms.RadioSelect,
        label="",
        help_text="",
    )

    foi_reason = forms.CharField(
        widget=forms.Textarea,
        label=(
            "Explain why the disclosure of information would be harmful to your interests. "
            "While the Export Control Joint Unit (ECJU) will take your views into account, "
            "they cannot guarantee that the information will not be made public."
        ),
        required=False,
    )

    def clean(self):
        """
        We want the foi_reason field to be required if agreed_to_foi is No, but
        using the default required=True makes it error if this question is never
        shown. This is a difficulty with using ConditionalRadios. To achieve the
        desired behaviour we can raise a ValidationError if the No answer is given
        and foi_reason is left blank which displays a field error to the user.
        """
        cleaned_data = super().clean()
        agreed_to_foi = cleaned_data.get("agreed_to_foi")
        foi_reason = cleaned_data.get("foi_reason")
        if agreed_to_foi and not foi_reason:
            self.add_error("foi_reason", "Explain why the disclosure of information would be harmful to your interests")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return [
            HTML(
                render_to_string(
                    "applications/forms/declaration/declaration-heading-question.html",
                )
            ),
            ConditionalRadios("agreed_to_foi", "Yes", ConditionalRadiosQuestion("No", "foi_reason")),
            HTML(
                render_to_string(
                    "applications/forms/declaration/declaration-heading-declaration.html",
                )
            ),
        ]
