from django.urls import reverse_lazy

from applications.forms.parties import (
    party_name_form,
    party_website_form,
    party_address_form,
    party_type_form,
    clearance_level_forms,
)
from conf.constants import PERMANENT, F680
from lite_content.lite_exporter_frontend.applications import ThirdPartyForm, PartyForm, PartyTypeForm
from lite_forms.components import BackLink, RadioButtons, Form, Option, FormGroup, TextInput

role_option_list = {
    "agent": ThirdPartyForm.Options.AGENT,
    "additional_end_user": ThirdPartyForm.Options.ADDITIONAL_END_USER,
    "intermediate_consignee": ThirdPartyForm.Options.INTERMEDIATE_CONSIGNEE,
    "submitter": ThirdPartyForm.Options.SUBMITTER,
    "consultant": ThirdPartyForm.Options.CONSULTANT,
    "contact": ThirdPartyForm.Options.CONTACT,
    "exporter": ThirdPartyForm.Options.EXPORTER,
    "customer": ThirdPartyForm.Options.CUSTOMER,
}


def _third_party_role_form(application, title, button, options, back_url):
    return Form(
        title=title,
        questions=[RadioButtons("role", options=options)],
        default_button_name=button,
        back_link=BackLink(PartyTypeForm.BACK_LINK, reverse_lazy(back_url, kwargs={"pk": application["id"]})),
    )


def third_party_forms(request, application, strings, back_url, clearance_options=None):
    form_options = role_option_list.copy()
    if application["case_type"]["sub_type"]["key"] != F680:
        form_options.pop("customer")
    export_type = application.get("export_type")
    if not export_type or export_type.get("key") == PERMANENT:
        del form_options["additional_end_user"]

    options = [Option(key, value) for key, value in form_options.items()]
    options.append(Option("other", PartyForm.Options.OTHER, show_or=True, components=[TextInput(name="role_other")]))
    forms = [
        _third_party_role_form(application, strings.ROLE_TITLE, strings.BUTTON, options, back_url),
        party_type_form(application, strings.TYPE_TITLE, strings.BUTTON, BackLink()),
        party_name_form(strings.NAME_FORM_TITLE, strings.BUTTON),
        party_website_form(strings.WEBSITE_FORM_TITLE, strings.BUTTON),
    ]

    if clearance_options:
        forms.extend(clearance_level_forms(clearance_options, strings.BUTTON))

    forms.append(party_address_form(request, strings.ADDRESS_FORM_TITLE, strings.SUBMIT_BUTTON))

    return FormGroup(forms)
