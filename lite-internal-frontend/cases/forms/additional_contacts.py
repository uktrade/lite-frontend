from django.urls import reverse_lazy

from core.services import get_countries
from lite_content.lite_internal_frontend.cases import AddAdditionalContact
from lite_forms.common import foreign_address_questions
from lite_forms.components import Form, TextInput, BackLink


def add_additional_contact_form(request, queue_id, case_id):
    return Form(
        title=AddAdditionalContact.TITLE,
        description=AddAdditionalContact.DESCRIPTION,
        questions=[
            TextInput(
                title=AddAdditionalContact.Details.TITLE,
                description=AddAdditionalContact.Details.DESCRIPTION,
                name="details",
            ),
            TextInput(title=AddAdditionalContact.Name.TITLE, name="name"),
            *foreign_address_questions(get_countries(request, True), ""),
            TextInput(title=AddAdditionalContact.Email.TITLE, name="email"),
            TextInput(
                title=AddAdditionalContact.PhoneNumber.TITLE,
                description=AddAdditionalContact.PhoneNumber.DESCRIPTION,
                name="phone_number",
            ),
        ],
        back_link=BackLink(
            AddAdditionalContact.BACK_LINK,
            reverse_lazy("cases:case", kwargs={"queue_pk": queue_id, "pk": case_id, "tab": "additional-contacts"}),
        ),
        default_button_name=AddAdditionalContact.SUBMIT_BUTTON,
        container="case",
    )
