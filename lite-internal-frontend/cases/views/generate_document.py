from http import HTTPStatus

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from cases.forms.generate_document import select_template_form, edit_document_text_form
from cases.helpers.helpers import generate_document_error_page
from cases.services import (
    post_generated_document,
    get_generated_document_preview,
    get_generated_document,
    get_case,
)
from core.helpers import convert_dict_to_query_params
from letter_templates.services import get_letter_templates, get_letter_template
from lite_content.lite_internal_frontend.cases import GenerateDocumentsPage
from lite_forms.components import BackLink
from lite_forms.generators import form_page
from lite_forms.views import SingleFormView

TEXT = "text"


class PickTemplateView(TemplateView):
    def __init__(self, decision, back_url, success_url, back_text):
        super().__init__()
        self.decision = decision
        self.back_url = back_url
        self.success_url = success_url
        self.back_text = back_text

    def get(self, request, **kwargs):
        pk = kwargs["pk"]
        case = get_case(request, pk)
        page = request.GET.get("page", 1)
        params = {"case": pk, "page": page}
        if self.decision:
            params["decision"] = kwargs.get("decision_key")
        templates, _ = get_letter_templates(request, convert_dict_to_query_params(params))
        back_link = BackLink(url=reverse_lazy(self.back_url, kwargs={"queue_pk": kwargs["queue_pk"], "pk": pk}))
        return form_page(
            request,
            select_template_form(templates["results"], templates, back_link=back_link),
            data=templates,
            extra_data={"case": case},
        )

    def post(self, request, **kwargs):
        template_id = request.POST.get("template")
        if template_id:
            kwargs["tpk"] = template_id
            return redirect(reverse_lazy(self.success_url, kwargs=kwargs))
        else:
            return HttpResponseRedirect(request.path_info)


class SelectTemplate(PickTemplateView):
    def __init__(self):
        decision = False
        back_text = GenerateDocumentsPage.SelectTemplateForm.BACK_LINK
        back_url = "cases:case"
        success_url = "cases:generate_document_edit"
        super().__init__(decision, back_url, success_url, back_text)


class SelectTemplateFinalAdvice(PickTemplateView):
    def __init__(self):
        decision = True
        back_text = "Back to Final Advice"
        back_url = "cases:finalise_documents"
        success_url = "cases:finalise_document_edit_text"
        super().__init__(decision, back_url, success_url, back_text)


class EditDocumentTextView(SingleFormView):
    def __init__(self, back_url, post_url, back_text):
        super().__init__()
        self.back_url = back_url
        self.post_url = post_url
        self.back_text = back_text

    @staticmethod
    def _convert_text_list_to_str(request, json):
        json[TEXT] = "\n\n".join(json[TEXT])
        return json, HTTPStatus.OK

    def init(self, request, **kwargs):
        case_id = kwargs["pk"]
        template_id = kwargs["tpk"]
        # Remove tpk ID kwarg
        back_link_kwargs = kwargs.copy()
        back_link_kwargs.pop("tpk", None)
        backlink = BackLink(text=self.back_text, url=reverse_lazy(self.back_url, kwargs=back_link_kwargs),)
        case = get_case(request, case_id)

        # If regenerating, get existing text for a given document ID
        if "document_id" in request.GET:
            document, _ = get_generated_document(request, case_id, request.GET["document_id"])
            self.data = {TEXT: document[TEXT]}
            backlink = BackLink(
                text=GenerateDocumentsPage.EditTextForm.BACK_LINK_REGENERATE,
                url=reverse_lazy(
                    "cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case_id, "tab": "documents"}
                ),
            )

        # if not returning to this page from adding paragraphs (going to page first time) get template text
        elif TEXT not in request.POST:
            paragraph_text = get_letter_template(
                request, str(template_id), params=convert_dict_to_query_params({TEXT: True})
            )[0][TEXT]
            self.data = {TEXT: paragraph_text}

        self.context = {"case": case}
        self.form = edit_document_text_form(request, backlink, kwargs, self.post_url)
        self.redirect = False
        self.action = self._convert_text_list_to_str


class EditDocumentText(EditDocumentTextView):
    def __init__(self):
        back_url = "cases:generate_document"
        post_url = "cases:generate_document_preview"
        back_text = GenerateDocumentsPage.EditTextForm.BACK_LINK
        super().__init__(back_url, post_url, back_text)


class EditTextFinalAdvice(EditDocumentTextView):
    def __init__(self):
        back_url = "cases:finalise_document_template"
        post_url = "cases:finalise_document_preview"
        back_text = GenerateDocumentsPage.EditTextForm.BACK_LINK
        super().__init__(back_url, post_url, back_text)


class RegenerateExistingDocument(TemplateView):
    def get(self, request, queue_pk, pk, dpk):
        case_id = str(pk)
        document_id = str(dpk)
        document, status_code = get_generated_document(request, case_id, document_id)
        if status_code != HTTPStatus.OK:
            return redirect(
                reverse_lazy(
                    "cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": case_id, "tab": "documents"}
                )
            )

        return redirect(
            reverse_lazy(
                "cases:generate_document_edit",
                kwargs={"queue_pk": queue_pk, "pk": case_id, "tpk": document["template"]},
            )
            + "?document_id="
            + document_id
        )


class PreviewDocument(TemplateView):
    def post(self, request, **kwargs):
        template_id = str(kwargs["tpk"])
        case_id = str(kwargs["pk"])

        text = request.POST.get(TEXT)
        if not text:
            return generate_document_error_page()

        preview, status_code = get_generated_document_preview(request, case_id, template_id, text=text)
        if status_code == 400:
            return generate_document_error_page()

        return render(
            request, "generated-documents/preview.html", {"preview": preview["preview"], TEXT: text, "kwargs": kwargs},
        )


class CreateDocument(TemplateView):
    def post(self, request, queue_pk, pk, tpk):
        text = request.POST.get(TEXT)
        if not text:
            return generate_document_error_page()

        status_code = post_generated_document(
            request, str(pk), {"template": str(tpk), TEXT: text, "visible_to_exporter": True}
        )
        if status_code != HTTPStatus.CREATED:
            return generate_document_error_page()
        else:
            return redirect(
                reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": str(pk), "tab": "documents"})
            )


class CreateDocumentFinalAdvice(TemplateView):
    def post(self, request, queue_pk, pk, decision_key, tpk):
        text = request.POST.get(TEXT)
        if not text:
            return generate_document_error_page()

        status_code = post_generated_document(
            request,
            str(pk),
            {"template": str(tpk), TEXT: text, "visible_to_exporter": False, "advice_type": decision_key},
        )
        if status_code != HTTPStatus.CREATED:
            return generate_document_error_page()
        else:
            return redirect(reverse_lazy("cases:finalise_documents", kwargs={"queue_pk": queue_pk, "pk": pk}))
