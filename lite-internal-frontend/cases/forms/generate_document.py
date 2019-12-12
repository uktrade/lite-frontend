from django.urls import reverse_lazy

from letter_templates.context_variables import get_sample_context_variables
from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_forms.components import Form, RadioButtonsImage, Option, BackLink, Checkboxes, HiddenField, MarkdownArea, Link

ADD_PARAGRAPH_KEY = "add_paragraphs"


def select_template_form(templates, case_id):
    return Form(
        title=strings.LETTER_TEMPLATES.LetterTemplatesPage.PickTemplate.TITLE,
        questions=[
            RadioButtonsImage(
                name="template",
                options=[
                    Option(t["id"], t["name"], img_url=f"/assets/images/letter_templates/{t['layout']['filename']}.png")
                    for t in templates
                ],
            )
        ],
        default_button_name=strings.LETTER_TEMPLATES.LetterTemplatesPage.PickTemplate.BUTTON,
        back_link=BackLink(
            text=GenerateDocumentsPage.SelectTemplateForm.BACK_LINK,
            url=reverse_lazy("cases:documents", kwargs={"pk": case_id}),
        ),
    )


def edit_document_text_form(backlink, kwargs):
    return Form(
        title=GenerateDocumentsPage.EditTextForm.HEADING,
        questions=[
            MarkdownArea(variables=get_sample_context_variables(), name="text", extras={"max_length": 5000}),
            Link(
                name=ADD_PARAGRAPH_KEY,
                text=GenerateDocumentsPage.EditTextForm.ADD_PARAGRAPHS_LINK,
                address=reverse_lazy("cases:generate_document_add_paragraphs", kwargs=kwargs),
                form_action=True,
            ),
        ],
        default_button_name=GenerateDocumentsPage.EditTextForm.BUTTON,
        back_link=backlink,
        post_url=reverse_lazy("cases:generate_document_preview", kwargs=kwargs),
    )


def add_paragraphs_form(paragraphs, text, kwargs):
    return Form(
        title=GenerateDocumentsPage.AddParagraphsForm.HEADING,
        questions=[
            HiddenField(name="text[]", value=text),
            Checkboxes(
                name="text[]",
                options=[Option(paragraph["text"], paragraph["name"], auto_check=False) for paragraph in paragraphs],
            ),
        ],
        back_link=BackLink(),
        default_button_name=GenerateDocumentsPage.AddParagraphsForm.BUTTON,
        post_url=reverse_lazy("cases:generate_document_edit", kwargs=kwargs),
    )
