from crispy_forms_gds.choices import Choice
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit, HTML
from django import forms
from django.urls import reverse_lazy

from core.forms.layouts import ConditionalRadios, ConditionalQuestion
from core.forms.widgets import Autocomplete
from exporter.core.constants import CaseTypes
from exporter.core.services import get_countries
from lite_content.lite_exporter_frontend import strings
from lite_content.lite_exporter_frontend.applications import PartyForm, PartyTypeForm
from lite_forms.common import country_question
from lite_forms.components import (
    BackLink,
    RadioButtons,
    Form,
    Option,
    TextArea,
    TextInput,
    FormGroup,
)
from lite_forms.generators import confirm_form


def party_create_new_or_copy_existing_form(application_id, back_url):
    return confirm_form(
        title=PartyForm.CopyExistingForm.TITLE,
        confirmation_name="copy_existing",
        yes_label=PartyForm.CopyExistingForm.YES,
        no_label=PartyForm.CopyExistingForm.NO,
        back_link_text=PartyForm.CopyExistingForm.BACK_LINK,
        back_url=back_url,
        submit_button_text=PartyForm.CopyExistingForm.BUTTON,
    )


def party_type_form(application, title, button, back_link):
    return Form(
        title=title,
        questions=[
            RadioButtons(
                "sub_type",
                options=[
                    Option("government", PartyForm.Options.GOVERNMENT),
                    Option("commercial", PartyForm.Options.COMMERCIAL),
                    Option("individual", PartyForm.Options.INDIVIDUAL),
                    Option(
                        "other", PartyForm.Options.OTHER, show_or=True, components=[TextInput(name="sub_type_other")]
                    ),
                ],
            ),
        ],
        default_button_name=button,
        back_link=back_link,
    )


def party_name_form(title, button):
    return Form(title=title, questions=[TextInput("name")], default_button_name=button)


def party_website_form(title, button):
    return Form(
        title=title,
        questions=[TextInput("website")],
        default_button_name=button,
    )


def party_address_form(request, title, button, is_gb_excluded=False):
    return Form(
        title=title,
        questions=[
            TextArea("address", "Address"),
            country_question(
                countries=get_countries(request, True, ["GB"]) if is_gb_excluded else get_countries(request, True),
                prefix="",
            ),
        ],
        default_button_name=button,
    )


def party_signatory_name_form(title, button):
    return Form(
        title=title,
        description="This is the name of the person who signed the end user undertaking or stockist undertaking",
        questions=[TextInput("signatory_name_euu")],
        default_button_name=button,
    )


def party_clearance_level_form(options, button):
    return Form(
        title=strings.Parties.Clearance.Level.TITLE,
        description=strings.Parties.Clearance.Level.DESCRIPTION,
        questions=[RadioButtons(name="clearance_level", options=options)],
        default_button_name=button,
    )


def party_descriptor_form(button):
    title = strings.Parties.Clearance.Descriptors.TITLE
    return Form(
        title=title,
        questions=[TextInput(title=strings.Parties.Clearance.Descriptors.DESCRIPTION, name="descriptors")],
        default_button_name=button,
    )


def clearance_level_forms(options, button):
    return [party_clearance_level_form(options, button), party_descriptor_form(button)]


def new_party_form_group(request, application, strings, back_url, clearance_options=None, is_end_user=False):
    back_link = BackLink(PartyTypeForm.BACK_LINK, reverse_lazy(back_url, kwargs={"pk": application["id"]}))

    forms = [
        party_type_form(application, strings.TITLE, strings.BUTTON, back_link),
        party_name_form(strings.NAME_FORM_TITLE, strings.BUTTON),
        party_website_form(strings.WEBSITE_FORM_TITLE, strings.BUTTON),
    ]

    if clearance_options:
        forms.extend(clearance_level_forms(clearance_options, strings.BUTTON))

    # Exclude the UK if end user on standard transhipment
    is_gb_excluded = application.case_type["reference"]["key"] == CaseTypes.SITL and is_end_user
    forms.append(
        party_address_form(request, strings.ADDRESS_FORM_TITLE, strings.SUBMIT_BUTTON, is_gb_excluded=is_gb_excluded)
    )

    if is_end_user:
        forms.append(party_signatory_name_form("Signatory name", "Save and continue"))

    return FormGroup(forms)


class PartyReuseForm(forms.Form):
    title = "Do you want to reuse an existing party?"

    reuse_party = forms.ChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if you want to reuse an existing party",
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "reuse_party",
            Submit("submit", "Continue"),
        )


class PartySubTypeSelectForm(forms.Form):
    title = "Select the type of end user"

    CHOICES = (
        Choice("government", PartyForm.Options.GOVERNMENT),
        Choice("commercial", PartyForm.Options.COMMERCIAL),
        Choice("individual", PartyForm.Options.INDIVIDUAL, divider="or"),
        Choice("other", PartyForm.Options.OTHER),
    )

    sub_type = forms.ChoiceField(
        choices=CHOICES,
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select what type of party you're creating",
        },
    )
    sub_type_other = forms.CharField(required=False, label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            ConditionalRadios(
                "sub_type",
                PartyForm.Options.GOVERNMENT,
                PartyForm.Options.COMMERCIAL,
                PartyForm.Options.INDIVIDUAL,
                ConditionalQuestion(PartyForm.Options.OTHER, "sub_type_other"),
            ),
            Submit("submit", "Continue"),
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("sub_type") == "other" and not cleaned_data.get("sub_type_other"):
            self.add_error("sub_type_other", "Enter the type of the party you're adding")

        return cleaned_data


class PartyNameForm(forms.Form):
    title = "End user name"
    name = forms.CharField(label="", error_messages={"required": "Enter a name"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "name",
            Submit("submit", "Continue"),
        )


class PartyWebsiteForm(forms.Form):
    title = "End user website address (optional)"
    website = forms.CharField(required=False, label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "website",
            Submit("submit", "Continue"),
        )


class PartyAddressForm(forms.Form):
    title = "End user address"
    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "10"}), error_messages={"required": "Enter an address"}
    )
    country = forms.ChoiceField(
        choices=[("", "Select a country")], error_messages={"required": "Select the country"}
    )  # populated in __init__

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        self.fields["country"].widget = Autocomplete(attrs={"id": "country-autocomplete", "nonce": request.csp_nonce})

        countries = get_countries(request)
        country_choices = [(country["id"], country["name"]) for country in countries]
        self.fields["country"].choices += country_choices

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "address",
            "country",
            Submit("submit", "Save and continue"),
        )


