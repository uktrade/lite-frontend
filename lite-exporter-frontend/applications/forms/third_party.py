from django.urls import reverse_lazy

from applications.forms.parties import party_name_form, party_website_form, party_address_form
from lite_content.lite_exporter_frontend.applications import ThirdPartyForm, PartyForm, PartyTypeForm
from lite_forms.components import BackLink, RadioButtons, Form, Option, FormGroup

option_list = {
    "agent": ThirdPartyForm.Options.AGENT,
    "additional_end_user": ThirdPartyForm.Options.ADDITIONAL_END_USER,
    "intermediate_consignee": ThirdPartyForm.Options.INTERMEDIATE_CONSIGNEE,
    "submitter": ThirdPartyForm.Options.SUBMITTER,
    "consultant": ThirdPartyForm.Options.CONSULTANT,
    "contact": ThirdPartyForm.Options.CONTACT,
    "exporter": ThirdPartyForm.Options.EXPORTER,
}


def _third_party_type_form(application, title, button, options, back_url):
    return Form(
        title=title,
        questions=[RadioButtons("sub_type", options=options)],
        default_button_name=button,
        back_link=BackLink(PartyTypeForm.BACK_LINK, reverse_lazy(back_url, kwargs={"pk": application["id"]})),
    )


def third_party_forms(application, strings, back_url):
    form_options = option_list.copy()
    if application["export_type"] and application["export_type"]["key"] == "permanent":
        del form_options["additional_end_user"]

    options = [Option(key, value) for key, value in form_options.items()]
    options.append(Option("other", PartyForm.Options.OTHER, show_or=True))

    return FormGroup(
        [
            _third_party_type_form(application, strings.TITLE, strings.BUTTON, options, back_url),
            party_name_form(strings.NAME_FORM_TITLE, strings.BUTTON),
            party_website_form(strings.WEBSITE_FORM_TITLE, strings.BUTTON),
            party_address_form(strings.ADDRESS_FORM_TITLE, strings.SUBMIT_BUTTON),
        ]
    )
