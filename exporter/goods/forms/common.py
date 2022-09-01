from datetime import datetime
from decimal import Decimal

from crispy_forms_gds.layout import Field, HTML

from django import forms
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse

from core.forms.layouts import (
    ConditionalQuestion,
    ConditionalRadios,
    ConditionalCheckbox,
    Prefixed,
)
from exporter.core.common.forms import (
    BaseForm,
    coerce_str_to_bool,
)
from exporter.core.forms import CustomErrorDateInputField
from exporter.core.services import (
    get_control_list_entries,
    get_pv_gradings_v2,
)
from exporter.core.validators import PastDateValidator


class ProductNameForm(BaseForm):
    class Layout:
        TITLE = "Give the product a descriptive name"

    name = forms.CharField(
        label="",
        error_messages={
            "required": "Enter a descriptive name",
        },
    )

    def get_layout_fields(self):
        return (
            HTML.p(
                "Try to match the name as closely as possible to any documentation such as the technical "
                "specification, end user certificate or firearm certificate.",
            ),
            "name",
            HTML.details(
                "Help with naming your product",
                render_to_string("goods/forms/common/help_with_naming_your_product.html"),
            ),
        )


class ProductControlListEntryForm(BaseForm):
    class Layout:
        TITLE = "Do you know the product's control list entry?"

    is_good_controlled = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        error_messages={
            "required": "Select yes if you know the product's control list entry",
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

    def get_layout_fields(self):
        return (
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
                render_to_string("goods/forms/common/help_with_control_list_entries.html"),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        is_good_controlled = cleaned_data.get("is_good_controlled")
        control_list_entries = cleaned_data.get("control_list_entries")

        if is_good_controlled and not control_list_entries:
            self.add_error("control_list_entries", "Enter the control list entry")

        return cleaned_data


class ProductPVGradingForm(BaseForm):
    class Layout:
        TITLE = "Does the product have a government security grading or classification?"

    is_pv_graded = forms.TypedChoiceField(
        choices=(
            (True, "Yes (includes Unclassified)"),
            (False, "No"),
        ),
        label="",
        coerce=coerce_str_to_bool,
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product has a security grading or classification",
        },
    )

    def get_layout_fields(self):
        return (
            HTML.p("For example, UK Official or NATO Restricted."),
            "is_pv_graded",
            HTML.details(
                "Help with security gradings",
                render_to_string("goods/forms/common/help_with_security_gradings.html"),
            ),
        )


class ProductPVGradingDetailsForm(BaseForm):
    class Layout:
        TITLE = "What is the security grading or classification?"

    prefix = forms.CharField(
        required=False, label="Enter a prefix (optional)", help_text="For example, UK, NATO or OCCAR"
    )

    grading = forms.ChoiceField(
        choices=(),
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select the security grading",
        },
    )
    suffix = forms.CharField(required=False, label="Enter a suffix (optional)", help_text="For example, UK eyes only")

    issuing_authority = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}),
        label="Name and address of the issuing authority",
        error_messages={
            "required": "Enter the name and address of the issuing authority",
        },
    )

    reference = forms.CharField(
        label="Reference",
        error_messages={
            "required": "Enter the reference",
        },
    )

    date_of_issue = CustomErrorDateInputField(
        label="Date of issue",
        require_all_fields=False,
        help_text=f"For example, 20 2 {datetime.now().year-2}",
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

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        gradings = [(key, display) for grading in get_pv_gradings_v2(request) for key, display in grading.items()]
        self.fields["grading"].choices += gradings

    def get_layout_fields(self):
        return (
            "prefix",
            "grading",
            "suffix",
            "issuing_authority",
            "reference",
            "date_of_issue",
            HTML.details(
                "Help with security gradings",
                render_to_string("goods/forms/common/help_with_security_gradings.html"),
            ),
        )


class ProductPartNumberForm(BaseForm):
    class Layout:
        TITLE = "Do you have the part number?"

    part_number = forms.CharField(required=False, label="")

    part_number_missing = forms.BooleanField(required=False, label="I do not have a part number")

    no_part_number_comments = forms.CharField(
        widget=forms.Textarea,
        label="Explain why you do not have a part number",
        required=False,
    )

    def get_layout_fields(self):
        return (
            "part_number",
            ConditionalCheckbox("part_number_missing", "no_part_number_comments"),
        )

    def clean(self):
        cleaned_data = super().clean()

        part_number_missing = cleaned_data.get("part_number_missing")
        part_number = cleaned_data.get("part_number")
        no_part_number_comments = cleaned_data.get("no_part_number_comments")

        mutually_exclusive_error_message = "Enter the part number or select that you do not have a part number"

        if not part_number and not part_number_missing:
            self.add_error(
                "part_number",
                mutually_exclusive_error_message,
            )
        elif part_number and part_number_missing:
            self.add_error(
                "part_number_missing",
                mutually_exclusive_error_message,
            )
        elif not part_number and part_number_missing and not no_part_number_comments:
            self.add_error(
                "no_part_number_comments",
                "Enter a reason why you do not have a part number",
            )

        return cleaned_data


class ProductDocumentAvailabilityForm(BaseForm):
    class Layout:
        TITLE = "Do you have a document that shows what your product is and what it's designed to do?"

    is_document_available = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        widget=forms.RadioSelect,
        label="",
        error_messages={
            "required": "Select yes or no",
        },
    )

    no_document_comments = forms.CharField(
        widget=forms.Textarea,
        label="Explain why you are not able to upload a product document. This may delay your application.",
        required=False,
    )

    def get_layout_fields(self):
        return (
            HTML.p(render_to_string("goods/forms/common/product_document_hint_text.html")),
            ConditionalRadios(
                "is_document_available",
                "Yes",
                ConditionalQuestion("No", "no_document_comments"),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        comments = cleaned_data.get("no_document_comments")
        if cleaned_data.get("is_document_available") is False and comments == "":
            self.add_error(
                "no_document_comments",
                "Enter a reason why you cannot upload a product document",
            )

        if cleaned_data.get("is_document_available") is True:
            cleaned_data["no_document_comments"] = ""

        return cleaned_data


class ProductDocumentSensitivityForm(BaseForm):
    class Layout:
        TITLE = "Is the document rated above Official-sensitive?"

    is_document_sensitive = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the document is rated above Official-sensitive",
        },
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_document_sensitive",
                ConditionalQuestion(
                    "Yes",
                    HTML.p(render_to_string("goods/forms/common/product_document_contact_ecju.html")),
                ),
                "No",
            ),
        )


