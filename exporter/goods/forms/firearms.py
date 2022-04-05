from crispy_forms_gds.choices import Choice
from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, HTML, Layout, Submit

from django import forms
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse

from core.forms.layouts import ConditionalQuestion, ConditionalRadios
from exporter.core.services import get_control_list_entries, get_pv_gradings_v2
from exporter.core.validators import FutureDateValidator, PastDateValidator, RelativeDeltaDateValidator


class CustomErrorDateInputField(DateInputField):
    def __init__(self, error_messages, **kwargs):
        super().__init__(**kwargs)

        for key, field in zip(["day", "month", "year"], self.fields):
            field_error_messages = error_messages.pop(key)
            field.error_messages["incomplete"] = field_error_messages["incomplete"]
            regex_validator = field.validators[0]
            regex_validator.message = field_error_messages["invalid"]

        self.error_messages = error_messages


def coerce_str_to_bool(val):
    return val == "True"


class TextChoice(Choice):
    def __init__(self, choice, **kwargs):
        super().__init__(choice.value, choice.label, **kwargs)


class BaseFirearmForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        for field in self.fields.values():
            if isinstance(field, forms.FileField):
                self.helper.attrs = {"enctype": "multipart/form-data"}
                break

        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
            *self.get_layout_fields(),
            Submit("submit", getattr(self.Layout, "SUBMIT_BUTTON", "Continue")),
        )

    def get_layout_fields(self):
        raise NotImplementedError(f"Implement `get_layout_fields` on {self.__class__.__name__}")


class FirearmCategoryForm(BaseFirearmForm):
    class Layout:
        TITLE = "Firearm category"

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

    def get_layout_fields(self):
        return (
            HTML.p("Some firearm categories require a criminal conviction check and additonal documentation."),
            Field(
                "category",
                template="gds/layout/checkboxes_with_divider.html",
            ),
        )

    def clean_category(self):
        data = self.cleaned_data["category"]

        if self.CategoryChoices.NONE not in data:
            return data

        if data == [self.CategoryChoices.NONE]:
            return data

        raise forms.ValidationError('Select a firearm category, or select "None of the above"')


class FirearmNameForm(BaseFirearmForm):
    class Layout:
        TITLE = "Give the product a descriptive name"

    title = Layout.TITLE
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
                render_to_string("goods/forms/firearms/help_with_naming_your_product.html"),
            ),
        )


class FirearmProductControlListEntryForm(BaseFirearmForm):
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
                render_to_string("goods/forms/firearms/help_with_control_list_entries.html"),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        is_good_controlled = cleaned_data.get("is_good_controlled")
        control_list_entries = cleaned_data.get("control_list_entries")

        if is_good_controlled and not control_list_entries:
            self.add_error("control_list_entries", "Enter the control list entry")

        return cleaned_data


class FirearmPvGradingForm(BaseFirearmForm):
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
                render_to_string("goods/forms/firearms/help_with_security_gradings.html"),
            ),
        )


class FirearmPvGradingDetailsForm(BaseFirearmForm):
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
        help_text="For example, 20 02 2020",
        error_messages={
            "required": "Enter the date of issue",
            "incomplete": "Enter the date of issue",
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
                render_to_string("goods/forms/firearms/help_with_security_gradings.html"),
            ),
        )


class FirearmCalibreForm(BaseFirearmForm):
    class Layout:
        TITLE = "What is the calibre of the product?"

    calibre = forms.CharField(
        label="",
        error_messages={
            "required": "Enter the calibre",
        },
    )

    def get_layout_fields(self):
        return ("calibre",)


class FirearmReplicaForm(BaseFirearmForm):
    class Layout:
        TITLE = "Is the product a replica firearm?"

    is_replica = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product is a replica firearm",
        },
    )

    replica_description = forms.CharField(
        widget=forms.Textarea,
        label="Describe the firearm the product is a replica of",
        required=False,
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_replica",
                ConditionalQuestion(
                    "Yes",
                    "replica_description",
                ),
                "No",
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        is_replica = cleaned_data.get("is_replica")
        replica_description = cleaned_data.get("replica_description")

        if is_replica and not replica_description:
            self.add_error("replica_description", "Enter a description")

        return cleaned_data


class FirearmRFDValidityForm(BaseFirearmForm):
    class Layout:
        TITLE = "Is your registered firearms dealer certificate still valid?"

    is_rfd_valid = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if your registered firearms dealer certificate is still valid",
        },
    )

    def __init__(self, rfd_certificate, *args, **kwargs):
        self.rfd_certificate_download_url = reverse(
            "organisation:document",
            kwargs={
                "pk": rfd_certificate["id"],
            },
        )
        self.rfd_certificate_name = rfd_certificate["document"]["name"]

        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return (
            HTML.p(
                render_to_string(
                    "goods/forms/firearms/rfd_certificate_download_link.html",
                    {
                        "url": self.rfd_certificate_download_url,
                        "name": self.rfd_certificate_name,
                    },
                ),
            ),
            "is_rfd_valid",
        )


class FirearmRegisteredFirearmsDealerForm(BaseFirearmForm):
    class Layout:
        TITLE = "Are you a registered firearms dealer?"

    is_registered_firearm_dealer = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if you are a registered firearms dealer",
        },
    )

    def get_layout_fields(self):
        return ("is_registered_firearm_dealer",)


class FirearmAttachRFDCertificate(BaseFirearmForm):
    class Layout:
        TITLE = "Upload a registered firearms dealer certificate"

    file = forms.FileField(
        label="",
        error_messages={
            "required": "Select a registered firearms dealer certificate",
        },
    )

    reference_code = forms.CharField(
        label="Certificate number",
        error_messages={
            "required": "Enter the certificate number",
        },
    )

    expiry_date = CustomErrorDateInputField(
        label="Expiry date",
        help_text="For example 27 3 2023",
        require_all_fields=False,
        error_messages={
            "required": "Enter the expiry date",
            "incomplete": "Enter the expiry date",
            "day": {
                "incomplete": "Expiry date must include a day",
                "invalid": "Expiry date must be a real date",
            },
            "month": {
                "incomplete": "Expiry date must include a month",
                "invalid": "Expiry date must be a real date",
            },
            "year": {
                "incomplete": "Expiry date must include a year",
                "invalid": "Expiry date must be a real date",
            },
        },
        validators=[
            FutureDateValidator("Expiry date must be in the future"),
            RelativeDeltaDateValidator("Expiry date must be within 5 years", years=5),
        ],
    )

    def get_layout_fields(self):
        return (
            "file",
            "reference_code",
            "expiry_date",
        )


class FirearmDocumentAvailability(BaseFirearmForm):
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
            HTML.p(render_to_string("goods/forms/firearms/product_document_hint_text.html")),
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

        return cleaned_data


class FirearmDocumentSensitivityForm(BaseFirearmForm):
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
                    HTML.p(render_to_string("goods/forms/firearms/product_document_contact_ecju.html")),
                ),
                "No",
            ),
        )


class FirearmDocumentUploadForm(BaseFirearmForm):
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

    def get_layout_fields(self):
        return (
            "product_document",
            "description",
        )
