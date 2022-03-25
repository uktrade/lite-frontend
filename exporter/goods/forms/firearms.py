from crispy_forms_gds.choices import Choice
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, HTML, Layout, Submit

from django import forms
from django.db import models
from django.template.loader import render_to_string

from core.forms.layouts import ConditionalQuestion, ConditionalRadios
from exporter.core.services import get_control_list_entries


class TextChoice(Choice):
    def __init__(self, choice, **kwargs):
        super().__init__(choice.value, choice.label, **kwargs)


class FirearmCategoryForm(forms.Form):
    class Layout:
        TITLE = "Firearm category"
        SUBTITLE = "Some firearm categories require a criminal conviction check and additonal documentation."
        SUBMIT_BUTTON = "Continue"

    class CategoryChoices(models.TextChoices):
        NON_AUTOMATIC_SHOTGUN = "NON_AUTOMATIC_SHOTGUN", "Non automatic shotgun"
        NON_AUTOMATIC_RIM_FIRED_RIFLE = "NON_AUTOMATIC_RIM_FIRED_RIFLE", "Non automatic rim-fired rifle"
        NON_AUTOMATIC_RIM_FIRED_HANDGUN = "NON_AUTOMATIC_RIM_FIRED_HANDGUN", "Non automatic rim-fired handgun"
        RIFLE_MADE_BEFORE_1938 = "RIFLE_MADE_BEFORE_1938", "Rifle made before 1938"
        COMBINATION_GUN_MADE_BEFORE_1938 = "COMBINATION_GUN_MADE_BEFORE_1938", "Combination gun made before 1938"
        NONE = "NONE", "None of the above"

    CATEGORY_CHOICES = (
        TextChoice(CategoryChoices.NON_AUTOMATIC_SHOTGUN),
        TextChoice(CategoryChoices.NON_AUTOMATIC_RIM_FIRED_RIFLE),
        TextChoice(CategoryChoices.NON_AUTOMATIC_RIM_FIRED_HANDGUN),
        TextChoice(CategoryChoices.RIFLE_MADE_BEFORE_1938),
        TextChoice(
            CategoryChoices.COMBINATION_GUN_MADE_BEFORE_1938,
            divider="or",
        ),
        TextChoice(CategoryChoices.NONE),
    )

    category = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
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
                "category",
                template="gds/layout/checkboxes_with_divider.html",
            ),
            Submit("submit", self.Layout.SUBMIT_BUTTON),
        )

    def clean_category(self):
        data = self.cleaned_data["category"]

        if self.CategoryChoices.NONE not in data:
            return data

        if data == [self.CategoryChoices.NONE]:
            return data

        raise forms.ValidationError('Select a firearm category, or select "None of the above"')


class FirearmNameForm(forms.Form):
    class Layout:
        TITLE = "Give the product a descriptive name"
        SUBTITLE = (
            "Try to match the name as closely as possible to any documentation such as the technical "
            "specification, end user certificate or firearm certificate."
        )
        SUBMIT_BUTTON = "Continue"

    name = forms.CharField(
        label="",
        error_messages={
            "required": "Enter a descriptive name",
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
            HTML.p(self.Layout.SUBTITLE),
            "name",
            HTML.details(
                "Help with naming your product",
                render_to_string("goods/forms/firearms/help_with_naming_your_product.html"),
            ),
            Submit("submit", self.Layout.SUBMIT_BUTTON),
        )


class FirearmProductControlListEntryForm(forms.Form):
    class Layout:
        TITLE = "Do you know the product's control list entry?"
        SUBMIT_BUTTON = "Continue"

    is_good_controlled = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=lambda val: val == "True",
        label="",
        error_messages={
            "required": "Select yes if you know the products control list entry",
        },
    )

    control_list_entries = forms.MultipleChoiceField(
        choices=[],  # set in __init__
        label="Enter the control list entry (type to get suggestions)",
        required=False,
        # setting id for javascript to use
        widget=forms.SelectMultiple(attrs={"id": "control_list_entries"}),
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        clc_list = get_control_list_entries(request)
        self.fields["control_list_entries"].choices = [(entry["rating"], entry["rating"]) for entry in clc_list]

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
            ConditionalRadios(
                "is_good_controlled",
                ConditionalQuestion(
                    "Yes",
                    "control_list_entries",
                ),
                ConditionalQuestion(
                    "No",
                    HTML.p(
                        "The product will be assessed and given a control list entry. "
                        "If the product isn't subject to any controls, you'll be issued "
                        "with a 'no licence required' document."
                    ),
                ),
            ),
            HTML.details(
                "Help with control list entries",
                render_to_string("goods/forms/firearms/help_with_control_list_entries.html"),
            ),
            Submit("submit", self.Layout.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()

        is_good_controlled = cleaned_data.get("is_good_controlled")
        control_list_entries = cleaned_data.get("control_list_entries")

        if is_good_controlled and not control_list_entries:
            self.add_error("control_list_entries", "Enter the control list entry")

        return cleaned_data


class FirearmCalibreForm(forms.Form):
    class Layout:
        TITLE = "What is the calibre of the product?"
        SUBMIT_BUTTON = "Continue"

    calibre = forms.CharField(
        label="",
        error_messages={
            "required": "Enter the calibre",
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
            "calibre",
            Submit("submit", self.Layout.SUBMIT_BUTTON),
        )
