from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit


class SelectRecommendationTypeForm(forms.Form):
    CHOICES = [
        ("approve_all", "Approve all"),
    ]

    recommendation = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select if you approve all or refuse all"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Continue"))
