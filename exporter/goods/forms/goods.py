from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Field, Fieldset, Layout, Submit

from django import forms
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.db import models

from core.builtins.custom_tags import default_na, linkify
from core.constants import ComponentAccessoryChoices, ProductCategories
from core.forms.layouts import ConditionalRadiosQuestion, ConditionalRadios, summary_list
from core.forms.utils import coerce_str_to_bool

from core.common.forms import TextChoice
from exporter.core.constants import (
    ProductSecurityFeatures,
    ProductDeclaredAtCustoms,
    FIREARM_AMMUNITION_COMPONENT_TYPES,
    FileUploadFileTypes,
)
from exporter.core.helpers import convert_control_list_entries, str_to_bool, convert_control_list_entries_to_options
from exporter.core.services import get_control_list_entries, get_pv_gradings, get_units
from exporter.goods.helpers import get_category_display_string, good_summary
from core.common.forms import BaseForm
from lite_content.lite_exporter_frontend.goods import (
    AddGoodToApplicationForm,
    AttachDocumentForm,
    CreateGoodForm,
    DocumentAvailabilityForm,
    DocumentSensitivityForm,
    EditGoodForm,
    GoodGradingForm,
)
from lite_forms.common import control_list_entries_question
from lite_forms.components import (
    BackLink,
    Button,
    Checkboxes,
    Custom,
    DateInput,
    FileUpload,
    Form,
    Group,
    Heading,
    HiddenField,
    Label,
    Option,
    RadioButtons,
    Select,
    TextArea,
    TextInput,
)
from lite_forms.helpers import convert_to_markdown
from lite_forms.styles import ButtonStyle, HeadingStyle


def edit_grading_form(request, good_id):
    return Form(
        title=CreateGoodForm.IsGraded.TITLE,
        description="",
        questions=[
            RadioButtons(
                name="is_pv_graded",
                options=[
                    Option(key="yes", value=CreateGoodForm.IsGraded.YES, components=pv_details_form(request).questions),
                    Option(key="no", value=CreateGoodForm.IsGraded.NO),
                ],
            )
        ],
        back_link=BackLink(CreateGoodForm.BACK_BUTTON, reverse_lazy("goods:good", kwargs={"pk": good_id})),
    )


def pv_details_form(request):
    return Form(
        title=GoodGradingForm.TITLE,
        description=GoodGradingForm.DESCRIPTION,
        questions=[
            Heading("PV grading", HeadingStyle.M),
            Group(
                id="pv-gradings-group",
                components=[
                    TextInput(title=GoodGradingForm.PREFIX, name="prefix", optional=True),
                    Select(
                        options=get_pv_gradings(request, convert_to_options=True),
                        title=GoodGradingForm.GRADING,
                        name="grading",
                        optional=True,
                    ),
                    TextInput(title=GoodGradingForm.SUFFIX, name="suffix", optional=True),
                ],
                classes=["app-pv-grading-inputs"],
            ),
            TextInput(title=GoodGradingForm.OTHER_GRADING, name="custom_grading", optional=True),
            TextInput(title=GoodGradingForm.ISSUING_AUTHORITY, name="issuing_authority"),
            TextInput(title=GoodGradingForm.REFERENCE, name="reference"),
            DateInput(
                title=GoodGradingForm.DATE_OF_ISSUE, prefix="date_of_issue", name="date_of_issue", optional=False
            ),
        ],
        default_button_name=GoodGradingForm.BUTTON,
    )


def edit_good_detail_form(request, good_id):
    return Form(
        title=EditGoodForm.TITLE,
        description=EditGoodForm.DESCRIPTION,
        questions=[
            TextInput(
                title="Name",
                description=("Give your product a name so it is easier to find in your product list"),
                name="name",
            ),
            TextArea(
                title=EditGoodForm.Description.TITLE,
                name="description",
                rows=5,
                optional=True,
                extras={"max_length": 280},
            ),
            TextInput(title=EditGoodForm.PartNumber.TITLE, name="part_number", optional=True),
            RadioButtons(
                title=EditGoodForm.IsControlled.TITLE,
                description=EditGoodForm.IsControlled.DESCRIPTION,
                name="is_good_controlled",
                options=[
                    Option(
                        key=True,
                        value=EditGoodForm.IsControlled.YES,
                        components=[
                            control_list_entries_question(
                                control_list_entries=convert_control_list_entries_to_options(
                                    get_control_list_entries(request)
                                ),
                                title=EditGoodForm.ControlListEntry.TITLE,
                                description=EditGoodForm.ControlListEntry.DESCRIPTION,
                            ),
                        ],
                    ),
                    Option(key=False, value=EditGoodForm.IsControlled.NO),
                ],
            ),
        ],
        back_link=BackLink(CreateGoodForm.BACK_BUTTON, reverse_lazy("goods:good", kwargs={"pk": good_id})),
    )


def check_document_available_form(back_url):
    return Form(
        title=DocumentAvailabilityForm.TITLE,
        description=DocumentAvailabilityForm.DESCRIPTION,
        questions=[
            RadioButtons(
                name="is_document_available",
                options=[
                    Option(key="yes", value=DocumentSensitivityForm.Options.YES),
                    Option(
                        key="no",
                        value=DocumentSensitivityForm.Options.NO,
                        components=[
                            TextArea(
                                title=DocumentAvailabilityForm.NO_DOCUMENT_TEXTFIELD_DESCRIPTION,
                                description=None,
                                name="no_document_comments",
                                optional=False,
                            ),
                        ],
                    ),
                ],
            ),
        ],
        back_link=BackLink("Back", back_url),
        default_button_name=DocumentAvailabilityForm.SUBMIT_BUTTON,
    )


def document_grading_form(back_url):
    return Form(
        title=DocumentSensitivityForm.TITLE,
        questions=[
            RadioButtons(
                name="is_document_sensitive",
                options=[
                    Option(
                        key="yes",
                        value=DocumentSensitivityForm.Options.YES,
                        components=[Label(text=DocumentSensitivityForm.ECJU_HELPLINE)],
                    ),
                    Option(
                        key="no",
                        value=DocumentSensitivityForm.Options.NO,
                    ),
                ],
            ),
        ],
        back_link=BackLink("Back", back_url),
        default_button_name=DocumentSensitivityForm.SUBMIT_BUTTON,
    )


def attach_documents_form(back_link):
    return Form(
        title=AttachDocumentForm.TITLE,
        description=AttachDocumentForm.DESCRIPTION,
        questions=[
            FileUpload(),
            TextArea(
                title=AttachDocumentForm.Description.TITLE,
                optional=True,
                name="description",
                extras={"max_length": 280},
            ),
        ],
        buttons=[Button(AttachDocumentForm.BUTTON, "submit")],
        back_link=back_link,
    )


