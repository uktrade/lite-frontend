from django.urls import reverse_lazy

from lite_content.lite_exporter_frontend.applications import DeletePartyDocumentForm
from lite_forms.components import Form, FileUpload, TextArea, BackLink, Option, RadioButtons
from lite_forms.generators import confirm_form


def attach_document_form(application_id, strings, back_link, is_optional):
    return Form(
        title=strings.TITLE,
        description=strings.DESCRIPTION,
        questions=[
            FileUpload(optional=is_optional),
            TextArea(title=strings.DESCRIPTION_FIELD_TITLE, optional=True, name="description"),
            RadioButtons(
                name="is_content_english",
                title=strings.Q1_TEXT,
                options=[
                    Option(key="true", value="Yes"),
                    Option(key="false", value="No"),
                ],
            ),
            RadioButtons(
                name="includes_company_letterhead",
                title=strings.Q2_TEXT,
                options=[
                    Option(key="true", value="Yes"),
                    Option(key="false", value="No"),
                ],
            ),
        ],
        back_link=BackLink(strings.BACK, reverse_lazy(back_link, kwargs={"pk": application_id})),
        default_button_name=strings.BUTTON_TEXT,
    )


def delete_document_confirmation_form(overview_url, strings):
    return confirm_form(
        title=DeletePartyDocumentForm.TITLE,
        confirmation_name="delete_document_confirmation",
        back_link_text=strings.BACK,
        back_url=overview_url,
    )
