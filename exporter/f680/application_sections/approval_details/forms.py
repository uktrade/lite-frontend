from django import forms
from django.db.models import TextChoices
from django.template.loader import render_to_string

from crispy_forms_gds.layout.content import HTML

from core.common.forms import BaseForm, TextChoice
from core.forms.layouts import (
    F680ConditionalCheckboxes,
    F680ConditionalCheckboxesQuestion,
    ConditionalRadios,
    ConditionalRadiosQuestion,
)
from core.forms.utils import coerce_str_to_bool


class ApprovalTypeForm(BaseForm):
    class Layout:
        TITLE = "Select the types of approvals you need"
        TITLE_AS_LABEL_FOR = "approval_choices"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    class ApprovalTypeChoices(TextChoices):
        INITIAL_DISCUSSIONS_OR_PROMOTING = (
            "initial_discussion_or_promoting",
            "Initial discussions or promoting products",
        )
        DEMONSTRATION_IN_THE_UK = (
            "demonstration_in_uk",
            "Demonstration in the United Kingdom to overseas customers",
        )
        DEMONSTRATION_OVERSEAS = "demonstration_overseas", "Demonstration overseas"
        TRAINING = "training", "Training"
        THROUGH_LIFE_SUPPORT = "through_life_support", "Through life support"
        SUPPLY = "supply", "Supply"

    ApprovalTypeChoices = (
        TextChoice(ApprovalTypeChoices.INITIAL_DISCUSSIONS_OR_PROMOTING),
        TextChoice(ApprovalTypeChoices.DEMONSTRATION_IN_THE_UK),
        TextChoice(ApprovalTypeChoices.DEMONSTRATION_OVERSEAS),
        TextChoice(ApprovalTypeChoices.TRAINING),
        TextChoice(ApprovalTypeChoices.THROUGH_LIFE_SUPPORT),
        TextChoice(ApprovalTypeChoices.SUPPLY),
    )

    approval_choices = forms.MultipleChoiceField(
        label=Layout.TITLE,
        choices=(),
        error_messages={
            "required": "Select an approval choice",
        },
        widget=forms.CheckboxSelectMultiple(),
    )

    demonstration_in_uk = forms.CharField(
        label="Explain what you are demonstrating and why",
        help_text="Explain what materials will be involved and if you'll use a substitute product",
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
    )

    demonstration_overseas = forms.CharField(
        label="Explain what you are demonstrating and why",
        help_text="Explain what materials will be involved and if you'll use a substitute product",
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
    )

    approval_details_text = forms.CharField(
        label="Provide details about what you're seeking approval to do",
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.conditional_checkbox_choices = (
            F680ConditionalCheckboxesQuestion(choices.label, choices.value) for choices in self.ApprovalTypeChoices
        )
        super().__init__(*args, **kwargs)
        self.fields["approval_choices"].choices = self.ApprovalTypeChoices

    def get_layout_fields(self):
        return (
            F680ConditionalCheckboxes("approval_choices", *self.conditional_checkbox_choices),
            "approval_details_text",
            HTML.details(
                "Help with exceptional circumstances",
                render_to_string("f680/forms/help_with_approval_type.html"),
            ),
        )


class ProductNameForm(BaseForm):
    class Layout:
        TITLE = "Give the item a descriptive name"
        TITLE_AS_LABEL_FOR = "product_name"
        SUBTITLE = render_to_string("f680/forms/subtitle_product_name.html")
        SUBMIT_BUTTON_TEXT = "Save and continue"

    product_name = forms.CharField(
        label=Layout.TITLE,
        help_text="Where possible include the make, model and type of the item",
    )

    def get_layout_fields(self):
        return ("product_name",)


class ProductDescription(BaseForm):
    class Layout:
        TITLE = "Describe the item"
        TITLE_AS_LABEL_FOR = "product_description"
        SUBTITLE = render_to_string("f680/forms/subtitle_product_description.html")
        SUBMIT_BUTTON_TEXT = "Save and continue"

    product_description = forms.CharField(
        label=Layout.TITLE,
        help_text="Where possible include the make, model and type of the item",
    )

    def get_layout_fields(self):
        return (
            "product_description",
            HTML.details(
                "Help with incorporating an item",
                render_to_string("f680/forms/help_product_description.html"),
            ),
        )


class ForeignTechOrSharedInformation(BaseForm):
    class Layout:
        TITLE = "Will any foreign technology or information be shared with the item?"
        TITLE_AS_LABEL_FOR = "is_foreign_tech_or_information_shared"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    is_foreign_tech_or_information_shared = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label=Layout.TITLE,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
    )

    def get_layout_fields(self):
        return ("is_foreign_tech_or_information_shared",)