def delete_good_form(good):
    back_link = reverse("goods:good", kwargs={"pk": good["id"]})

    try:
        if good["firearm_details"] and good["firearm_details"]["type"]["key"] == "firearms":
            back_link = reverse("goods:firearm_detail", kwargs={"pk": good["id"]})
        elif good["item_category"]["key"] == ProductCategories.PRODUCT_CATEGORY_COMPLETE_ITEM:
            back_link = reverse("goods:complete_item_detail", kwargs={"pk": good["id"]})
    except KeyError:
        pass

    return Form(
        title=EditGoodForm.DeleteConfirmationForm.TITLE,
        questions=[good_summary(good)],
        buttons=[
            Button(value=EditGoodForm.DeleteConfirmationForm.YES, action="submit", style=ButtonStyle.WARNING),
            Button(
                value=EditGoodForm.DeleteConfirmationForm.NO,
                action="",
                style=ButtonStyle.SECONDARY,
                link=back_link,
            ),
        ],
    )


def format_list_item(link, name, description):
    return (
        "<br>"
        + "<li>"
        + linkify(
            link,
            name=name,
        )
        + f"&nbsp;&nbsp;{description}"
        + "</li>"
    )


def upload_firearms_act_certificate_form(section, filename, back_link):
    return Form(
        title=f"Attach your Firearms Act 1968 {section} certificate",
        description=FileUploadFileTypes.UPLOAD_GUIDANCE_TEXT + "\n\nThe file must be smaller than 50MB.",
        questions=[
            HiddenField("firearms_certificate_uploaded", False),
            FileUpload(),
            HiddenField("uploaded_file_name", filename),
            TextInput(
                title=CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_CERTIFICATE_NUMBER,
                description="",
                name="section_certificate_number",
                optional=False,
            ),
            DateInput(
                title="Expiry date",
                description="For example, 12 11 2022",
                prefix="section_certificate_date_of_expiry",
                name="section_certificate_date_of_expiry",
            ),
            Label(text="Or"),
            Checkboxes(
                name="section_certificate_missing",
                options=[
                    Option(
                        key="True",
                        value=f"I do not have a Firearms Act 1968 {section} certificate",
                    )
                ],
            ),
            TextArea(
                title="Provide a reason why you do not have a certificate",
                name="section_certificate_missing_reason",
                optional=False,
            ),
        ],
        back_link=back_link,
        buttons=[Button("Save and continue", "submit")],
    )


def build_firearm_back_link_create(form_url, form_data):
    return Custom(
        data={
            **form_data,
            "form_pk": int(form_data["form_pk"]) + 1,
            "form_url": form_url,
        },
        template="applications/firearm_upload_back_link.html",
    )


def build_firearm_create_back(back_link):
    return BackLink("Back", back_link)


def has_valid_section_five_certificate(application):
    documents = {item["document_type"]: item for item in application.get("organisation", {}).get("documents", [])}
    if "section-five-certificate" in documents:
        return not documents["section-five-certificate"]["is_expired"]
    return False