class ProductDocumentUploadForm(BaseForm):
    class Layout:
        TITLE = "Upload a document that shows what your product is designed to do"

    product_document = forms.FileField(
        label="Upload a file",
        error_messages={
            "required": "Select a document that shows what your product is designed to do",
        },
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}),
        label="",
        help_text="Description (optional)",
        required=False,
    )

    def __init__(self, *args, good_id=None, document=None, **kwargs):
        self.document = document
        if self.document:
            self.product_document_download_url = reverse(
                "goods:document",
                kwargs={
                    "pk": good_id,
                    "file_pk": self.document["id"],
                },
            )
            self.document_name = self.document["name"]

        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        layout_fields = ("product_document", "description")
        if self.document:
            self.fields["product_document"].required = False
            layout_fields = (
                HTML.p(
                    render_to_string(
                        "goods/forms/common/product_document_download_link.html",
                        {
                            "safe": self.document.get("safe", False),
                            "url": self.product_document_download_url,
                            "name": self.document_name,
                        },
                    ),
                ),
            ) + layout_fields

        return layout_fields


class ProductOnwardExportedForm(BaseForm):
    class Layout:
        TITLE = "Will the product be onward exported to any additional countries?"

    is_onward_exported = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product will be onward exported to additional countries",
        },
    )

    def get_layout_fields(self):
        return (
            HTML.p("Tell us if the item will be exported again, beyond its first destination."),
            HTML.p("This includes when the product has been incorporated into another item."),
            "is_onward_exported",
            HTML.details(
                "Help with incorporated products",
                render_to_string("goods/forms/common/help_with_incorporated_products.html"),
            ),
        )


