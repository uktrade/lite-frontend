from django.urls import reverse_lazy

from lite_content.lite_exporter_frontend.applications import DeletePartyDocumentForm
from lite_forms.components import Form, FileUpload, TextArea, BackLink, Label
from lite_forms.generators import confirm_form


def attach_document_form(application_id, strings, back_link):
    return Form(
        strings.TITLE,
        strings.DESCRIPTION,
        [FileUpload(), TextArea(title=strings.DESCRIPTION_FIELD_TITLE, optional=True, name="description")],
        back_link=BackLink(strings.BACK, reverse_lazy(back_link, kwargs={"pk": application_id})),
        footer_label=Label(
            'Or <a id="return_to_application" href="'
            + str(reverse_lazy("applications:task_list", kwargs={"pk": application_id}))
            + '" class="govuk-link govuk-link--no-visited-state">'
            + strings.SAVE_AND_RETURN_LATER
            + "</a> "
            + strings.ATTACH_LATER
        ),
    )


def delete_document_confirmation_form(overview_url, strings):
    return confirm_form(
        title=DeletePartyDocumentForm.TITLE,
        confirmation_name="delete_document_confirmation",
        back_link_text=strings.BACK,
        back_url=overview_url,
    )
