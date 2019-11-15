from django.shortcuts import render
from django.views.generic import TemplateView

from letter_templates.helpers import get_template_content, generate_preview
from letter_templates.services import get_letter_paragraphs
from picklists.services import get_picklists


def get_order_paragraphs_page(request, template_content):
    letter_paragraphs = get_letter_paragraphs(request, template_content["letter_paragraphs"])
    return render(
        request,
        "letter_templates/order_letter_paragraphs.html",
        {
            "letter_paragraphs": letter_paragraphs,
            "name": template_content["name"],
            "layout": template_content["layout"],
            "restricted_to": template_content["restricted_to"],
        },
    )


class LetterParagraphs(TemplateView):
    @staticmethod
    def _add_letter_paragraph(request, template_content):
        all_letter_paragraphs = get_picklists(request, "letter_paragraph")
        context = {
            "name": template_content["name"],
            "layout": template_content["layout"],
            "restricted_to": template_content["restricted_to"],
            "letter_paragraphs": [
                paragraph
                for paragraph in all_letter_paragraphs["picklist_items"]
                if paragraph["id"] not in template_content["letter_paragraphs"]
            ],
            "existing_letter_paragraphs": template_content["letter_paragraphs"],
        }
        return render(request, "letter_templates/add_letter_paragraphs.html", context)

    def _preview(self, request, template_content):
        """
        Display a preview once letter paragraphs have been selected and sorted.
        """
        letter_paragraphs = get_letter_paragraphs(request, template_content["letter_paragraphs"])
        preview = generate_preview(template_content["layout"]["filename"], letter_paragraphs)
        return render(
            request,
            "letter_templates/preview.html",
            {
                "preview": preview,
                "name": template_content["name"],
                "layout": template_content["layout"],
                "restricted_to": template_content["restricted_to"],
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
