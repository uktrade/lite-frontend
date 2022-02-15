from django.shortcuts import render
from django.views.generic import TemplateView

from caseworker.letter_templates.helpers import get_template_content
from caseworker.letter_templates.services import get_letter_paragraphs, get_letter_preview
from lite_content.lite_internal_frontend.letter_templates import LetterTemplatesPage
from lite_forms.generators import error_page
from caseworker.picklists.services import get_picklists_for_input

from core.auth.views import LoginRequiredMixin


def get_order_paragraphs_page(request, template_content):
    letter_paragraphs = get_letter_paragraphs(request, template_content["letter_paragraphs"])
    return render(
        request,
        "letter-templates/order-letter-paragraphs.html",
        {
            "letter_paragraphs": letter_paragraphs,
            "name": template_content["name"],
            "layout": template_content["layout"],
            "visible_to_exporter": template_content["visible_to_exporter"],
            "include_digital_signature": template_content["include_digital_signature"],
            "case_types": template_content["case_types"],
            "decisions": template_content["decisions"],
        },
    )


class LetterParagraphs(LoginRequiredMixin, TemplateView):
    @staticmethod
    def _error_page():
        return error_page(
            None,
            title=LetterTemplatesPage.TITLE,
            description=LetterTemplatesPage.ERROR,
            show_back_link=True,
        )

    @staticmethod
    def _add_letter_paragraph(request, template_content):
        all_letter_paragraphs = get_picklists_for_input(request, "letter_paragraph")
        context = {
            "name": template_content["name"],
            "layout": template_content["layout"],
            "visible_to_exporter": template_content["visible_to_exporter"],
            "include_digital_signature": template_content["include_digital_signature"],
            "case_types": template_content["case_types"],
            "decisions": template_content["decisions"],
            "letter_paragraphs": [
                paragraph
                for paragraph in all_letter_paragraphs
                if paragraph["id"] not in template_content["letter_paragraphs"]
            ],
            "existing_letter_paragraphs": template_content["letter_paragraphs"],
        }
        return render(request, "letter-templates/add-letter-paragraphs.html", context)

    def _preview(self, request, template_content):
        """
        Display a preview once letter paragraphs have been selected and sorted.
        """
        preview, status_code = get_letter_preview(
            request, template_content["layout"]["id"], template_content["letter_paragraphs"]
        )
        if status_code == 400:
            return self._error_page()
        return render(
            request,
            "letter-templates/preview.html",
            {
                "preview": preview["preview"],
                "name": template_content["name"],
                "layout": template_content["layout"],
                "visible_to_exporter": template_content["visible_to_exporter"],
                "include_digital_signature": template_content["include_digital_signature"],
                "case_types": template_content["case_types"],
                "decisions": template_content["decisions"],
                "letter_paragraphs": template_content["letter_paragraphs"],
            },
        )

    @staticmethod
    def _remove_letter_paragraph(template_content):
        pk_to_delete = template_content["action"].split(".")[1]
        template_content["letter_paragraphs"].remove(pk_to_delete)

    def post(self, request):
        template_content = get_template_content(request)
        if template_content["action"].lower() == "add_letter_paragraph":
            return self._add_letter_paragraph(request, template_content)
        elif template_content["action"].lower() == "preview":
            return self._preview(request, template_content)
        elif "delete" in template_content["action"].lower():
            self._remove_letter_paragraph(template_content)
        return get_order_paragraphs_page(request, template_content)
