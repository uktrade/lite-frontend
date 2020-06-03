from django.urls import reverse_lazy

from core.components import PicklistPicker
from letter_templates.context_variables import get_sample_context_variables
from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_content.lite_internal_frontend.strings import letter_templates
from lite_forms.components import Form, RadioButtonsImage, Option, MarkdownArea
from picklists.enums import PicklistCategories


def select_template_form(templates, total_pages, back_link):
    return Form(
        title=letter_templates.LetterTemplatesPage.PickTemplate.TITLE,
        questions=[
            RadioButtonsImage(
                name="template",
                options=[
                    Option(t["id"], t["name"], img_url=f"/assets/images/letter_templates/{t['layout']['filename']}.png")
                    for t in templates
                ],
                total_pages=total_pages,
            )
        ],
        default_button_name=letter_templates.LetterTemplatesPage.PickTemplate.BUTTON,
        back_link=back_link,
        container="case",
    )


def edit_document_text_form(back_link, kwargs, post_url):
    return Form(
        title=GenerateDocumentsPage.EditTextForm.HEADING,
        questions=[
            MarkdownArea(variables=get_sample_context_variables(), name="text", extras={"max_length": 5000}),
            PicklistPicker(target="text", type=PicklistCategories.letter_paragraph.key),
        ],
        default_button_name=GenerateDocumentsPage.EditTextForm.BUTTON,
        back_link=back_link,
        post_url=reverse_lazy(post_url, kwargs=kwargs),
        container="case",
    )
