from datetime import datetime

from django import forms
from django.core.validators import EmailValidator
from django.db.models import TextChoices
from django.template.loader import render_to_string

from crispy_forms_gds.choices import Choice
from crispy_forms_gds.layout.content import HTML

from core.common.forms import BaseForm, TextChoice
from core.forms.layouts import (
    F680ConditionalCheckboxes,
    F680ConditionalCheckboxesQuestion,
    ConditionalRadios,
    ConditionalRadiosQuestion,
)
from core.forms.utils import coerce_str_to_bool

from exporter.core.forms import CustomErrorDateInputField
from exporter.core.validators import PastDateValidator
from exporter.f680.constants import SecurityGrading

from exporter.core.organisation.validators import validate_phone


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
        label="",
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
        error_messages={
            "required": "Enter details about what you're seeking approval to do",
        },
    )

    def clean(self):
        required_fields = ["demonstration_in_uk", "demonstration_overseas"]
        cleaned_data = super().clean()
        approval_choices = cleaned_data.get("approval_choices", [])

        for choice in approval_choices:
            required_field_data = cleaned_data.get(choice, False)
            if choice in required_fields and not required_field_data:
                self.add_error(choice, "What you're demonstrating and why cannot be blank")

        return cleaned_data

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
        label="",
        help_text="Where possible include the make, model and type of the item",
        error_messages={"required": "Enter a descriptive name"},
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
        label="",
        help_text="Where possible include the make, model and type of the item",
        widget=forms.Textarea(attrs={"rows": 5}),
        error_messages={"required": "Enter a description"},
    )

    def get_layout_fields(self):
        return (
            "product_description",
            HTML.details(
                "Help with incorporating an item",
                render_to_string("f680/forms/help_product_description.html"),
            ),
        )


class ProductHasSecurityClassification(BaseForm):
    class Layout:
        TITLE = "Has the product been given a security classifcation by a UK MOD authority?"
        TITLE_AS_LABEL_FOR = "has_security_classification"
        SUBMIT_BUTTON_TEXT = "Continue"

    has_security_classification = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label="",
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        error_messages={"required": "Select yes if you have a security classification"},
    )

    def get_layout_fields(self):
        return ("has_security_classification",)


class ActionTakenToClassifyInfo(BaseForm):
    class Layout:
        TITLE = "Provide details on what action will have to be taken to have the product security classified"
        TITLE_AS_LABEL_FOR = "actions_to_classify"
        SUBMIT_BUTTON_TEXT = "Continue"

    actions_to_classify = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"rows": 5}),
        error_messages={"required": "Enter details about what you have done to get the item security classified"},
    )

    def get_layout_fields(self):
        return ("actions_to_classify",)


class ProductSecurityClassificationForm(BaseForm):
    class Layout:
        TITLE = "What is the maximum security classification given?"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    prefix = forms.CharField(
        label="Enter a prefix (optional)",
        required=False,
    )
    security_classification = forms.ChoiceField(
        choices=SecurityGrading.product_choices,
        label="Select security classification",
        widget=forms.RadioSelect,
        error_messages={"required": "Select a security classification"},
    )
    other_security_classification = forms.CharField(
        label="Enter the security classification",
        required=False,
    )
    suffix = forms.CharField(
        label="Enter a suffix (optional)",
        help_text="For example, UK eyes only",
        required=False,
    )
    issuing_authority_name_address = forms.CharField(
        label="Name and address of the issuing authority",
        widget=forms.Textarea(attrs={"rows": "5"}),
        error_messages={"required": "Enter who issued the security classification"},
    )
    reference = forms.CharField(
        label="Reference",
        error_messages={"required": "Enter a reference"},
    )
    date_of_issue = CustomErrorDateInputField(
        label="Date of issue",
        require_all_fields=False,
        help_text=f"For example, 20 2 {datetime.now().year-1}",
        error_messages={
            "required": "Enter the date of issue",
            "incomplete": "Enter the date of issue",
            "invalid": "Date of issue must be a real date",
            "day": {
                "incomplete": "Date of issue must include a day",
                "invalid": "Date of issue must be a real date",
            },
            "month": {
                "incomplete": "Date of issue must include a month",
                "invalid": "Date of issue must be a real date",
            },
            "year": {
                "incomplete": "Date of issue must include a year",
                "invalid": "Date of issue must be a real date",
            },
        },
        validators=[PastDateValidator("Date of issue must be in the past")],
    )

    def clean(self):
        return self.add_required_to_conditional_text_field(
            {
                "parent_field": "security_classification",
                "parent_field_response": "other",
                "required_field": "other_security_classification",
                "error_message": "Security classification cannot be blank",
            }
        )

    def __init__(self, *args, **kwargs):
        self.conditional_radio_choices = [
            (
                ConditionalRadiosQuestion(choice.label, "other_security_classification")
                if choice.value == "other"
                else choice.label
            )
            for choice in SecurityGrading.product_choices
        ]
        super().__init__(*args, **kwargs)
        self.fields["security_classification"].choices = SecurityGrading.product_choices

    def get_layout_fields(self):
        return (
            "prefix",
            ConditionalRadios("security_classification", *self.conditional_radio_choices),
            "suffix",
            "issuing_authority_name_address",
            "reference",
            "date_of_issue",
        )


