from django import forms
from django.db import models

from core.common.forms import BaseForm, TextChoice
from core.forms.utils import coerce_str_to_bool


class ApplicationCopyConfirmationForm(BaseForm):
    CONFIRMATION_CHOICES = [(True, "Yes"), (False, "No")]
    help_text = """Selecting Yes creates an exact copy of the current application which can be used
    to make amendments. The new application will need to be submitted again after all amendments.
     You can still view current application but cannot modify it."""

    class Layout:
        TITLE = "Confirm to create a copy of this application for making amendments"

    confirm_copy = forms.TypedChoiceField(
        choices=CONFIRMATION_CHOICES,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        help_text=help_text,
        label="",
        error_messages={"required": "Confirmation required to copy application or not"},
    )

    def get_layout_fields(self):
        return ("confirm_copy",)


class ApplicationCopyEntitySelectionForm(BaseForm):

    class Layout:
        TITLE = "Select entities"

    class EntityChoices(models.TextChoices):
        PRODUCTS = "products", "Products"
        PARTIES = "parties", "Parties"

    ENTITY_CHOICES = (
        TextChoice(EntityChoices.PRODUCTS),
        TextChoice(EntityChoices.PARTIES),
    )

    entities = forms.MultipleChoiceField(
        choices=ENTITY_CHOICES,
        initial=["products", "parties"],
        label="Select the entities you would like to copy",
        widget=forms.CheckboxSelectMultiple(),
    )

    def get_layout_fields(self):
        return ("entities",)
