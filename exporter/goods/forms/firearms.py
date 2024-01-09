from crispy_forms_gds.layout import Field, HTML

from django import forms
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse

from core.constants import (
    FirearmsActSections,
    SerialChoices,
)
from core.forms.layouts import (
    ConditionalCheckbox,
    ConditionalRadiosQuestion,
    ConditionalRadios,
)
from core.forms.utils import coerce_str_to_bool

from core.common.forms import BaseForm, TextChoice
from exporter.core.forms import (
    CustomErrorDateInputField,
    PotentiallyUnsafeClearableFileInput,
)
from exporter.core.validators import (
    FutureDateValidator,
    PastDateValidator,
    RelativeDeltaDateValidator,
)
from exporter.goods.forms.goods import SerialNumbersField


class FirearmCategoryForm(BaseForm):
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


class FirearmCalibreForm(BaseForm):
    class Layout:
        TITLE = "What is the calibre of the product?"
        TITLE_AS_LABEL_FOR = "calibre"

    calibre = forms.CharField(
        label="",
        error_messages={
            "required": "Enter the calibre",
        },
    )

    def get_layout_fields(self):
        return ("calibre",)


class FirearmReplicaForm(BaseForm):
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
        widget=forms.TextInput,
        label="Describe the firearm the product is a replica of ",
        required=False,
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "is_replica",
                ConditionalRadiosQuestion(
                    "Yes",
                    Field("replica_description", css_class="input-force-default-width"),
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
        if not is_replica:
            cleaned_data["replica_description"] = ""

        return cleaned_data


class FirearmRFDValidityForm(BaseForm):
    class Layout:
        TITLE = "Is your registered firearms dealer certificate still valid?"

    is_rfd_certificate_valid = forms.TypedChoiceField(
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
            "is_rfd_certificate_valid",
        )


class FirearmRegisteredFirearmsDealerForm(BaseForm):
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


class FirearmAttachRFDCertificate(BaseForm):
    class Layout:
        TITLE = "Upload a registered firearms dealer certificate"

    file = forms.FileField(
        label="Upload a DOCX, DOC, PDF or PNG file.",
        error_messages={
            "required": "Select a registered firearms dealer certificate",
        },
        widget=PotentiallyUnsafeClearableFileInput,
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
            "invalid": "Expiry date must be a real date",
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


class FirearmFirearmAct1968Form(BaseForm):
    class Layout:
        TITLE = "Which section of the Firearms Act 1968 is the product covered by?"

    class SectionChoices(models.TextChoices):
        SECTION_1 = FirearmsActSections.SECTION_1, "Section 1"
        SECTION_2 = FirearmsActSections.SECTION_2, "Section 2"
        SECTION_5 = FirearmsActSections.SECTION_5, "Section 5"
        DONT_KNOW = "dont_know", "Don't know"

    firearms_act_section = forms.ChoiceField(
        choices=SectionChoices.choices,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select which section of the Firearms Act 1968 the is product covered by",
        },
    )

    not_covered_explanation = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}),
        label="Explain",
        required=False,
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "firearms_act_section",
                self.SectionChoices.SECTION_1.label,
                self.SectionChoices.SECTION_2.label,
                self.SectionChoices.SECTION_5.label,
                ConditionalRadiosQuestion(
                    self.SectionChoices.DONT_KNOW.label,
                    "not_covered_explanation",
                ),
            ),
            HTML.details(
                "More information about the Firearms Act 1968",
                render_to_string("goods/forms/firearms/firearms_act_1968_information.html"),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        firearms_act_section = cleaned_data.get("firearms_act_section")
        not_covered_explanation = cleaned_data.get("not_covered_explanation")
        if firearms_act_section == self.SectionChoices.DONT_KNOW and not not_covered_explanation:
            self.add_error("not_covered_explanation", "Explain why you don't know")

        return cleaned_data


class BaseAttachFirearmActCertificateForm(BaseForm):
    file_type = None

    class Layout:
        pass

    file = forms.FileField(
        label="",
        required=False,
        widget=PotentiallyUnsafeClearableFileInput(
            force_required=True,
        ),
    )

    section_certificate_number = forms.CharField(
        label="Certificate number",
        required=False,
    )

    section_certificate_date_of_expiry = CustomErrorDateInputField(
        label="Expiry date",
        require_all_fields=False,
        help_text="For example, 30 9 2024",
        required=False,
        error_messages={
            "required": "Enter the expiry date",
            "incomplete": "Enter the expiry date",
            "invalid": "Expiry date must be a real date",
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

    section_certificate_missing = forms.BooleanField(
        required=False,
    )

    section_certificate_missing_reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": "5"}),
    )

    def __init__(self, *args, **kwargs):
        self.Layout.TITLE = f"Upload your {self.file_type}"

        super().__init__(*args, **kwargs)

        self.fields["section_certificate_missing"].label = f"I do not have a {self.file_type}"
        self.fields["section_certificate_missing_reason"].label = f"Explain why you do not have a {self.file_type}"

    def get_layout_fields(self):
        return (
            "file",
            "section_certificate_number",
            "section_certificate_date_of_expiry",
            HTML.p("Or"),
            ConditionalCheckbox(
                "section_certificate_missing",
                "section_certificate_missing_reason",
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        section_certificate_missing = cleaned_data.get("section_certificate_missing")
        if not section_certificate_missing:
            file = cleaned_data.get("file")
            if not file:
                self.add_error("file", f"Select a {self.file_type}")

            section_certificate_number = cleaned_data.get("section_certificate_number")
            if not section_certificate_number:
                self.add_error("section_certificate_number", "Enter the certificate number")

            try:
                section_certificate_date_of_expiry = cleaned_data["section_certificate_date_of_expiry"]
            except KeyError:
                pass  # Some other validation has picked this up and this is why it's not in cleaned_data
            else:
                if not section_certificate_date_of_expiry:
                    self.add_error("section_certificate_date_of_expiry", "Enter the expiry date")
        else:
            section_certificate_missing_reason = cleaned_data.get("section_certificate_missing_reason")
            if not section_certificate_missing_reason:
                self.add_error(
                    "section_certificate_missing_reason",
                    f"Enter a reason why you do not have a {self.file_type}",
                )

        return cleaned_data


class FirearmAttachFirearmCertificateForm(BaseAttachFirearmActCertificateForm):
    file_type = "firearm certificate"


class FirearmAttachShotgunCertificateForm(BaseAttachFirearmActCertificateForm):
    file_type = "shotgun certificate"


class FirearmAttachSection5LetterOfAuthorityForm(BaseAttachFirearmActCertificateForm):
    file_type = "section 5 letter of authority"


class FirearmSection5Form(BaseForm):
    class Layout:
        TITLE = "Is the product covered by section 5 of the Firearms Act 1968?"

    class Section5Choices(models.TextChoices):
        YES = "yes", "Yes"
        NO = "no", "No"
        DONT_KNOW = "dont_know", "Don't know"

    is_covered_by_section_5 = forms.ChoiceField(
        choices=Section5Choices.choices,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select whether the product is covered by section 5 of the Firearms Act 1968",
        },
    )

    def get_layout_fields(self):
        return ("is_covered_by_section_5",)


class FirearmMadeBefore1938Form(BaseForm):
    class Layout:
        TITLE = "Was the product made before 1938?"

    is_made_before_1938 = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product was made before 1938",
        },
    )

    def get_layout_fields(self):
        return ("is_made_before_1938",)


class FirearmYearOfManufactureForm(BaseForm):
    class Layout:
        TITLE = "What year was it made?"

    year_of_manufacture = forms.IntegerField(
        label="For example, 1930",
        widget=forms.TextInput,
        error_messages={
            "required": "Enter the year it was made",
            "min_value": "The year it was made must be a real year",
            "max_value": "The year must be before 1938",
        },
        min_value=1000,
        max_value=1937,
    )

    def get_layout_fields(self):
        return ("year_of_manufacture",)


class FirearmIsDeactivatedForm(BaseForm):
    class Layout:
        TITLE = "Has the product been deactivated?"

    is_deactivated = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product has been deactivated",
        },
    )

    def get_layout_fields(self):
        return ("is_deactivated",)