class GroupTwoProductTypeForm(forms.Form):
    title = CreateGoodForm.FirearmGood.ProductType.TITLE

    type = forms.TypedChoiceField(
        choices=(
            ("firearms", CreateGoodForm.FirearmGood.ProductType.FIREARM),
            ("ammunition", CreateGoodForm.FirearmGood.ProductType.AMMUNITION),
            ("components_for_firearms", CreateGoodForm.FirearmGood.ProductType.COMPONENTS_FOR_FIREARM),
            ("components_for_ammunition", CreateGoodForm.FirearmGood.ProductType.COMPONENTS_FOR_AMMUNITION),
            ("firearms_accessory", CreateGoodForm.FirearmGood.ProductType.FIREARMS_ACCESSORY),
            ("software_related_to_firearms", CreateGoodForm.FirearmGood.ProductType.SOFTWARE_RELATED_TO_FIREARM),
            ("technology_related_to_firearms", CreateGoodForm.FirearmGood.ProductType.TECHNOLOGY_RELATED_TO_FIREARM),
        ),
        error_messages={
            "required": "Select the type of product",
        },
        widget=forms.RadioSelect,
        label="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "type",
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["product_type_step"] = True
        return cleaned_data


class FirearmsNumberOfItemsForm(forms.Form):
    title = "Number of items"

    number_of_items = forms.IntegerField(
        error_messages={
            "required": "Enter the number of items",
        },
        widget=forms.TextInput,
        label="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "number_of_items",
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["number_of_items_step"] = True
        return cleaned_data


class IdentificationMarkingsForm(forms.Form):
    title = CreateGoodForm.FirearmGood.IdentificationMarkings.TITLE

    serial_numbers_available = forms.ChoiceField(
        choices=(
            ("AVAILABLE", CreateGoodForm.FirearmGood.IdentificationMarkings.YES_NOW),
            ("LATER", CreateGoodForm.FirearmGood.IdentificationMarkings.YES_LATER),
            ("NOT_AVAILABLE", CreateGoodForm.FirearmGood.IdentificationMarkings.NO),
        ),
        error_messages={
            "required": "Select whether you can enter serial numbers now, later or if the product does not have them",
        },
        label="",
    )
    no_identification_markings_details = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label=CreateGoodForm.FirearmGood.IdentificationMarkings.NO_MARKINGS_DETAILS,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            ConditionalRadios(
                "serial_numbers_available",
                CreateGoodForm.FirearmGood.IdentificationMarkings.YES_NOW,
                CreateGoodForm.FirearmGood.IdentificationMarkings.YES_LATER,
                ConditionalRadiosQuestion(
                    CreateGoodForm.FirearmGood.IdentificationMarkings.NO,
                    "no_identification_markings_details",
                ),
            ),
            Submit("submit", CreateGoodForm.FirearmGood.IdentificationMarkings.BUTTON_TEXT),
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["identification_markings_step"] = True

        if cleaned_data.get("serial_numbers_available") == "NOT_AVAILABLE":
            if not cleaned_data.get("no_identification_markings_details"):
                self.add_error(
                    "no_identification_markings_details",
                    "Enter a reason why the product has not been marked",
                )

        return cleaned_data


class SerialNumbersWidget(forms.MultiWidget):
    template_name = "forms/widgets/serial_numbers.html"

    def __init__(self, number_of_inputs, **kwargs):
        widgets = [forms.TextInput() for i in range(number_of_inputs)]

        super().__init__(widgets, **kwargs)

    def decompress(self, value):
        if value:
            return value
        return []


class SerialNumbersField(forms.MultiValueField):
    def __init__(self, number_of_inputs, **kwargs):
        error_messages = {}

        fields = [forms.CharField(label=f"Serial number {i + 1}") for i in range(number_of_inputs)]

        self.widget = SerialNumbersWidget(number_of_inputs)

        super().__init__(error_messages=error_messages, fields=fields, require_all_fields=False, **kwargs)

    def clean(self, value):
        if not any(val.strip() for val in value if val):
            raise forms.ValidationError("Enter at least one serial number")
        return value

    def compress(self, data_list):
        return data_list


class BaseSerialNumbersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        number_of_items = kwargs.pop("number_of_items")

        super().__init__(*args, **kwargs)

        self.fields["serial_numbers"] = SerialNumbersField(
            number_of_items,
            label="",
            required=False,
        )

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML.p("Enter at least one serial number."),
            HTML.p(f"{number_of_items} items"),
            "serial_numbers",
            Submit("submit", self.save_button_text),
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


class FirearmsCaptureSerialNumbersForm(BaseSerialNumbersForm):
    title = "Enter the serial numbers for this product"
    save_button_text = "Save and continue"

    def clean(self):
        cleaned_data = super().clean()

        cleaned_data["capture_serial_numbers_step"] = True

        return cleaned_data


class UpdateSerialNumbersForm(BaseSerialNumbersForm):
    save_button_text = "Submit"

    def __init__(self, *args, **kwargs):
        self.product_name = kwargs.pop("product_name")

        super().__init__(*args, **kwargs)

    @property
    def title(self):
        return f"Enter the serial numbers for '{self.product_name}'"


class ProductMilitaryUseForm(forms.Form):
    title = CreateGoodForm.MilitaryUse.TITLE

    is_military_use = forms.ChoiceField(
        choices=(
            ("yes_designed", CreateGoodForm.MilitaryUse.YES_DESIGNED),
            ("yes_modified", CreateGoodForm.MilitaryUse.YES_MODIFIED),
            ("no", CreateGoodForm.MilitaryUse.NO),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select no if the product is not for military use",
        },
    )

    modified_military_use_details = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label=CreateGoodForm.MilitaryUse.MODIFIED_MILITARY_USE_DETAILS,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            ConditionalRadios(
                "is_military_use",
                CreateGoodForm.MilitaryUse.YES_DESIGNED,
                ConditionalRadiosQuestion(
                    CreateGoodForm.MilitaryUse.YES_MODIFIED,
                    "modified_military_use_details",
                ),
                CreateGoodForm.MilitaryUse.NO,
            ),
            Submit("submit", "Save"),
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("is_military_use") == "yes_modified" and not cleaned_data.get(
            "modified_military_use_details"
        ):
            self.add_error("modified_military_use_details", "Enter the details of the modifications")


class ProductUsesInformationSecurityForm(forms.Form):
    title = CreateGoodForm.ProductInformationSecurity.TITLE

    uses_information_security = forms.ChoiceField(
        choices=(
            (True, "Yes"),
            (False, CreateGoodForm.ProductInformationSecurity.NO),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product is designed to employ information security features",
        },
    )

    information_security_details = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label=f"{CreateGoodForm.ProductInformationSecurity.INFORMATION_SECURITY_DETAILS} (optional)",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            ConditionalRadios(
                "uses_information_security",
                ConditionalRadiosQuestion(
                    "Yes",
                    "information_security_details",
                ),
                CreateGoodForm.ProductInformationSecurity.NO,
            ),
            Submit("submit", "Save"),
        )


class IsFirearmForm(BaseForm):
    class Layout:
        TITLE = "Is it a firearm product?"

    is_firearm_product = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label="Select whether it is a firearm product. This includes components, accessories, software and technology relating to firearms.",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes to add a firearm product",
        },
    )

    def get_layout_fields(self):
        return ("is_firearm_product",)


class NonFirearmCategoryForm(BaseForm):
    class Layout:
        TITLE = "Select the product category"

    class NonFirearmCategoryChoices(models.TextChoices):
        COMPLETE_ITEM = "COMPLETE_ITEM", "It's a complete product"
        MATERIAL_CATEGORY = "MATERIAL_CATEGORY", "It forms part of a product"
        TECHNOLOGY = "TECHNOLOGY", "It helps to operate a product"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        category_choices = [
            TextChoice(
                self.NonFirearmCategoryChoices.COMPLETE_ITEM,
                hint="Hardware such as devices, systems, platforms, vehicles, equipment.",
            ),
            TextChoice(
                self.NonFirearmCategoryChoices.MATERIAL_CATEGORY,
                hint="Hardware such as components and accessories, or raw materials and substances.",
            ),
            TextChoice(
                self.NonFirearmCategoryChoices.TECHNOLOGY,
                hint="For example, software or information such as technology manuals and specifications.",
            ),
        ]

        self.fields["no_firearm_category"].choices = category_choices

    no_firearm_category = forms.ChoiceField(
        choices=[],  # updated in init
        widget=forms.RadioSelect,
        label="",
        error_messages={
            "required": "Select the product category",
        },
    )

    def get_layout_fields(self):
        return ("no_firearm_category",)


class IsMaterialSubstanceCategoryForm(BaseForm):
    class Layout:
        TITLE = "Is it a material or substance?"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        material_substance_choices = [(True, "Yes"), (False, "No, it's a component, accessory or module")]
        self.fields["is_material_substance"].choices = material_substance_choices

    is_material_substance = forms.TypedChoiceField(
        choices=[],  # updated in init
        coerce=coerce_str_to_bool,
        widget=forms.RadioSelect,
        label="",
        error_messages={
            "required": "Select yes if the product is a material or substance",
        },
    )

    def get_layout_fields(self):
        return ("is_material_substance",)