class ProductForeignTechOrSharedInformation(BaseForm):
    class Layout:
        TITLE = "Will any foreign technology or information be shared with the item?"
        TITLE_AS_LABEL_FOR = "is_foreign_tech_or_information_shared"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    is_foreign_tech_or_information_shared = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label="",
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        error_messages={"required": "Select yes if you will be sharing foreign technology"},
    )

    def get_layout_fields(self):
        return ("is_foreign_tech_or_information_shared",)


class ProductControlledUnderItar(BaseForm):
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
        label="",
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        error_messages={"required": "Select yes if the foreign technology is controlled under ITAR"},
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

    def clean(self):
        return self.add_required_to_conditional_text_field(
            {
                "parent_field": "is_controlled_under_itar",
                "parent_field_response": False,
                "required_field": "controlled_info",
                "error_message": "Information on how the foreign technology or information is controlled cannot be blank",
            }
        )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_controlled_under_itar",
                "Yes, it's controlled under  ITAR",
                ConditionalRadiosQuestion("No", "controlled_info"),
            ),
            HTML.details(
                "Help with ITAR",
                render_to_string("f680/forms/help_ITAR.html"),
            ),
        )


class ProductControlledUnderItarDetails(BaseForm):
    class Layout:
        TITLE = "Tell us about the technology or information controlled under ITAR"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    controlled_information = forms.CharField(
        label="What is the ITAR controlled technology or information?",
        widget=forms.Textarea(attrs={"rows": 5}),
        error_messages={"required": "Enter details about the ITAR controlled technology or information"},
    )

    itar_reference_number = forms.CharField(
        label="ITAR reference number",
        help_text="You can find this on the licence, agreement or authorisation you received from the US",
        error_messages={"required": "Enter an ITAR reference number"},
    )

    usml_categories = forms.CharField(
        label="What are the United States Munitions List (USML) categories listed on your ITAR approval?",
        help_text="You can find this on the licence, agreement or authorisation you received from the US",
        error_messages={"required": "Enter a USML category"},
    )

    itar_approval_scope = forms.CharField(
        label="Describe the scope of your ITAR approval",
        help_text="You can find this on the licence, agreement or authorisation you received from the US",
        widget=forms.Textarea(attrs={"rows": 5}),
        error_messages={"required": "Enter details about the ITAR approval scope"},
    )

    expected_time_in_possession = forms.CharField(
        label=(
            "How long do you expect the technology or information that is controlled under the US ITAR "
            "to be in your possession?"
        ),
        help_text="For example, 10 years",
        error_messages={"required": "Enter how long you'll possess the technology or information"},
    )

    def get_layout_fields(self):
        return (
            "controlled_information",
            "itar_reference_number",
            "usml_categories",
            "itar_approval_scope",
            "expected_time_in_possession",
        )


