from django.urls import reverse_lazy

from lite_content.lite_internal_frontend import picklists
from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_content.lite_internal_frontend.strings import letter_templates
from lite_forms.components import Form, RadioButtonsImage, Option, BackLink, TextArea, Custom, HelpSection


def select_template_form(templates, back_url):
    return Form(
        title=letter_templates.LetterTemplatesPage.PickTemplate.TITLE,
        questions=[
            RadioButtonsImage(
                name="template",
                options=[
                    Option(
                        template["id"],
                        template["name"],
                        img_url=f"/assets/images/letter_templates/{template['layout']['filename']}.png",
                    )
                    for template in templates["results"]
                ],
            )
        ],
        default_button_name=letter_templates.LetterTemplatesPage.PickTemplate.BUTTON,
        back_link=BackLink(url=back_url),
        container="case",
    )


def select_addressee_form():
    return Form(
        title=GenerateDocumentsPage.AddresseeForm.TITLE,
        description=GenerateDocumentsPage.AddresseeForm.DESCRIPTION,
        questions=[Custom("components/addressee-table.html")],
        default_button_name=letter_templates.LetterTemplatesPage.PickTemplate.BUTTON,
        container="case",
    )


def edit_document_text_form(kwargs, post_url):
    return Form(
        title=GenerateDocumentsPage.EditTextForm.HEADING,
        questions=[
            TextArea(name="text"),
        ],
        default_button_name=GenerateDocumentsPage.EditTextForm.BUTTON,
        post_url=reverse_lazy(post_url, kwargs=kwargs),
        helpers=[HelpSection(picklists.NewPicklistForm.HELP, None, "teams/markdown-help.html")],
        container="case",
    )
