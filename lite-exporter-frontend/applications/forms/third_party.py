from lite_forms.components import RadioButtons, Form, Option, FormGroup

from lite_content.lite_exporter_frontend.applications import ThirdPartyForm, PartyForm
from applications.forms.end_user import _party_name_form, _party_website_form, _party_address_form
from applications.components import back_to_task_list

option_list = {
    "agent": ThirdPartyForm.Options.AGENT,
    "additional_end_user": ThirdPartyForm.Options.ADDITIONAL_END_USER,
    "intermediate_consignee": ThirdPartyForm.Options.INTERMEDIATE_CONSIGNEE,
    "submitter": ThirdPartyForm.Options.SUBMITTER,
    "consultant": ThirdPartyForm.Options.CONSULTANT,
    "contact": ThirdPartyForm.Options.CONTACT,
    "exporter": ThirdPartyForm.Options.EXPORTER,
}


def _third_party_type_form(application, title, button, options):
    return Form(
        title=title,
        questions=[RadioButtons("sub_type", options=options)],
        default_button_name=button,
        back_link=back_to_task_list(application["id"]),
    )


def third_party_forms(application):
    form_options = option_list.copy()
    if application["export_type"] and application["export_type"]["key"] == "permanent":
        del form_options["additional_end_user"]

    options = [Option(key, value) for key, value in form_options.items()]
    options.append(Option("other", PartyForm.Options.OTHER, show_or=True))

    return FormGroup(
        [
            _third_party_type_form(application, ThirdPartyForm.TITLE, ThirdPartyForm.BUTTON, options),
            _party_name_form(ThirdPartyForm.NAME_FORM_TITLE, ThirdPartyForm.BUTTON),
            _party_website_form(ThirdPartyForm.WEBSITE_FORM_TITLE, ThirdPartyForm.BUTTON),
            _party_address_form(ThirdPartyForm.ADDRESS_FORM_TITLE, ThirdPartyForm.SUBMIT_BUTTON),
        ]
    )