class ProductIncludeCryptography(BaseForm):
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
        label="",
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        error_messages={"required": "Select yes if the item includes information security features"},
    )

    cryptography_or_security_feature_info = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        label="Provide full details",
        required=False,
    )

    def clean(self):
        return self.add_required_to_conditional_text_field(
            {
                "parent_field": "is_including_cryptography_or_security_features",
                "parent_field_response": True,
                "required_field": "cryptography_or_security_feature_info",
                "error_message": "Details about the information security features cannot be blank",
            }
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


class ProductRatedUnderMTCR(BaseForm):
    class Layout:
        TITLE = "Do you believe the item is rated under the Missile Technology Control Regime (MTCR)"
        TITLE_AS_LABEL_FOR = "is_item_rated_under_mctr"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    is_item_rated_under_mctr = forms.ChoiceField(
        choices=(
            Choice("mtcr_1", "Yes, the product is MTCR Category 1"),
            Choice("mtcr_2", "Yes, the product is MTCR Category 2"),
            Choice("supports_mtcr_1", "No, but the item supports a MTCR Category 1 item"),
            Choice("supports_mtcr_2", "No, but the item supports a MTCR Category 2 item"),
            Choice("no", "No", divider="Or"),
            Choice("dont_know", "Don't know"),
        ),
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select yes if the product is rated under MTCR"},
    )

    def get_layout_fields(self):
        return (
            "is_item_rated_under_mctr",
            HTML.details(
                "Help with MTCR categories",
                render_to_string("f680/forms/help_mctr_categories.html"),
            ),
        )


class ProductMANPADs(BaseForm):
    class Layout:
        TITLE = "Do you believe the item is a man-portable air defence system (MANPAD)?"
        TITLE_AS_LABEL_FOR = "is_item_manpad"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    is_item_manpad = forms.ChoiceField(
        choices=(
            Choice("yes", "Yes, the product is a MANPAD"),
            Choice("no", "No, the product is not a MANPAD", divider="Or"),
            Choice("dont_know", "Don't know"),
        ),
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select yes if the product is a MANPADS"},
    )

    def get_layout_fields(self):
        return (
            "is_item_manpad",
            HTML.details(
                "Help with MANPADs",
                render_to_string("f680/forms/help_manpads.html"),
            ),
        )


class ProductElectronicMODData(BaseForm):
    class Layout:
        TITLE = "Will any electronic warfare data owned by the Ministry of Defence (MOD) be shared with the item?"
        TITLE_AS_LABEL_FOR = "is_mod_electronic_data_shared"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    is_mod_electronic_data_shared = forms.ChoiceField(
        choices=(
            Choice("yes", "Yes"),
            Choice("no", "No"),
        ),
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select yes if EW data will be shared"},
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_mod_electronic_data_shared",
                ConditionalRadiosQuestion(
                    "Yes",
                    HTML.p(
                        "You need to complete part A off the MOD EW Data Release Capture Form and attach "
                        "it to the application in the supporting documents section"
                    ),
                ),
                "No",
            ),
            HTML.details(
                "Help with electronic warfare data",
                render_to_string("f680/forms/help_electronic_warfare_data.html"),
            ),
        )


class ProductFunding(BaseForm):
    class Layout:
        TITLE = "Who is funding the item?"
        TITLE_AS_LABEL_FOR = "funding_source"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    funding_source = forms.ChoiceField(
        choices=(
            Choice("mod", "MOD"),
            Choice("part_mod", "Part MOD"),
            Choice("private_venture", "Private venture"),
        ),
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select who is funding the item"},
    )

    def get_layout_fields(self):
        return ("funding_source",)


class ModSponsorDetails(BaseForm):
    class Layout:
        TITLE = "Who is funding the item?"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    full_name = forms.CharField(
        label="Full name",
        error_messages={"required": "Enter the sponsor's full name"},
    )
    address = forms.CharField(
        label="Address",
        widget=forms.Textarea(attrs={"rows": 5}),
        error_messages={"required": "Enter the sponsor's address"},
    )
    phone_number = forms.CharField(
        label="Phone number",
        error_messages={
            "required": "Enter the sponsor's phone number",
        },
        validators=[validate_phone],
    )
    email_address = forms.CharField(
        label="Email address",
        error_messages={
            "required": "Enter the sponsor's email address",
        },
        validators=[EmailValidator("Enter an email address in the correct format, like name@example.com")],
    )

    def get_layout_fields(self):
        return (
            "full_name",
            "address",
            "phone_number",
            "email_address",
        )


class ProductUsedByUKArmedForces(BaseForm):
    class Layout:
        TITLE = "Will the item be used by the UK Armed Forces?"
        TITLE_AS_LABEL_FOR = "is_used_by_uk_armed_forces"
        SUBMIT_BUTTON_TEXT = "Save and continue"

    is_used_by_uk_armed_forces = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label="",
        widget=forms.RadioSelect,
        coerce=coerce_str_to_bool,
        error_messages={"required": "Select yes if UK armed forced will use the item"},
    )

    used_by_uk_armed_forces_info = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        label="Explain how it will be used",
        required=False,
    )

    def clean(self):
        return self.add_required_to_conditional_text_field(
            {
                "parent_field": "is_used_by_uk_armed_forces",
                "parent_field_response": True,
                "required_field": "used_by_uk_armed_forces_info",
                "error_message": "Details about how the item will be used cannot be blank",
            }
        )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_used_by_uk_armed_forces",
                ConditionalRadiosQuestion("Yes", "used_by_uk_armed_forces_info"),
                "No",
            ),
        )