class FirearmDeactivationDetailsForm(BaseForm):
    class Layout:
        TITLE = "Has the product been deactivated?"

    date_of_deactivation = CustomErrorDateInputField(
        label="When was the item deactivated?",
        require_all_fields=False,
        help_text="For example, 12 11 2007",
        error_messages={
            "required": "Enter the deactivation date",
            "incomplete": "Enter the deactivation date",
            "invalid": "Deactivation date must be a real date",
            "day": {
                "incomplete": "Deactivation date must include a day",
                "invalid": "Deactivation date must be a real date",
            },
            "month": {
                "incomplete": "Deactivation date must include a month",
                "invalid": "Deactivation date must be a real date",
            },
            "year": {
                "incomplete": "Deactivation date must include a year",
                "invalid": "Deactivation date must be a real date",
            },
        },
        validators=[
            PastDateValidator("Deactivation date must be in the past"),
        ],
    )
    is_deactivated_to_standard = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="Has the item been deactivated to UK proof house standards?",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product has been deactivated to UK proof house standards",
        },
    )
    not_deactivated_to_standard_comments = forms.CharField(
        widget=forms.Textarea,
        label="Describe who deactivated the product and to what standard it was done",
        required=False,
    )

    def get_layout_fields(self):
        return (
            "date_of_deactivation",
            ConditionalRadios(
                "is_deactivated_to_standard",
                "Yes",
                ConditionalRadiosQuestion("No", "not_deactivated_to_standard_comments"),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        is_deactivated_to_standard = cleaned_data.get("is_deactivated_to_standard")
        not_deactivated_to_standard_comments = cleaned_data.get("not_deactivated_to_standard_comments")

        if not is_deactivated_to_standard and not not_deactivated_to_standard_comments:
            self.add_error(
                "not_deactivated_to_standard_comments",
                "Enter who deactivated the product and to what standard it was done",
            )

        if cleaned_data.get("is_deactivated_to_standard"):
            cleaned_data["not_deactivated_to_standard_comments"] = ""

        return cleaned_data


class FirearmSerialIdentificationMarkingsForm(BaseForm):
    class Layout:
        TITLE = "Will each product have a serial number or other identification marking?"

    serial_numbers_available = forms.ChoiceField(
        choices=SerialChoices.choices,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select if each product will have a serial number",
        },
    )

    no_identification_markings_details = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Explain why the product has not been marked",
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "serial_numbers_available",
                SerialChoices.AVAILABLE.label,
                ConditionalRadiosQuestion(
                    SerialChoices.LATER.label,
                    HTML.p(
                        "You must submit the serial numbers before you can export the products.<br/><br/>"
                        "You can check your application progress, view issued licences and add serial numbers from your dashboard."
                    ),
                ),
                ConditionalRadiosQuestion(
                    SerialChoices.NOT_AVAILABLE.label,
                    "no_identification_markings_details",
                ),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        serial_numbers_available = cleaned_data.get("serial_numbers_available")
        no_identification_markings_details = cleaned_data.get("no_identification_markings_details")

        if (serial_numbers_available == SerialChoices.NOT_AVAILABLE) and not no_identification_markings_details:
            self.add_error("no_identification_markings_details", "Enter why products will not have serial numbers")

        if serial_numbers_available != SerialChoices.NOT_AVAILABLE:
            cleaned_data["no_identification_markings_details"] = ""

        return cleaned_data


class FirearmSerialNumbersForm(BaseForm):
    class Layout:
        TITLE = "Enter serial numbers or other identification markings"

    def __init__(self, number_of_items, *args, **kwargs):
        self.number_of_items = number_of_items
        super().__init__(*args, **kwargs)

        self.fields["serial_numbers"] = SerialNumbersField(
            number_of_items,
            label="Enter one serial number for every row",
            required=False,
        )

    def get_layout_fields(self):
        return (
            HTML.p(f"{self.number_of_items} item" + "s" if self.number_of_items > 1 else ""),
            "serial_numbers",
        )

    def clean(self):
        cleaned_data = super().clean()
        try:
            serial_numbers = cleaned_data.pop("serial_numbers")
        except KeyError:
            return cleaned_data

        for i, serial_number in enumerate(serial_numbers):
            cleaned_data[f"serial_number_input_{i}"] = serial_number

        return cleaned_data


class FirearmRFDInvalidForm(BaseForm):
    class Layout:
        TITLE = "You must be registered as a firearms dealer"

    def get_layout_fields(self):
        return (HTML(render_to_string("goods/forms/firearms/rfd_invalid.html")),)

    def get_layout_actions(self):
        return [
            HTML.p(f'<a class="govuk-button" href="{reverse("core:home")}">Exit application</a>'),
        ]