class ProductSecurityFeaturesForm(BaseForm):
    class Layout:
        TITLE = ProductSecurityFeatures.TITLE

    has_security_features = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        coerce=coerce_str_to_bool,
        label=ProductSecurityFeatures.HAS_SECURITY_FEATURES,
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product include security features to protect information",
        },
    )

    security_feature_details = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label=ProductSecurityFeatures.SECURITY_FEATURE_DETAILS,
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "has_security_features",
                ConditionalRadiosQuestion(
                    "Yes",
                    "security_feature_details",
                ),
                ProductSecurityFeatures.NO,
            ),
            HTML.details(
                "Help with security features",
                f'<p class="govuk-body">{ProductSecurityFeatures.HELP_TEXT}</p>',
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        details = cleaned_data.get("security_feature_details")
        if cleaned_data.get("has_security_features") is True and details == "":
            self.add_error(
                "security_feature_details",
                "Enter the details of security features",
            )

        if cleaned_data.get("security_feature_details") is False:
            cleaned_data["security_feature_details"] = ""

        return cleaned_data


class ProductDeclaredAtCustomsForm(BaseForm):
    class Layout:
        TITLE = ProductDeclaredAtCustoms.TITLE

    HAS_DECLARED_AT_CUSTOMS_CHOICES = (
        (True, "Yes"),
        (False, ProductDeclaredAtCustoms.NO),
    )

    has_declared_at_customs = forms.TypedChoiceField(
        choices=HAS_DECLARED_AT_CUSTOMS_CHOICES,
        label="",
        coerce=coerce_str_to_bool,
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product will be declared at customs",
        },
    )

    def get_layout_fields(self):
        return (
            "has_declared_at_customs",
            HTML.details(
                "Help with export declarations",
                render_to_string("goods/forms/common/help_with_export_declarations.html"),
            ),
        )


class AddGoodsQuestionsForm(forms.Form):
    name = forms.CharField(
        help_text="Give your product a name so it is easier to find in your product list",
        error_messages={
            "required": "Enter a product name",
        },
        required=True,
    )

    description = forms.CharField(required=False, label="Description (optional)", widget=forms.Textarea)

    part_number = forms.CharField(required=False, label="Part number (optional)")

    is_good_controlled = forms.ChoiceField(
        choices=(
            (True, CreateGoodForm.IsControlled.YES),
            (False, CreateGoodForm.IsControlled.NO),
        ),
        label=CreateGoodForm.IsControlled.TITLE,
        help_text=convert_to_markdown(CreateGoodForm.IsControlled.DESCRIPTION),
    )

    control_list_entries = forms.MultipleChoiceField(
        help_text="Type to get suggestions. For example ML1a.",
        choices=(),  # set in __init__
        required=False,
    )

    is_pv_graded = forms.ChoiceField(
        choices=(
            ("yes", CreateGoodForm.IsGraded.YES),
            ("no", CreateGoodForm.IsGraded.NO),
        ),
        label=CreateGoodForm.IsGraded.TITLE,
        help_text=CreateGoodForm.IsGraded.DESCRIPTION,
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select an option",
        },
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        application_pk = kwargs.pop("application_pk")
        super().__init__(*args, **kwargs)

        if application_pk is not None:
            self.title = CreateGoodForm.TITLE_APPLICATION
        else:
            self.title = CreateGoodForm.TITLE_GOODS_LIST

        try:
            clc_list = request.session["clc_list"]
        except KeyError:
            clc_list = get_control_list_entries(request)
            request.session["clc_list"] = clc_list

        self.fields["control_list_entries"].choices = [(entry["rating"], entry["rating"]) for entry in clc_list]

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "name",
            Field.textarea(
                "description",
                aria_describedby="",  # Required as there's a bug in gds crispy forms if this isn't set and you set max_characters
                max_characters=280,
                rows=5,
            ),
            "part_number",
            ConditionalRadios(
                "is_good_controlled",
                ConditionalRadiosQuestion(
                    CreateGoodForm.IsControlled.YES,
                    Field(
                        "control_list_entries",
                        data_module="multi-select",
                        data_multi_select_objects_as_plural="control list entries",
                    ),
                ),
                CreateGoodForm.IsControlled.NO,
            ),
            "is_pv_graded",
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()
        if not str_to_bool(cleaned_data.get("is_good_controlled")):
            cleaned_data.pop("control_list_entries", None)
        return cleaned_data


def decompose_date(field_name, field_data, joiner=""):
    decomposed_data = {}

    decomposed_data[field_name] = field_data.strftime("%Y-%m-%d")
    decomposed_data[f"{field_name}{joiner}day"] = str(field_data.day)
    decomposed_data[f"{field_name}{joiner}month"] = str(field_data.month)
    decomposed_data[f"{field_name}{joiner}year"] = str(field_data.year)

    return decomposed_data


class PvDetailsForm(forms.Form):
    title = GoodGradingForm.TITLE

    prefix = forms.CharField(required=False, label=f"{GoodGradingForm.PREFIX} (optional)")

    grading = forms.ChoiceField(required=False, label=GoodGradingForm.GRADING, choices=[("", "Select")])

    suffix = forms.CharField(required=False, label=f"{GoodGradingForm.SUFFIX} (optional)")

    custom_grading = forms.CharField(required=False, label=f"{GoodGradingForm.OTHER_GRADING} (optional)")

    issuing_authority = forms.CharField(
        label=GoodGradingForm.ISSUING_AUTHORITY,
        error_messages={
            "required": "This field may not be blank",
        },
    )

    reference = forms.CharField(
        label=GoodGradingForm.REFERENCE,
        error_messages={
            "required": "This field may not be blank",
        },
    )

    date_of_issue = DateInputField(label=GoodGradingForm.DATE_OF_ISSUE)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        gradings = [(key, display) for grading in get_pv_gradings(request) for key, display in grading.items()]
        self.fields["grading"].choices += gradings

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML.h3("PV grading"),
            Fieldset(
                Field.text("prefix"), Field.text("grading"), Field.text("suffix"), css_class="app-pv-grading-inputs"
            ),
            "custom_grading",
            "issuing_authority",
            "reference",
            "date_of_issue",
            Submit("submit", "Save and continue"),
        )

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get("grading") and not cleaned_data.get("custom_grading"):
            self.add_error("custom_grading", "Enter the grading if it's not listed in the dropdown list")
        elif cleaned_data.get("grading") and cleaned_data.get("custom_grading"):
            self.add_error(
                "custom_grading",
                "Check if this grading or the grading selected on the dropdown list is the correct one for the product",
            )

        date_of_issue = cleaned_data.get("date_of_issue")
        if date_of_issue:
            cleaned_data.update(decompose_date("date_of_issue", date_of_issue))

        return cleaned_data