class PartySignatoryNameForm(forms.Form):
    title = "Signatory name"
    signatory_name_euu = forms.CharField(
        label="",
        help_text="This is the name of the person who signed the end user undertaking or stockist undertaking",
        error_messages={"required": "Enter a name"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "signatory_name_euu",
            Submit("submit", "Continue"),
        )


class PartyDocumentsForm(forms.Form):
    title = "Do you have an end-user document?"
    text_p1 = """
        You will be asked to upload either an
         <a class="govuk-link" target="_blank" href="https://www.gov.uk/government/publications/end-user-undertaking-euu-form">
         end-user undertaking (opens in new tab)</a> or
         <a class="govuk-link" target="_blank" href="https://www.gov.uk/government/publications/stockist-undertaking-su-form">
         stockist undertaking (opens in new tab)</a> completed by the end-user or stockist.
    """
    text_p2 = "You must include at least one page on company letterhead. This can either be within the end-user document or on a separate document."
    text_p3 = (
        "Products listed in the document should match as closely as possible to the products listed in the application."
    )
    text_p4 = "All products on the application must appear in the document."
    end_user_document_available = forms.ChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if you have an end-user document",
        },
    )
    end_user_document_missing_reason = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"rows": "5"}),
        help_text="Explain why you do not have an end-user undertaking or stockist undertaking.",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML.p(self.text_p1),
            HTML.p(self.text_p2),
            HTML.p(self.text_p3),
            HTML.p(self.text_p4),
            ConditionalRadios(
                "end_user_document_available",
                "Yes",
                ConditionalQuestion("No", "end_user_document_missing_reason"),
            ),
            Submit("submit", "Continue"),
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("end_user_document_available") == "False" and not cleaned_data.get(
            "end_user_document_missing_reason"
        ):
            self.add_error(
                "end_user_document_missing_reason",
                "Enter why you do not have an end-user undertaking or stockist undertaking",
            )

        return cleaned_data


class PartyDocumentUploadForm(forms.Form):
    title = "Upload an end-user document"
    party_document = forms.FileField(
        label="",
        error_messages={
            "required": "Select an end-user document",
        },
    )
    product_differences_note = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}),
        label="Describe any differences between products listed in the document and products on the application (optional)",
        required=False,
    )
    document_in_english = forms.ChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label="Is the end-user document in English?",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the end-user document is in English",
        },
    )
    document_on_letterhead = forms.ChoiceField(
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        label="Does the document include at least one page on company letterhead?",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select yes if the document includes at least one page on company letterhead",
        },
    )

    def __init__(self, edit, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # when edit user may choose not to replace the existing document
        # so make this field optional
        if edit:
            self.fields["party_document"].required = False

        self.helper = FormHelper()
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "party_document",
            "product_differences_note",
            "document_in_english",
            "document_on_letterhead",
            Submit("submit", "Continue"),
        )


class PartyEnglishTranslationDocumentUploadForm(forms.Form):
    title = "Upload an English translation"
    party_eng_translation_document = forms.FileField(
        label="",
        error_messages={
            "required": "Select an English translation",
        },
    )

    def __init__(self, edit, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if edit:
            self.fields["party_eng_translation_document"].required = False

        self.helper = FormHelper()
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML.p("Exporters are responsible for verifying that translations are accurate."),
            "party_eng_translation_document",
            Submit("submit", "Continue"),
        )


class PartyCompanyLetterheadDocumentUploadForm(forms.Form):
    title = "Upload a document on company letterhead"
    party_letterhead_document = forms.FileField(
        label="",
        error_messages={
            "required": "Select a document on company letterhead",
        },
    )

    def __init__(self, edit, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if edit:
            self.fields["party_letterhead_document"].required = False

        self.helper = FormHelper()
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML.p("The document only needs to include the end-user's name and signature."),
            "party_letterhead_document",
            Submit("submit", "Continue"),
        )


class PartyEC3DocumentUploadForm(forms.Form):
    title = "Upload an EC3 form (optional)"
    party_ec3_document = forms.FileField(label="", required=False)
    ec3_missing_reason = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}),
        label="",
        help_text="If you do not have an EC3 form, explain why (optional)",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML.p(
                "An EC3 form is required if you are exporting firearm products from Northern Ireland to a country within the European Union."
            ),
            "party_ec3_document",
            "ec3_missing_reason",
            HTML.details(
                "Help with the EC3 form and exemptions",
                """You do not require an EC3 form to export weapons sights, sound suppressors or silencers, magazines, antique firearms
                 manufactured before 1890 (including parts and components for those firearms) and items which will be used by
                 police, armed forces or public authorities.<br><br>
                <a class="govuk-link" target="_blank" href="https://www.gov.uk/government/publications/end-user-undertaking-euu-form">
                Guidance on the EC3 form (opens in new tab)</a>
            """,
            ),
            Submit("submit", "Continue"),
        )