class ProductOnwardAlteredProcessedForm(BaseForm):
    class Layout:
        TITLE = "Will the item be altered or processed before it is exported again?"

    is_onward_altered_processed = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No, it will be onward exported in its original state"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the item will be altered or processed before it is exported again",
        },
    )

    is_onward_altered_processed_comments = forms.CharField(
        widget=forms.Textarea,
        label="Explain how the product will be processed or altered",
        required=False,
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_onward_altered_processed",
                ConditionalQuestion("Yes", "is_onward_altered_processed_comments"),
                "No, it will be onward exported in its original state",
            ),
            HTML.details(
                "Help with altered or processed products",
                render_to_string("goods/forms/common/help_with_altered_processed_products.html"),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        is_onward_altered_processed = cleaned_data.get("is_onward_altered_processed")
        is_onward_altered_processed_comments = cleaned_data.get("is_onward_altered_processed_comments")

        if is_onward_altered_processed and not is_onward_altered_processed_comments:
            self.add_error("is_onward_altered_processed_comments", "Enter how the product will be altered or processed")

        if cleaned_data.get("is_onward_altered_processed") is False:
            cleaned_data["is_onward_altered_processed_comments"] = ""

        return cleaned_data


class ProductOnwardIncorporatedForm(BaseForm):
    class Layout:
        TITLE = "Will the product be incorporated into another item before it is onward exported?"

    is_onward_incorporated = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product will be incorporated into another item before it is onward exported",
        },
    )

    is_onward_incorporated_comments = forms.CharField(
        widget=forms.Textarea,
        label="Describe what you are incorporating the product into",
        required=False,
    )

    def get_layout_fields(self):
        return (
            HTML.p("For example, will it be integrated into a higher system, platform or software?"),
            ConditionalRadios(
                "is_onward_incorporated",
                ConditionalQuestion("Yes", "is_onward_incorporated_comments"),
                "No",
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        is_onward_incorporated = cleaned_data.get("is_onward_incorporated")
        is_onward_incorporated_comments = cleaned_data.get("is_onward_incorporated_comments")

        if is_onward_incorporated and not is_onward_incorporated_comments:
            self.add_error(
                "is_onward_incorporated_comments", "Enter a description of what you are incorporating the product into"
            )

        if cleaned_data.get("is_onward_incorporated") is False:
            cleaned_data["is_onward_incorporated_comments"] = ""

        return cleaned_data


class ProductQuantityAndValueForm(BaseForm):
    class Layout:
        TITLE = "Quantity and value"

    number_of_items = forms.IntegerField(
        error_messages={
            "invalid": "Number of items must be a number, like 16",
            "required": "Enter the number of items",
            "min_value": "Number of items must be 1 or more",
        },
        min_value=1,
        widget=forms.TextInput,
    )
    value = forms.DecimalField(
        decimal_places=2,
        error_messages={
            "invalid": "Total value must be a number, like 16.32",
            "required": "Enter the total value",
            "max_decimal_places": "Total value must not be more than 2 decimals",
            "min_value": "Total value must be 0.01 or more",
        },
        label="Total value",
        min_value=Decimal("0.01"),
        widget=forms.TextInput,
    )

    def get_layout_fields(self):
        return (
            Field("number_of_items", css_class="govuk-input--width-10 input-force-default-width"),
            Prefixed("£", "value", css_class="govuk-input--width-10 input-force-default-width"),
        )


class ProductUsesInformationSecurityForm(BaseForm):
    class Layout:
        TITLE = "Does the product include security features to protect information?"
        SUBTITLE = "For example, authentication, encryption or any other information security controls."

    uses_information_security = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product includes security features to protect information",
        },
    )

    information_security_details = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        label=f"Provide details of the information security features",
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "uses_information_security",
                ConditionalQuestion(
                    "Yes",
                    "information_security_details",
                ),
                "No",
            ),
            HTML.details(
                "Help with security features",
                render_to_string("goods/forms/common/help_with_security_features.html"),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        uses_information_security = cleaned_data.get("uses_information_security")
        information_security_details = cleaned_data.get("information_security_details")

        if uses_information_security and not information_security_details:
            self.add_error("information_security_details", "Enter details of the information security features")

        return cleaned_data


class ProductMilitaryUseForm(BaseForm):
    class Layout:
        TITLE = "Is the product specially designed or modified for military use?"

    class IsMilitaryUseChoices(models.TextChoices):
        YES_DESIGNED = "yes_designed", "Yes, it is specially designed for military use"
        YES_MODIFIED = "yes_modified", "Yes, it is modified for military use"
        NO = "no", "No"

    is_military_use = forms.ChoiceField(
        choices=IsMilitaryUseChoices.choices,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select if the product is specially designed or modified for military use",
        },
    )

    modified_military_use_details = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        label="Provide details of the modifications",
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_military_use",
                self.IsMilitaryUseChoices.YES_DESIGNED.label,
                ConditionalQuestion(
                    self.IsMilitaryUseChoices.YES_MODIFIED.label,
                    "modified_military_use_details",
                ),
                self.IsMilitaryUseChoices.NO.label,
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        is_military_use = cleaned_data.get("is_military_use")
        modified_military_use_details = cleaned_data.get("modified_military_use_details")

        if is_military_use == self.IsMilitaryUseChoices.YES_MODIFIED and not modified_military_use_details:
            self.add_error("modified_military_use_details", "Enter details of modifications")

        return cleaned_data


class ProductDescriptionForm(BaseForm):
    class Layout:
        TITLE = "Describe the product and what it is designed to do"

    product_description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        label="",
        error_messages={
            "required": "Enter a description of the product and what it is designed to do",
        },
    )

    def get_layout_fields(self):
        return ("product_description",)