class FirearmsYearOfManufactureDetailsForm(forms.Form):
    title = "What is the year of manufacture of the firearm?"

    year_of_manufacture = forms.CharField(label="", error_messages={"required": "Enter the year of manufacture"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "year_of_manufacture",
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["firearm_year_of_manufacture_step"] = True

        try:
            year_of_manufacture = int(cleaned_data["year_of_manufacture"])
        except KeyError:
            return cleaned_data
        except ValueError:
            year_of_manufacture = 0

        if year_of_manufacture <= 0:
            self.add_error("year_of_manufacture", "Year of manufacture must be valid")

        if year_of_manufacture > timezone.now().date().year:
            self.add_error("year_of_manufacture", "Year of manufacture must be in the past")

        return cleaned_data


class FirearmsReplicaForm(forms.Form):
    title = CreateGoodForm.FirearmGood.FirearmsReplica.TITLE

    is_replica = forms.ChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product is a replica firearm",
        },
    )

    replica_description = forms.CharField(
        widget=forms.Textarea,
        label=CreateGoodForm.FirearmGood.FirearmsReplica.DESCRIPTION,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            ConditionalRadios(
                "is_replica",
                ConditionalRadiosQuestion(
                    "Yes",
                    "replica_description",
                ),
                "No",
            ),
            Submit("submit", "Save and continue"),
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["is_replica_step"] = True

        if str_to_bool(cleaned_data.get("is_replica")) and not cleaned_data.get("replica_description"):
            self.add_error("replica_description", "Enter a description")

        return cleaned_data


class FirearmsCalibreDetailsForm(forms.Form):
    title = "What is the calibre of the product?"

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
            HTML.h1(self.title),
            "calibre",
            Submit("submit", "Save and continue"),
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["firearm_calibre_step"] = True
        return cleaned_data


class RegisteredFirearmsDealerForm(forms.Form):
    title = "Are you a registered firearms dealer?"

    is_registered_firearm_dealer = forms.ChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
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
            HTML.h1(self.title),
            "is_registered_firearm_dealer",
            Submit("submit", "Save and continue"),
        )


class AttachFirearmsDealerCertificateForm(forms.Form):
    title = "Attach your registered firearms dealer certificate"

    file = forms.FileField(
        label=FileUploadFileTypes.UPLOAD_GUIDANCE_TEXT,
        help_text="The file must be smaller than 50MB",
        error_messages={
            "required": "Select certificate file to upload",
        },
    )

    reference_code = forms.CharField(
        label="Certificate number",
        error_messages={
            "required": "Enter the certificate number",
        },
    )

    expiry_date = DateInputField(
        label="Expiry date",
        help_text="For example 12 3 2022",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "file",
            "reference_code",
            "expiry_date",
            Submit("submit", "Save"),
        )

    def clean(self):
        cleaned_data = super().clean()

        expiry_date = cleaned_data.pop("expiry_date", None)

        if expiry_date:
            if expiry_date < timezone.now().date():
                self.add_error("expiry_date", "Expiry date must be in the future")
            else:
                cleaned_data.update(decompose_date("expiry_date", expiry_date, joiner="_"))

        return cleaned_data


class FirearmsActConfirmationForm(forms.Form):
    class Layout:
        RFD_FORM_TITLE = "Is the product covered by section 5 of the Firearms Act 1968?"
        NON_RFD_FORM_TITLE = CreateGoodForm.FirearmGood.FirearmsActCertificate.TITLE

    is_covered_by_firearm_act_section_one_two_or_five = forms.ChoiceField(
        choices=(
            ("Yes", CreateGoodForm.FirearmGood.FirearmsActCertificate.YES),
            ("No", CreateGoodForm.FirearmGood.FirearmsActCertificate.NO),
            ("Unsure", CreateGoodForm.FirearmGood.FirearmsActCertificate.DONT_KNOW),
        ),
        label="",
        widget=forms.RadioSelect,
    )

    firearms_act_section = forms.ChoiceField(
        choices=(
            ("firearms_act_section1", "Section 1"),
            ("firearms_act_section2", "Section 2"),
            ("firearms_act_section5", "Section 5"),
        ),
        label="Select section",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select which section the product is covered by",
        },
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.is_rfd = kwargs.pop("is_rfd")

        super().__init__(*args, **kwargs)

        if self.is_rfd:
            self.title = self.Layout.RFD_FORM_TITLE

            details = [
                "What does section 5 cover?",
                linkify(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE_LINK,
                    name=CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE,
                )
                + f"&nbsp;&nbsp;covers weapons and ammunition that are generally prohibited.",
            ]
        else:
            self.title = self.Layout.NON_RFD_FORM_TITLE

            details = [
                "What do these sections cover?",
                linkify(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_ONE_LINK,
                    name=CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_ONE,
                )
                + f"&nbsp;&nbsp;is a broad category covering most types of firearm and ammunition, including rifles and high powered air weapons.<br><br>"
                + linkify(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_TWO_LINK,
                    name=CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_TWO,
                )
                + f"&nbsp;&nbsp;covers most types of shotgun.<br><br>"
                + linkify(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE_LINK,
                    name=CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE,
                )
                + f"&nbsp;&nbsp;covers weapons and ammunition that are generally prohibited.",
            ]

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML.details(*details),
            (
                "is_covered_by_firearm_act_section_one_two_or_five"
                if self.is_rfd
                else ConditionalRadios(
                    "is_covered_by_firearm_act_section_one_two_or_five",
                    ConditionalRadiosQuestion(
                        CreateGoodForm.FirearmGood.FirearmsActCertificate.YES,
                        "firearms_act_section",
                    ),
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.NO,
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.DONT_KNOW,
                )
            ),
            Submit("submit", "Save and continue"),
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["section_certificate_step"] = True

        if not cleaned_data.get("is_covered_by_firearm_act_section_one_two_or_five"):
            # Remove the default error as the message depends on whether is_rfd is set
            self.errors.pop("is_covered_by_firearm_act_section_one_two_or_five", None)

            if self.is_rfd:
                self.add_error(
                    "is_covered_by_firearm_act_section_one_two_or_five",
                    "Select yes if the product covered by section 5 of the Firearms Act 1968",
                )
            else:
                self.add_error(
                    "is_covered_by_firearm_act_section_one_two_or_five",
                    "Select yes if the product is covered by Section 1, Section 2 or Section 5 of the Firearms Act 1968",
                )

        if (
            not self.is_rfd
            and cleaned_data.get("is_covered_by_firearm_act_section_one_two_or_five") == "Yes"
            and not cleaned_data.get("firearms_act_section")
        ):
            self.add_error("firearms_act_section", "Select which section the product is covered by")

        return cleaned_data


