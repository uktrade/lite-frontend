from datetime import datetime

from crispy_forms_gds.layout import HTML

from django import forms
from django.template.loader import render_to_string

from core.forms.layouts import (
    ConditionalQuestion,
    ConditionalRadios,
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
        TITLE = "Do you have the part number ?"

    is_part_number = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Enter the part number or select that you do not have a part number",
        },
    )
    part_number = forms.CharField(required=False)

    no_part_number_comments = forms.CharField(
        widget=forms.Textarea,
        label="Explain why you do not have a part number",
        required=False,
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_part_number",
                ConditionalQuestion(
                    "Yes",
                    "part_number",
                ),
                ConditionalQuestion("No", "no_part_number_comments"),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        part_number = cleaned_data.get("part_number")
        no_part_number_comments = cleaned_data.get("no_part_number_comments")
        is_part_number = cleaned_data.get("is_part_number")

        if is_part_number and not part_number:
            self.add_error("part_number", "Enter the part number or select that you do not have a part number")
        elif not is_part_number and not no_part_number_comments:
            self.add_error(
                "no_part_number_comments", "Enter the part number or select that you do not have a part number"
            )
        return cleaned_data
