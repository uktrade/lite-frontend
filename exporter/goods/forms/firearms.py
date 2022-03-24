from crispy_forms_gds.choices import Choice
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, HTML, Layout, Submit

from django import forms
from django.db import models


class TextChoice(Choice):
    def __init__(self, choice, **kwargs):
        super().__init__(choice.value, choice.label, **kwargs)


class FirearmCategoryForm(forms.Form):
    class Layout:
        TITLE = "Firearm category"
        SUBTITLE = "Some firearm categories require a criminal conviction check and additonal documentation."
        SUBMIT_BUTTON = "Continue"

    class FirearmCategoryChoices(models.TextChoices):
        NON_AUTOMATIC_SHOTGUN = "NON_AUTOMATIC_SHOTGUN", "Non automatic shotgun"
        NON_AUTOMATIC_RIM_FIRED_RIFLE = "NON_AUTOMATIC_RIM_FIRED_RIFLE", "Non automatic rim-fired rifle"
        NON_AUTOMATIC_RIM_FIRED_HANDGUN = "NON_AUTOMATIC_RIM_FIRED_HANDGUN", "Non automatic rim-fired handgun"
        RIFLE_MADE_BEFORE_1938 = "RIFLE_MADE_BEFORE_1938", "Rifle made before 1938"
        COMBINATION_GUN_MADE_BEFORE_1938 = "COMBINATION_GUN_MADE_BEFORE_1938", "Combination gun made before 1938"
        NONE = "NONE", "None of the above"

    FIREARM_CATEGORY_CHOICES = (
        TextChoice(FirearmCategoryChoices.NON_AUTOMATIC_SHOTGUN),
        TextChoice(FirearmCategoryChoices.NON_AUTOMATIC_RIM_FIRED_RIFLE),
        TextChoice(FirearmCategoryChoices.NON_AUTOMATIC_RIM_FIRED_HANDGUN),
        TextChoice(FirearmCategoryChoices.RIFLE_MADE_BEFORE_1938),
        TextChoice(
            FirearmCategoryChoices.COMBINATION_GUN_MADE_BEFORE_1938,
            divider="or",
        ),
        TextChoice(FirearmCategoryChoices.NONE),
    )

    firearm_category = forms.MultipleChoiceField(
        choices=FIREARM_CATEGORY_CHOICES,
        error_messages={
            "required": 'Select a firearm category, or select "None of the above"',
        },
        label="Does the product belong to any of the following categories?",
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
            HTML.p(self.Layout.SUBTITLE),
            Field(
                "firearm_category",
                template="gds/layout/checkboxes_with_divider.html",
            ),
            Submit("submit", self.Layout.SUBMIT_BUTTON),
        )

    def clean_firearm_category(self):
        data = self.cleaned_data["firearm_category"]

        if self.FirearmCategoryChoices.NONE not in data:
            return data

        if data == [self.FirearmCategoryChoices.NONE]:
            return data

        raise forms.ValidationError('Select a firearm category, or select "None of the above"')