class SoftwareTechnologyDetailsForm(forms.Form):
    software_or_technology_details = forms.CharField(
        label="",
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        product_type = kwargs.pop("product_type")
        super().__init__(*args, **kwargs)

        self.category_text = get_category_display_string(product_type)
        self.title = CreateGoodForm.TechnologySoftware.TITLE + self.category_text

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "software_or_technology_details",
            Submit("submit", "Save"),
        )

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get("software_or_technology_details"):
            self.errors.clear()
            self.add_error("software_or_technology_details", f"Enter the purpose of the {self.category_text}")

        return cleaned_data


class ProductComponentForm(forms.Form):
    class Layout:
        TITLE = CreateGoodForm.ProductComponent.TITLE

    title = CreateGoodForm.ProductComponent.TITLE

    is_component = forms.ChoiceField(
        choices=(
            ("yes_designed", CreateGoodForm.ProductComponent.YES_DESIGNED),
            ("yes_modified", CreateGoodForm.ProductComponent.YES_MODIFIED),
            ("yes_general", CreateGoodForm.ProductComponent.YES_GENERAL_PURPOSE),
            ("no", CreateGoodForm.ProductComponent.NO),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select no if the product is not a component",
        },
    )

    designed_details = forms.CharField(
        label=CreateGoodForm.ProductComponent.DESIGNED_DETAILS,
        widget=forms.Textarea,
        required=False,
    )

    modified_details = forms.CharField(
        label=CreateGoodForm.ProductComponent.MODIFIED_DETAILS,
        widget=forms.Textarea,
        required=False,
    )

    general_details = forms.CharField(
        label=CreateGoodForm.ProductComponent.GENERAL_DETAILS,
        widget=forms.Textarea,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            ConditionalRadios(
                "is_component",
                ConditionalRadiosQuestion(
                    CreateGoodForm.ProductComponent.YES_DESIGNED,
                    "designed_details",
                ),
                ConditionalRadiosQuestion(
                    CreateGoodForm.ProductComponent.YES_MODIFIED,
                    "modified_details",
                ),
                ConditionalRadiosQuestion(
                    CreateGoodForm.ProductComponent.YES_GENERAL_PURPOSE,
                    "general_details",
                ),
                CreateGoodForm.ProductComponent.NO,
            ),
            Submit("submit", "Save"),
        )

    def clean(self):
        cleaned_data = super().clean()

        component_details = (
            ("yes_designed", "designed_details", "Enter the details of the hardware"),
            ("yes_modified", "modified_details", "Enter the details of the modifications and the hardware"),
            (
                "yes_general",
                "general_details",
                "Enter the details of the types of applications the component is intended to be used in",
            ),
        )

        max_chars = 2000

        for is_component, details_field, empty_field_msg in component_details:
            details = cleaned_data.get(details_field, "")

            if cleaned_data.get("is_component") == is_component and not details:
                self.add_error(details_field, empty_field_msg)

            if len(details) > max_chars:
                self.add_error(details_field, f"Ensure this field has no more than {max_chars} characters")

        return cleaned_data


def get_unit_quantity_value_summary_list_items(good, number_of_items):
    summary_list_items = [
        ("Name", good["description"] if not good["name"] else good["name"]),
        ("Control list entries", convert_control_list_entries(good["control_list_entries"])),
        ("Part number", default_na(good["part_number"])),
    ]

    if good["item_category"]["key"] == ProductCategories.PRODUCT_CATEGORY_FIREARM:
        firearm_type = good["firearm_details"]["type"]["key"]

        if firearm_type in FIREARM_AMMUNITION_COMPONENT_TYPES:
            summary_list_items.append(
                ("Number of items", str(number_of_items)),
            )

    return summary_list_items


