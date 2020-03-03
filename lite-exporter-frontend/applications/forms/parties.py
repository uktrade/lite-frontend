from django.urls import reverse_lazy

from core.services import get_countries
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


def party_create_new_or_copy_existing_form(application_id):
    return confirm_form(
        title=PartyForm.CopyExistingForm.TITLE,
        confirmation_name="copy_existing",
        yes_label=PartyForm.CopyExistingForm.YES,
        no_label=PartyForm.CopyExistingForm.NO,
        back_link_text=PartyForm.CopyExistingForm.BACK_LINK,
        back_url=reverse_lazy("applications:task_list", kwargs={"pk": application_id}),
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
                    Option("other", PartyForm.Options.OTHER, show_or=True),
                ],
            ),
        ],
        default_button_name=button,
        back_link=back_link,
    )


def party_name_form(title, button):
    return Form(title=title, questions=[TextInput("name")], default_button_name=button)


def party_website_form(title, button):
    return Form(title=title, questions=[TextInput("website")], default_button_name=button,)


def party_address_form(title, button):
    return Form(
        title=title,
        questions=[TextArea("address", "Address"), country_question(countries=get_countries(None, True), prefix=""),],
        default_button_name=button,
    )


def party_clearance_level_form(options, button):
    return Form(
        title=strings.Parties.Clearance.Level.TITLE,
        description=strings.Parties.Clearance.Level.DESCRIPTION,
        questions=[RadioButtons(name="clearance_level", options=options)],
        default_button_name=button,
    )


def party_descriptor_form(button, optional=False):
    title = (
        strings.Parties.Clearance.Descriptors.TITLE_OPTIONAL
        if optional
        else strings.Parties.Clearance.Descriptors.TITLE
    )
    return Form(
        title=title,
        questions=[TextInput(title=strings.Parties.Clearance.Descriptors.DESCRIPTION, name="descriptors")],
        default_button_name=button,
    )


def clearance_level_forms(options, button):
    return [party_clearance_level_form(options, button), party_descriptor_form(button, optional=True)]


def new_party_form_group(application, strings, back_url, clearance_options=None):
    back_link = BackLink(PartyTypeForm.BACK_LINK, reverse_lazy(back_url, kwargs={"pk": application["id"]}))

    forms = [
        party_type_form(application, strings.TITLE, strings.BUTTON, back_link),
        party_name_form(strings.NAME_FORM_TITLE, strings.BUTTON),
        party_website_form(strings.WEBSITE_FORM_TITLE, strings.BUTTON),
    ]

    if clearance_options:
        forms.extend(clearance_level_forms(clearance_options, strings.BUTTON))

    forms.append(party_address_form(strings.ADDRESS_FORM_TITLE, strings.SUBMIT_BUTTON))

    return FormGroup(forms)
