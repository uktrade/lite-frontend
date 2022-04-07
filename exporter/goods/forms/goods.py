import json

from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Field, Fieldset, Layout, Submit
from django import forms
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from core.builtins.custom_tags import default_na, linkify
from core.forms.layouts import ConditionalQuestion, ConditionalRadios, summary_list
from exporter.core.constants import FIREARM_AMMUNITION_COMPONENT_TYPES, PRODUCT_CATEGORY_FIREARM
from exporter.core.helpers import (
    convert_control_list_entries,
    str_to_bool,
)
from exporter.core.services import get_control_list_entries, get_pv_gradings, get_units
from exporter.goods.helpers import get_category_display_string, good_summary
from lite_content.lite_exporter_frontend.goods import (
    AddGoodToApplicationForm,
    AttachDocumentForm,
    CreateGoodForm,
    DocumentAvailabilityForm,
    DocumentSensitivityForm,
    EditGoodForm,
    GoodGradingForm,
    GoodsQueryForm,
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
                                control_list_entries=get_control_list_entries(request, convert_to_options=True),
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


def raise_a_goods_query(good_id, raise_a_clc: bool, raise_a_pv: bool):
    questions = []

    if raise_a_clc:
        if GoodsQueryForm.CLCQuery.TITLE:
            questions += [
                Heading(GoodsQueryForm.CLCQuery.TITLE, HeadingStyle.M),
            ]
        questions += [
            TextInput(
                title=GoodsQueryForm.CLCQuery.Code.TITLE,
                description=GoodsQueryForm.CLCQuery.Code.DESCRIPTION,
                name="clc_control_code",
                optional=True,
            ),
            TextArea(
                title=GoodsQueryForm.CLCQuery.Details.TITLE,
                name="clc_raised_reasons",
                optional=True,
            ),
        ]

    if raise_a_pv:
        if GoodsQueryForm.PVGrading.TITLE:
            questions += [
                Heading(GoodsQueryForm.PVGrading.TITLE, HeadingStyle.M),
            ]
        questions += [
            TextArea(
                title=GoodsQueryForm.PVGrading.Details.TITLE,
                name="pv_grading_raised_reasons",
                optional=True,
            ),
        ]

    return Form(
        title=GoodsQueryForm.TITLE,
        description=GoodsQueryForm.DESCRIPTION,
        questions=questions,
        back_link=BackLink(GoodsQueryForm.BACK_LINK, reverse("goods:good", kwargs={"pk": good_id})),
        default_button_name="Save",
    )


def delete_good_form(good):
    return Form(
        title=EditGoodForm.DeleteConfirmationForm.TITLE,
        questions=[good_summary(good)],
        buttons=[
            Button(value=EditGoodForm.DeleteConfirmationForm.YES, action="submit", style=ButtonStyle.WARNING),
            Button(
                value=EditGoodForm.DeleteConfirmationForm.NO,
                action="",
                style=ButtonStyle.SECONDARY,
                link=reverse_lazy("goods:good", kwargs={"pk": good["id"]}),
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
        description="The file must be smaller than 50MB",
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
                title=CreateGoodForm.FirearmGood.FirearmsActCertificate.EXPIRY_DATE,
                description=CreateGoodForm.FirearmGood.FirearmsActCertificate.EXPIRY_DATE_HINT,
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


class ProductCategoryForm(forms.Form):
    title = CreateGoodForm.ProductCategory.TITLE

    item_category = forms.ChoiceField(
        choices=(
            ("group1_platform", CreateGoodForm.ProductCategory.GROUP1_PLATFORM),
            ("group1_device", CreateGoodForm.ProductCategory.GROUP1_DEVICE),
            ("group1_components", CreateGoodForm.ProductCategory.GROUP1_COMPONENTS),
            ("group1_materials", CreateGoodForm.ProductCategory.GROUP1_MATERIALS),
            (PRODUCT_CATEGORY_FIREARM, CreateGoodForm.ProductCategory.GROUP2_FIREARMS),
            ("group3_software", CreateGoodForm.ProductCategory.GROUP3_SOFTWARE),
            ("group3_technology", CreateGoodForm.ProductCategory.GROUP3_TECHNOLOGY),
        ),
        widget=forms.RadioSelect,
        label="",
        error_messages={
            "required": "Select a product category",
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "item_category",
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )


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
                ConditionalQuestion(
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
        if not any(value):
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
                ConditionalQuestion(
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
                ConditionalQuestion(
                    "Yes",
                    "information_security_details",
                ),
                CreateGoodForm.ProductInformationSecurity.NO,
            ),
            Submit("submit", "Save"),
        )


class AddGoodsQuestionsForm(forms.Form):

    name = forms.CharField(
        help_text="Give your product a name so it is easier to find in your product list",
        error_messages={
            "required": "Enter a product name",
        },
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
        choices=[],  # set in __init__
        required=False,
        # setting id for javascript to use
        widget=forms.SelectMultiple(attrs={"id": "control_list_entries"}),
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
                ConditionalQuestion(
                    CreateGoodForm.IsControlled.YES,
                    "control_list_entries",
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
                ConditionalQuestion(
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
        label="",
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
            self.title = "Is the product covered by section 5 of the Firearms Act 1968?"

            details = [
                "What does section 5 cover?",
                linkify(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE_LINK,
                    name=CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE,
                )
                + f"&nbsp;&nbsp;covers weapons and ammunition that are generally prohibited.",
            ]
        else:
            self.title = CreateGoodForm.FirearmGood.FirearmsActCertificate.TITLE

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
            "is_covered_by_firearm_act_section_one_two_or_five"
            if self.is_rfd
            else ConditionalRadios(
                "is_covered_by_firearm_act_section_one_two_or_five",
                ConditionalQuestion(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.YES,
                    "firearms_act_section",
                ),
                CreateGoodForm.FirearmGood.FirearmsActCertificate.NO,
                CreateGoodForm.FirearmGood.FirearmsActCertificate.DONT_KNOW,
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
                ConditionalQuestion(
                    CreateGoodForm.ProductComponent.YES_DESIGNED,
                    "designed_details",
                ),
                ConditionalQuestion(
                    CreateGoodForm.ProductComponent.YES_MODIFIED,
                    "modified_details",
                ),
                ConditionalQuestion(
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

    if good["item_category"]["key"] == PRODUCT_CATEGORY_FIREARM:
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
                ConditionalQuestion(
                    "Yes",
                    "date_of_deactivation",
                    ConditionalRadios(
                        "is_deactivated_to_standard",
                        ConditionalQuestion(
                            "Yes",
                            "deactivation_standard",
                        ),
                        ConditionalQuestion(
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
                ConditionalQuestion(
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


class ComponentOfAFirearmUnitQuantityValueForm(forms.Form):
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
                ConditionalQuestion(
                    "Yes",
                    "date_of_deactivation",
                    ConditionalRadios(
                        "is_deactivated_to_standard",
                        ConditionalQuestion(
                            "Yes",
                            "deactivation_standard",
                        ),
                        ConditionalQuestion(
                            "No",
                            "deactivation_standard_other",
                        ),
                    ),
                ),
                "No",
            ),
            ConditionalRadios(
                "is_gun_barrel",
                ConditionalQuestion(
                    "Yes",
                    ConditionalRadios(
                        "has_proof_mark",
                        "Yes",
                        ConditionalQuestion(
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


class ComponentOfAFirearmAmmunitionUnitQuantityValueForm(forms.Form):
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
                ConditionalQuestion(
                    "Yes",
                    "date_of_deactivation",
                    ConditionalRadios(
                        "is_deactivated_to_standard",
                        ConditionalQuestion(
                            "Yes",
                            "deactivation_standard",
                        ),
                        ConditionalQuestion(
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

    quantity = forms.CharField(label="Quantity", required=False)

    value = forms.CharField(label="Total value", required=False)

    is_good_incorporated = forms.TypedChoiceField(
        choices=((True, "Yes"), (False, "No")),
        coerce=lambda x: x == "True",
        error_messages={
            "required": "Select yes if the product will be incorporated into another product",
        },
        label="Will the product be incorporated into another product?",
        widget=forms.RadioSelect(),
    )

    OPTIONAL_VALUE = "ITG"

    def __init__(self, *args, good, number_of_items, request, **kwargs):
        super().__init__(*args, **kwargs)

        unit_field = self.fields["unit"]
        units = get_units(request)
        unit_field.choices += list(units.items())

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            summary_list(get_unit_quantity_value_summary_list_items(good, number_of_items)),
            Field(
                "unit",
                data_unit_toggle=json.dumps(
                    {
                        "quantity_id": self["quantity"].id_for_label,
                        "value_id": self["value"].id_for_label,
                        "optional_value": self.OPTIONAL_VALUE,
                    }
                ),
            ),
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

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("unit") != self.OPTIONAL_VALUE:
            if not cleaned_data.get("quantity"):
                self.add_error("quantity", "Enter a quantity")
            if not cleaned_data.get("value"):
                self.add_error("value", "Enter the total value of the products")

        return cleaned_data