class FirearmsUnitQuantityValueForm(forms.Form):
    title = AddGoodToApplicationForm.TITLE

    value = forms.CharField(
        error_messages={
            "required": "Enter the total value of the products",
        },
        label="Total value",
    )

    is_good_incorporated = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        error_messages={
            "required": "Select yes if the product will be incorporated into another product",
        },
        label="Will the product be incorporated into another product?",
        widget=forms.RadioSelect(),
    )

    is_deactivated = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        error_messages={
            "required": "Select yes if the product has been deactivated",
        },
        label="Has the product been deactivated?",
        widget=forms.RadioSelect(),
    )

    date_of_deactivation = DateInputField(
        label="Date of deactivation",
        required=False,
    )

    is_deactivated_to_standard = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        label="Has the product been deactivated to UK/EU proof house standards?",
        required=False,
        widget=forms.RadioSelect(),
    )

    deactivation_standard = forms.ChoiceField(
        choices=(
            ("", "Select"),
            ("UK", "UK"),
            ("EU", "EU"),
        ),
        label="Proof house standard",
        required=False,
    )

    deactivation_standard_other = forms.CharField(
        label="Describe who deactivated the product and to what standard it was done",
        widget=forms.Textarea,
        required=False,
    )

    has_proof_mark = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        error_messages={
            "required": "Select whether the product has valid UK proof marks",
        },
        label="Does the product have valid UK proof marks?",
        widget=forms.RadioSelect(),
    )

    no_proof_mark_details = forms.CharField(
        label="Please give details why not",
        widget=forms.Textarea,
        required=False,
    )

    def __init__(self, *args, good, number_of_items, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            summary_list(get_unit_quantity_value_summary_list_items(good, number_of_items)),
            Field("value", template="forms/currency_field.html"),
            Field.radios("is_good_incorporated", inline=True),
            ConditionalRadios(
                "is_deactivated",
                ConditionalRadiosQuestion(
                    "Yes",
                    "date_of_deactivation",
                    ConditionalRadios(
                        "is_deactivated_to_standard",
                        ConditionalRadiosQuestion(
                            "Yes",
                            "deactivation_standard",
                        ),
                        ConditionalRadiosQuestion(
                            "No",
                            "deactivation_standard_other",
                        ),
                    ),
                ),
                "No",
            ),
            ConditionalRadios(
                "has_proof_mark",
                "Yes",
                ConditionalRadiosQuestion(
                    "No",
                    "no_proof_mark_details",
                ),
            ),
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("is_deactivated") is True:
            if not cleaned_data["date_of_deactivation"]:
                self.add_error("date_of_deactivation", "Enter a valid date of deactivation")

            if cleaned_data["is_deactivated_to_standard"] == "":
                self.add_error(
                    "is_deactivated_to_standard",
                    "Select yes if the product has been deactivated to UK/EU proof house standards",
                )
            elif cleaned_data["is_deactivated_to_standard"] is True:
                if not cleaned_data.get("deactivation_standard"):
                    self.add_error("deactivation_standard", "Select yes if the product has valid UK proof marks")
            elif cleaned_data["is_deactivated_to_standard"] is False:
                if not cleaned_data["deactivation_standard_other"]:
                    self.add_error(
                        "deactivation_standard_other",
                        "Enter details of who deactivated the product and to what standard it was done",
                    )

        if cleaned_data.get("has_proof_mark") is False and not cleaned_data["no_proof_mark_details"]:
            self.add_error(
                "no_proof_mark_details", "Enter details of why the product does not have valid UK proof marks"
            )

        date_of_deactivation = cleaned_data.get("date_of_deactivation")
        if date_of_deactivation:
            cleaned_data.update(decompose_date("date_of_deactivation", date_of_deactivation))

        return cleaned_data


class ComponentAccessoryOfAFirearmUnitQuantityValueForm(forms.Form):
    title = AddGoodToApplicationForm.TITLE

    value = forms.CharField(
        error_messages={
            "required": "Enter the total value of the products",
        },
        label="Total value",
    )

    is_good_incorporated = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        error_messages={
            "required": "Select yes if the product will be incorporated into another product",
        },
        label="Will the product be incorporated into another product?",
        widget=forms.RadioSelect(),
    )

    is_deactivated = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        error_messages={
            "required": "Select yes if the product has been deactivated",
        },
        label="Has the product been deactivated?",
        widget=forms.RadioSelect(),
    )

    date_of_deactivation = DateInputField(
        label="Date of deactivation",
        required=False,
    )

    is_deactivated_to_standard = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        label="Has the product been deactivated to UK/EU proof house standards?",
        required=False,
        widget=forms.RadioSelect(),
    )

    deactivation_standard = forms.ChoiceField(
        choices=(
            ("", "Select"),
            ("UK", "UK"),
            ("EU", "EU"),
        ),
        label="Proof house standard",
        required=False,
    )

    deactivation_standard_other = forms.CharField(
        label="Describe who deactivated the product and to what standard it was done",
        widget=forms.Textarea,
        required=False,
    )

    is_gun_barrel = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        error_messages={
            "required": "Select whether the product is a gun barrel or the action of a gun",
        },
        label="Is the product a gun barrel or the action of a gun?",
        widget=forms.RadioSelect(),
    )

    has_proof_mark = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        error_messages={
            "required": "Select whether the product has valid UK proof marks",
        },
        label="Does the product have valid UK proof marks?",
        required=False,
        widget=forms.RadioSelect(),
    )

    no_proof_mark_details = forms.CharField(
        label="Please give details why not",
        widget=forms.Textarea,
        required=False,
    )

    def __init__(self, *args, good, number_of_items, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            summary_list(get_unit_quantity_value_summary_list_items(good, number_of_items)),
            Field("value", template="forms/currency_field.html"),
            Field.radios("is_good_incorporated", inline=True),
            ConditionalRadios(
                "is_deactivated",
                ConditionalRadiosQuestion(
                    "Yes",
                    "date_of_deactivation",
                    ConditionalRadios(
                        "is_deactivated_to_standard",
                        ConditionalRadiosQuestion(
                            "Yes",
                            "deactivation_standard",
                        ),
                        ConditionalRadiosQuestion(
                            "No",
                            "deactivation_standard_other",
                        ),
                    ),
                ),
                "No",
            ),
            ConditionalRadios(
                "is_gun_barrel",
                ConditionalRadiosQuestion(
                    "Yes",
                    ConditionalRadios(
                        "has_proof_mark",
                        "Yes",
                        ConditionalRadiosQuestion(
                            "No",
                            "no_proof_mark_details",
                        ),
                    ),
                ),
                "No",
            ),
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("is_deactivated") is True:
            if not cleaned_data["date_of_deactivation"]:
                self.add_error("date_of_deactivation", "Enter a valid date of deactivation")

            if cleaned_data["is_deactivated_to_standard"] == "":
                self.add_error(
                    "is_deactivated_to_standard",
                    "Select yes if the product has been deactivated to UK/EU proof house standards",
                )
            elif cleaned_data["is_deactivated_to_standard"] is True:
                if not cleaned_data["deactivation_standard"]:
                    self.add_error("deactivation_standard", "Select yes if the product has valid UK proof marks")
            elif cleaned_data["is_deactivated_to_standard"] is False:
                if not cleaned_data["deactivation_standard_other"]:
                    self.add_error(
                        "deactivation_standard_other",
                        "Enter details of who deactivated the product and to what standard it was done",
                    )

        if cleaned_data.get("is_gun_barrel") is True:
            if cleaned_data.get("has_proof_mark") is False and not cleaned_data["no_proof_mark_details"]:
                self.add_error(
                    "no_proof_mark_details", "Enter details of why the product does not have valid UK proof marks"
                )

        date_of_deactivation = cleaned_data.get("date_of_deactivation")
        if date_of_deactivation:
            cleaned_data.update(decompose_date("date_of_deactivation", date_of_deactivation))

        return cleaned_data


class ComponentAccessoryOfAFirearmAmmunitionUnitQuantityValueForm(forms.Form):
    title = AddGoodToApplicationForm.TITLE

    value = forms.CharField(
        error_messages={
            "required": "Enter the total value of the products",
        },
        label="Total value",
    )

    is_good_incorporated = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        error_messages={
            "required": "Select yes if the product will be incorporated into another product",
        },
        label="Will the product be incorporated into another product?",
        widget=forms.RadioSelect(),
    )

    is_deactivated = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        error_messages={
            "required": "Select yes if the product has been deactivated",
        },
        label="Has the product been deactivated?",
        widget=forms.RadioSelect(),
    )

    date_of_deactivation = DateInputField(
        label="Date of deactivation",
        required=False,
    )

    is_deactivated_to_standard = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        label="Has the product been deactivated to UK/EU proof house standards?",
        required=False,
        widget=forms.RadioSelect(),
    )

    deactivation_standard = forms.ChoiceField(
        choices=(
            ("", "Select"),
            ("UK", "UK"),
            ("EU", "EU"),
        ),
        label="Proof house standard",
        required=False,
    )

    deactivation_standard_other = forms.CharField(
        label="Describe who deactivated the product and to what standard it was done",
        widget=forms.Textarea,
        required=False,
    )

    def __init__(self, *args, good, number_of_items, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            summary_list(get_unit_quantity_value_summary_list_items(good, number_of_items)),
            Field("value", template="forms/currency_field.html"),
            Field.radios("is_good_incorporated", inline=True),
            ConditionalRadios(
                "is_deactivated",
                ConditionalRadiosQuestion(
                    "Yes",
                    "date_of_deactivation",
                    ConditionalRadios(
                        "is_deactivated_to_standard",
                        ConditionalRadiosQuestion(
                            "Yes",
                            "deactivation_standard",
                        ),
                        ConditionalRadiosQuestion(
                            "No",
                            "deactivation_standard_other",
                        ),
                    ),
                ),
                "No",
            ),
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("is_deactivated") is True:
            if not cleaned_data["date_of_deactivation"]:
                self.add_error("date_of_deactivation", "Enter a valid date of deactivation")

            if cleaned_data["is_deactivated_to_standard"] == "":
                self.add_error(
                    "is_deactivated_to_standard",
                    "Select yes if the product has been deactivated to UK/EU proof house standards",
                )
            elif cleaned_data["is_deactivated_to_standard"] is True:
                if not cleaned_data["deactivation_standard"]:
                    self.add_error("deactivation_standard", "Select yes if the product has valid UK proof marks")
            elif cleaned_data["is_deactivated_to_standard"] is False:
                if not cleaned_data["deactivation_standard_other"]:
                    self.add_error(
                        "deactivation_standard_other",
                        "Enter details of who deactivated the product and to what standard it was done",
                    )

        date_of_deactivation = cleaned_data.get("date_of_deactivation")
        if date_of_deactivation:
            cleaned_data.update(decompose_date("date_of_deactivation", date_of_deactivation))

        return cleaned_data


class UnitQuantityValueForm(forms.Form):
    title = AddGoodToApplicationForm.TITLE

    unit = forms.ChoiceField(
        choices=[
            ("", "Select"),
        ],  # This will get appended to in init
        error_messages={
            "required": "Select a unit of measurement",
        },
        label=AddGoodToApplicationForm.Units.TITLE,
    )

    quantity = forms.CharField(
        label="Quantity",
        error_messages={
            "required": "Enter a quantity",
        },
    )

    value = forms.CharField(
        label="Total value",
        error_messages={
            "required": "Enter the total value of the products",
        },
    )

    is_good_incorporated = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        error_messages={
            "required": "Select yes if the product will be incorporated into another product",
        },
        label="Will the product be incorporated into another product?",
        widget=forms.RadioSelect(),
    )

    def __init__(self, *args, good, number_of_items, request, **kwargs):
        super().__init__(*args, **kwargs)

        unit_field = self.fields["unit"]
        units = get_units(request)
        unit_field.choices += list(units.items())

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            summary_list(get_unit_quantity_value_summary_list_items(good, number_of_items)),
            "unit",
            Field(
                "quantity",
                autocomplete="off",
                autocorrect="off",
                css_class="govuk-input--width-20",
                pattern="^[0-9]*.{0,1}[0-9]{0,6}$",
            ),
            Field("value", template="forms/currency_field.html"),
            Field.radios("is_good_incorporated", inline=True),
            Submit("submit", "Save"),
        )


