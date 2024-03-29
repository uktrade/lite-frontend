from http import HTTPStatus
from urllib.parse import quote

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, View

from caseworker.cases.forms.generate_document import (
    select_template_form,
    edit_document_text_form,
    select_addressee_form,
)
from caseworker.cases.helpers.helpers import generate_document_error_page
from caseworker.cases.services import (
    post_generated_document,
    send_generated_document,
    get_generated_document_preview,
    get_generated_document,
    get_case,
    get_case_additional_contacts,
    get_case_applicant,
)
from core.helpers import check_url, convert_dict_to_query_params
from caseworker.letter_templates.services import get_letter_template, get_letter_templates
from lite_content.lite_internal_frontend import letter_templates
from lite_forms.components import FormGroup
from lite_forms.views import SingleFormView, MultiFormView

from core.auth.views import LoginRequiredMixin


TEXT = "text"
TEMPLATE = "template"


class GenerateDocument(MultiFormView):
    contacts: []
    templates: []
    applicant: {}
    template: str
    back_url: str

    @staticmethod
    def _validate(request, pk, json):
        if not json.get(TEMPLATE):
            return (
                {"errors": {TEMPLATE: [letter_templates.LetterTemplatesPage.PickTemplate.NO_TEMPLATE_SELECTED]}},
                HTTPStatus.BAD_REQUEST,
            )
        return json, HTTPStatus.OK

    def get_forms(self):
        if self.contacts:
            return FormGroup(
                [
                    select_template_form(self.templates, self.back_url),
                    select_addressee_form(),
                    edit_document_text_form(
                        {"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"], "tpk": self.template},
                        post_url="cases:generate_document_preview",
                    ),
                ]
            )
        else:
            return FormGroup(
                [
                    select_template_form(self.templates, self.back_url),
                    edit_document_text_form(
                        {"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"], "tpk": self.template},
                        post_url="cases:generate_document_preview",
                    ),
                ]
            )

    def init(self, request, **kwargs):
        self.back_url = reverse_lazy(
            "cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"], "tab": "documents"}
        )
        self.contacts = get_case_additional_contacts(request, kwargs["pk"])
        self.applicant = get_case_applicant(request, kwargs["pk"])

        self.template = request.POST.get(TEMPLATE)

        params = {"case": self.kwargs["pk"], "page": self.request.GET.get("page", 1)}
        if self.kwargs.get("decision_key"):
            params["decision"] = self.kwargs["decision_key"]
        self.templates, _ = get_letter_templates(self.request, convert_dict_to_query_params(params))
        self.data = {"total_pages": self.templates["total_pages"]}

        if self.template and not request.POST.get(TEXT):
            template, _ = get_letter_template(request, self.template, params=convert_dict_to_query_params({TEXT: True}))
            self.data[TEXT] = template[TEXT]

        self.object_pk = kwargs["pk"]
        self.action = self._validate
        self.additional_context = {
            "case": get_case(request, self.object_pk),
            "applicant": self.applicant,
            "contacts": self.contacts,
        }


class GenerateDecisionDocument(LoginRequiredMixin, GenerateDocument):
    def get_forms(self):
        self.back_url = reverse_lazy(
            "cases:finalise_documents", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]}
        )
        return FormGroup(
            [
                select_template_form(self.templates, back_url=self.back_url),
                edit_document_text_form(
                    {
                        "queue_pk": self.kwargs["queue_pk"],
                        "pk": self.kwargs["pk"],
                        "tpk": self.template,
                        "decision_key": self.kwargs["decision_key"],
                    },
                    post_url="cases:finalise_document_preview",
                ),
            ]
        )


class RegenerateExistingDocument(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        document, _ = get_generated_document(request, str(kwargs["pk"]), str(kwargs["dpk"]))
        template = document["template"]
        self.data = {TEXT: document.get(TEXT)}
        self.object_pk = kwargs["pk"]
        self.form = edit_document_text_form(
            {"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"], "tpk": template},
            post_url="cases:generate_document_preview",
        )
        self.context = {"case": get_case(request, self.object_pk)}


class PreviewViewDocument(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        document, _ = get_generated_document(request, str(kwargs["pk"]), str(kwargs["dpk"]))
        template = document["template"]
        text = document.get(TEXT)
        self.object_pk = kwargs["pk"]
        addressee = request.POST.get("addressee", "")
        self.kwargs["tpk"] = template
        self.kwargs["dpk"] = kwargs["dpk"]

        preview, status_code = get_generated_document_preview(
            request, self.object_pk, template=template, text=quote(text), addressee=addressee
        )

        if status_code == 400:
            return generate_document_error_page()

        return render(
            request,
            "generated-documents/preview-view.html",
            {"preview": preview["preview"], TEXT: text, "addressee": "", "kwargs": self.kwargs},
        )


class PreviewDocument(LoginRequiredMixin, TemplateView):
    def post(self, request, **kwargs):
        template_id = str(kwargs["tpk"])
        case_id = str(kwargs["pk"])
        addressee = request.POST.get("addressee", "")
        text = request.POST.get(TEXT)

        preview, status_code = get_generated_document_preview(
            request, case_id, template=template_id, text=quote(text), addressee=addressee
        )
        if status_code == 400:
            return generate_document_error_page()

        return render(
            self.request,
            "generated-documents/preview.html",
            {"preview": preview["preview"], "text": text, "addressee": addressee, "kwargs": self.kwargs},
        )


class CreateDocument(LoginRequiredMixin, TemplateView):
    def post(self, request, queue_pk, pk, tpk):
        text = request.POST.get(TEXT)
        status_code = post_generated_document(
            request,
            str(pk),
            {"template": str(tpk), TEXT: text, "addressee": request.POST.get("addressee"), "visible_to_exporter": True},
        )
        if status_code != HTTPStatus.CREATED:
            return generate_document_error_page()
        else:
            return redirect(
                reverse_lazy("cases:case", kwargs={"queue_pk": queue_pk, "pk": str(pk), "tab": "documents"})
            )


class SendExistingDocument(LoginRequiredMixin, View):
    def get_success_message(self, send_response, case):
        if send_response.json()["document"]["advice_type"] == "inform":
            return f"Inform letter sent to {case['data']['organisation']['name']}, {case['reference_code']}"
        return f"Document sent to {case['data']['organisation']['name']}, {case['reference_code']}"

    def post(self, request, queue_pk, pk, document_pk):
        response = send_generated_document(request, pk, document_pk)
        case = get_case(request, pk)
        if response.ok:
            success_message = self.get_success_message(response, case)
            messages.success(self.request, success_message)
        else:
            messages.error(
                self.request,
                f"An error occurred when sending the document. Please try again later",
            )
        return redirect(reverse("queues:cases", kwargs={"queue_pk": queue_pk}))


class CreateDocumentFinalAdvice(LoginRequiredMixin, TemplateView):
    def post(self, request, queue_pk, pk, decision_key, tpk):
        text = request.POST.get(TEXT)
        status_code = post_generated_document(
            request,
            str(pk),
            {"template": str(tpk), TEXT: text, "visible_to_exporter": False, "advice_type": decision_key},
        )

        if status_code != HTTPStatus.CREATED:
            return generate_document_error_page()
        if request.POST.get("return_url"):
            return redirect(check_url(request, request.POST["return_url"]))

        return redirect(reverse_lazy("cases:finalise_documents", kwargs={"queue_pk": queue_pk, "pk": pk}))
