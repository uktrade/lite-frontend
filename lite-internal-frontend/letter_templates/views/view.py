from django.shortcuts import render
from django.views.generic import TemplateView

from letter_templates import helpers
from letter_templates.services import (
    get_letter_paragraphs,
    get_letter_templates,
    get_letter_template,
)


class LetterTemplatesList(TemplateView):
    def get(self, request, **kwargs):
        context = {"letter_templates": get_letter_templates(request)}
        return render(request, "letter_templates/letter_templates.html", context)


class LetterTemplateDetail(TemplateView):
    def get(self, request, **kwargs):
        letter_template_id = str(kwargs["pk"])
        letter_template = get_letter_template(request, letter_template_id)

        context = {
            "letter_template": letter_template,
            "preview": helpers.generate_preview(
                letter_template["layout"]["filename"],
                get_letter_paragraphs(request, letter_template["letter_paragraphs"]),
            ),
        }
        return render(request, "letter_templates/letter_template.html", context)