class ProductIsComponentForm(BaseForm):
    class Layout:
        TITLE = "Is the product a component?"

    is_component = forms.TypedChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label="",
        coerce=coerce_str_to_bool,
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the product is a component",
        },
    )

    def get_layout_fields(self):
        return (
            "is_component",
            HTML.details(
                "Help with components and accessories",
                render_to_string("goods/forms/common/help_with_component_accessories.html"),
            ),
        )


class ProductComponentDetailsForm(BaseForm):
    class Layout:
        TITLE = "What type of component is it?"

    component_type = forms.ChoiceField(
        choices=ComponentAccessoryChoices.choices,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select the type of component",
        },
    )

    designed_details = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        label="Provide details of the specific hardware",
    )

    modified_details = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        label="Provide details of the modifications and the specific hardware",
    )

    general_details = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        label="Provide details of the intended general-purpose use",
    )

    def get_layout_fields(self):
        return (
            ConditionalRadios(
                "component_type",
                ConditionalRadiosQuestion(
                    ComponentAccessoryChoices.DESIGNED.label,
                    "designed_details",
                ),
                ConditionalRadiosQuestion(
                    ComponentAccessoryChoices.MODIFIED.label,
                    "modified_details",
                ),
                ConditionalRadiosQuestion(
                    ComponentAccessoryChoices.GENERAL.label,
                    "general_details",
                ),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()

        component_type = cleaned_data.get("component_type")

        hardware_details = cleaned_data.get("designed_details")
        modified_hardware_details = cleaned_data.get("modified_details")
        general_purpose_details = cleaned_data.get("general_details")

        if component_type == ComponentAccessoryChoices.DESIGNED.value and not hardware_details:
            self.add_error(
                "designed_details",
                "Enter details of the specific hardware",
            )
        elif component_type == ComponentAccessoryChoices.MODIFIED.value and not modified_hardware_details:
            self.add_error(
                "modified_details",
                "Enter details of the modifications and the specific hardware",
            )
        elif component_type == ComponentAccessoryChoices.GENERAL.value and not general_purpose_details:
            self.add_error(
                "general_details",
                "Enter details of the intended general-purpose use",
            )

        return cleaned_data


class GoodArchiveForm(BaseForm):
    class Layout:
        TITLE = "Are you sure you want to archive this product?"
        SUBMIT_BUTTON_TEXT = "Archive product"

    def __init__(self, *args, cancel_url, **kwargs):
        self.cancel_url = cancel_url
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return [
            HTML.p(
                "If you move this product to the archive you will not be able to use it on any applications and it will be "
                "hidden from your default product list."
            ),
            HTML.p("You can remove it from the archive and restore it to your product list at any time."),
        ]

    def get_layout_actions(self):
        layout_actions = super().get_layout_actions()

        layout_actions.append(
            HTML(
                f'<a class="govuk-button govuk-button--secondary" href="{self.cancel_url}" id="cancel-id-cancel">Cancel</a>'
            ),
        )

        return layout_actions


class GoodRestoreForm(BaseForm):
    class Layout:
        TITLE = "Are you sure you want to restore this product?"
        SUBMIT_BUTTON_TEXT = "Restore product"

    def __init__(self, *args, cancel_url, **kwargs):
        self.cancel_url = cancel_url
        super().__init__(*args, **kwargs)

    def get_layout_fields(self):
        return [
            HTML.p("This product will show in your product list and you will be able to add it to applications."),
        ]

    def get_layout_actions(self):
        layout_actions = super().get_layout_actions()

        layout_actions.append(
            HTML(
                f'<a class="govuk-button govuk-button--secondary" href="{self.cancel_url}" id="cancel-id-cancel">Cancel</a>'
            ),
        )

        return layout_actions