class ControlledUnderItar(BaseForm):
    class Layout:
        TITLE = (
            "Is the technology or information controlled under the US International Traffic in Arms Regulations (ITAR)?"
        )
        TITLE_AS_LABEL_FOR = "is_controlled_under_itar"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    is_controlled_under_itar = forms.TypedChoiceField(
        choices=(
            (True, "Yes, it's controlled under  ITAR"),
            (False, "No"),
        ),
        help_text="We need to know about any items classified as Defence Articles or Technical Data.",
        label=Layout.TITLE,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
    )

    controlled_info = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        label=(
            "Explain how the technology or information is controlled."
            "Include countries classification levels and reference numbers."
            "  You can upload supporting documents later in your application"
        ),
        required=False,
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_controlled_under_itar",
                ConditionalRadiosQuestion("Yes, it's controlled under  ITAR", "controlled_info"),
                "No",
            ),
            HTML.details(
                "Help with ITAR",
                render_to_string("f680/forms/help_ITAR.html"),
            ),
        )


class AboutControlledUnderItar(BaseForm):
    class Layout:
        TITLE = "Tell us about the technology or information controlled under ITAR"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    controlled_information = forms.CharField(
        label="What is the ITAR controlled technology or information?",
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    itar_reference_number = forms.CharField(
        label="ITAR reference number",
        help_text="You can find this on the licence, agreement or authorisation you received from the US",
    )

    usml_categories = forms.CharField(
        label="What are the United States Munitions List (USML) categories listed on your ITAR approval?",
        help_text="You can find this on the licence, agreement or authorisation you received from the US",
    )

    itar_approval_scope = forms.CharField(
        label="Describe the scope of your ITAR approval",
        help_text="You can find this on the licence, agreement or authorisation you received from the US",
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    expected_time_in_possession = forms.CharField(
        label="How long do you expect the technology or information that is controlled under the US ITAR to be in your possession?",
        help_text="For example, 10 years",
    )

    def get_layout_fields(self):
        return (
            "controlled_information",
            "itar_reference_number",
            "usml_categories",
            "itar_approval_scope",
            "expected_time_in_possession",
        )


class IncludeCryptography(BaseForm):
    class Layout:
        TITLE = "Does the item include cryptography or other information security features?"
        TITLE_AS_LABEL_FOR = "is_including_cryptography_or_security_features"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    is_including_cryptography_or_security_features = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        help_text="We need to know about any items classified as Defence Articles or Technical Data.",
        label=Layout.TITLE,
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
    )

    cryptography_or_security_feature_info = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        label="Provide full details",
        required=False,
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_including_cryptography_or_security_features",
                ConditionalRadiosQuestion("Yes", "cryptography_or_security_feature_info"),
                "No",
            ),
            HTML.details(
                "Help with security features",
                render_to_string("f680/forms/help_security_features.html"),
            ),
        )


class ItemRatedUnderMCTR(BaseForm):
    class Layout:
        TITLE = "Do you believe the item is rated under the Missile Technology Control Regime (MTCR)"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    is_item_rated_under_mctr = forms.ChoiceField(
        choices=(
            ("Yes, the product is MTCR Category 1", "Yes, the product is MTCR Category 1"),
            ("Yes, the product is MTCR Category 2", "Yes, the product is MTCR Category 2"),
            ("No, but the item supports a MTCR Category 1 item", "No, but the item supports a MTCR Category 1 item"),
            ("No, but the item supports a MTCR Category 2 item", "No, but the item supports a MTCR Category 2 item"),
            ("No", "No"),
            ("Don't Know", "Don't know"),
        ),
        widget=forms.RadioSelect,
        label="Do you believe the item is rated under the Missile Technology Control Regime (MTCR)",
    )

    def get_layout_fields(self):
        return (
            "is_item_rated_under_mctr",
            HTML.details(
                "Help with MTCR categories",
                render_to_string("f680/forms/help_mctr_categories.html"),
            ),
        )


class ItemRatedUnderMCTR(BaseForm):
    class Layout:
        TITLE = "Do you believe the item is rated under the Missile Technology Control Regime (MTCR)"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    is_item_rated_under_mctr = forms.ChoiceField(
        choices=(
            ("Yes, the product is MTCR Category 1", "Yes, the product is MTCR Category 1"),
            ("Yes, the product is MTCR Category 2", "Yes, the product is MTCR Category 2"),
            ("No, but the item supports a MTCR Category 1 item", "No, but the item supports a MTCR Category 1 item"),
            ("No, but the item supports a MTCR Category 2 item", "No, but the item supports a MTCR Category 2 item"),
            ("No", "No"),
            ("Don't Know", "Don't know"),
        ),
        widget=forms.RadioSelect,
        label="Do you believe the item is rated under the Missile Technology Control Regime (MTCR)",
    )

    def get_layout_fields(self):
        return (
            "is_item_rated_under_mctr",
            HTML.details(
                "Help with MTCR categories",
                render_to_string("f680/forms/help_mctr_categories.html"),
            ),
        )
