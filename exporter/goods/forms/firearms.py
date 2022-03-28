from crispy_forms_gds.choices import Choice
from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, HTML, Layout, Submit

from datetime import date
from django import forms
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse

from core.forms.layouts import ConditionalQuestion, ConditionalRadios
from exporter.core.services import get_control_list_entries, get_pv_gradings_v2


def coerce_str_to_bool(val):
    return val == "True"


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


class FirearmPvGradingForm(forms.Form):
    class Layout:
        TITLE = "Does the product have a government security grading or classification?"
        SUBMIT_BUTTON = "Continue"

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
            HTML.p("For example, UK Official or NATO Restricted."),
            "is_pv_graded",
            HTML.details(
                "Help with security gradings",
                render_to_string("goods/forms/firearms/help_with_security_gradings.html"),
            ),
            Submit("submit", self.Layout.SUBMIT_BUTTON),
        )


def decompose_date(field_name, field_data, joiner=""):
    decomposed_data = {}

    decomposed_data[field_name] = field_data.strftime("%Y-%m-%d")
    decomposed_data[f"{field_name}{joiner}day"] = str(field_data.day)
    decomposed_data[f"{field_name}{joiner}month"] = str(field_data.month)
    decomposed_data[f"{field_name}{joiner}year"] = str(field_data.year)

    return decomposed_data


class FirearmPvGradingDetailsForm(forms.Form):
    class Layout:
        TITLE = "What is the security grading or classification?"
        SUBMIT_BUTTON = "Continue"

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

    date_of_issue = DateInputField(
        label="Date of issue",
        require_all_fields=False,
        help_text="For example, 20 02 2020",
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        gradings = [(key, display) for grading in get_pv_gradings_v2(request) for key, display in grading.items()]
        self.fields["grading"].choices += gradings

        date_of_issue = self.fields["date_of_issue"]
        date_of_issue.error_messages = {"required": "Enter the date of issue"}
        for field in date_of_issue.fields:
            field.error_messages = {"incomplete": f"Date of issue must include a {field.label.lower()}"}

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
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
            Submit("submit", self.Layout.SUBMIT_BUTTON),
        )

    def clean_date_of_issue(self):
        date_of_issue = self.cleaned_data["date_of_issue"]
        if date_of_issue > date.today():
            raise forms.ValidationError("Date of issue must be in the past")

        return date_of_issue


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


class FirearmReplicaForm(forms.Form):
    class Layout:
        TITLE = "Is the product a replica firearm?"
        SUBMIT_BUTTON = "Continue"

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
            ConditionalRadios(
                "is_replica",
                ConditionalQuestion(
                    "Yes",
                    "replica_description",
                ),
                "No",
            ),
            Submit("submit", self.Layout.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()

        is_replica = cleaned_data.get("is_replica")
        replica_description = cleaned_data.get("replica_description")

        if is_replica and not replica_description:
            self.add_error("replica_description", "Enter a description")

        return cleaned_data


class FirearmRFDValidityForm(forms.Form):
    class Layout:
        TITLE = "Is your registered firearms dealer certificate still valid?"
        SUBMIT_BUTTON = "Continue"

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
        super().__init__(*args, **kwargs)

        rfd_certificate_download_url = reverse(
            "organisation:document",
            kwargs={
                "pk": rfd_certificate["id"],
            },
        )
        rfd_certificate_name = rfd_certificate["document"]["name"]

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
            HTML.p(
                render_to_string(
                    "goods/forms/firearms/rfd_certificate_download_link.html",
                    {
                        "url": rfd_certificate_download_url,
                        "name": rfd_certificate_name,
                    },
                ),
            ),
            "is_rfd_valid",
            Submit("submit", self.Layout.SUBMIT_BUTTON),
        )


class FirearmRegisteredFirearmsDealerForm(forms.Form):
    class Layout:
        TITLE = "Are you a registered firearms dealer?"
        SUBMIT_BUTTON = "Continue"

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.Layout.TITLE),
            "is_registered_firearm_dealer",
            Submit("submit", self.Layout.SUBMIT_BUTTON),
        )
