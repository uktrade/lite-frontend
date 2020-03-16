from http import HTTPStatus

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.components import BackLink

from cases.forms.generate_document import select_template_form, edit_document_text_form, add_paragraphs_form
from cases.services import post_generated_document, get_generated_document_preview, get_generated_document
from core.helpers import convert_dict_to_query_params
from letter_templates.services import get_letter_templates, get_letter_template
from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_forms.generators import form_page, error_page
from lite_forms.views import SingleFormView
from picklists.services import get_picklists


TEXT = "text"


class SelectTemplate(TemplateView):
    def get(self, request, pk):
        page = request.GET.get("page")
        if not page:
            page = 1
        templates, _ = get_letter_templates(request, convert_dict_to_query_params({"case": pk, "page": page}))
        return form_page(request, select_template_form(templates["results"], templates["total_pages"], pk))

    def post(self, request, **kwargs):
        template_id = request.POST.get("template")
        if template_id:
            return redirect(
                reverse_lazy("cases:generate_document_edit", kwargs={"pk": str(kwargs["pk"]), "tpk": template_id})
            )
        else:
            return redirect(reverse_lazy("cases:generate_document", kwargs={"pk": str(kwargs["pk"])}))


class EditDocumentText(SingleFormView):
    @staticmethod
    def _convert_text_list_to_str(request, json):
        json[TEXT] = "\n\n".join(json[TEXT])
        return json, HTTPStatus.OK

    def init(self, request, pk, tpk):
        case_id = str(pk)
        template_id = str(tpk)
        keys = {"pk": case_id, "tpk": template_id}
        backlink = BackLink(
            text=GenerateDocumentsPage.EditTextForm.BACK_LINK,
            url=reverse_lazy("cases:generate_document", kwargs={"pk": case_id}),
        )

        # If regenerating, get existing text for a given document ID
        if "document_id" in request.GET:
            document, _ = get_generated_document(request, case_id, request.GET["document_id"])
            self.data = {TEXT: document[TEXT]}
            backlink = BackLink(
                text=GenerateDocumentsPage.EditTextForm.BACK_LINK_REGENERATE,
                url=reverse_lazy("cases:documents", kwargs={"pk": case_id}),
            )

        # if not returning to this page from adding paragraphs (going to page first time) get template text
        elif TEXT not in request.POST:
            paragraph_text = get_letter_template(
                request, template_id, params=convert_dict_to_query_params({TEXT: True})
            )[0][TEXT]
            self.data = {TEXT: paragraph_text}

        self.form = edit_document_text_form(backlink, keys)
        self.redirect = False
        self.action = self._convert_text_list_to_str


class RegenerateExistingDocument(TemplateView):
    def get(self, request, pk, dpk):
        case_id = str(pk)
        document_id = str(dpk)
        document, status_code = get_generated_document(request, case_id, document_id)
        if status_code != HTTPStatus.OK:
            return redirect(reverse_lazy("cases:documents", kwargs={"pk": case_id}))

        return redirect(
            reverse_lazy("cases:generate_document_edit", kwargs={"pk": case_id, "tpk": document["template"]})
            + "?document_id="
            + document_id
        )


class AddDocumentParagraphs(SingleFormView):
    @staticmethod
    def _get_form_data(request, json):
        return json, HTTPStatus.OK

    def init(self, request, **kwargs):
        letter_paragraphs = get_picklists(request, "letter_paragraph")["picklist_items"]
        case_id = str(kwargs["pk"])
        template_id = str(kwargs["tpk"])

        self.form = add_paragraphs_form(letter_paragraphs, request.POST[TEXT], {"pk": case_id, "tpk": template_id})
        self.redirect = False
        self.action = self._get_form_data


def _error_page():
    return error_page(
        None, title=GenerateDocumentsPage.TITLE, description=GenerateDocumentsPage.ERROR, show_back_link=True,
    )


class PreviewDocument(TemplateView):
    def post(self, request, pk, tpk):
        template_id = str(tpk)
        case_id = str(pk)

        text = request.POST.get(TEXT)
        if not text:
            return _error_page()

        preview, status_code = get_generated_document_preview(request, case_id, template_id, text=text)
        if status_code == 400:
            return _error_page()

        return render(
            request,
            "generated-documents/preview.html",
            {"preview": preview["preview"], TEXT: text, "pk": case_id, "tpk": template_id},
        )


class CreateDocument(TemplateView):
    def post(self, request, **kwargs):
        text = request.POST.get(TEXT)
        if not text:
            return _error_page()

        template_id = str(kwargs["tpk"])
        case_id = str(kwargs["pk"])
        status_code = post_generated_document(request, case_id, {"template": template_id, TEXT: text})
        if status_code != HTTPStatus.CREATED:
            return _error_page()
        else:
            return redirect(reverse_lazy("cases:documents", kwargs={"pk": case_id}))
