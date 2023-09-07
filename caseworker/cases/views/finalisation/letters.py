from caseworker.cases.views.finalisation.forms import SelectInformLetterTemplateForm, LetterEditTextForm
from urllib.parse import quote
from django.views.generic import FormView
from caseworker.letter_templates.services import get_letter_templates, get_letter_template

from core.auth.views import LoginRequiredMixin
from core.helpers import convert_dict_to_query_params
from django.urls import reverse
from django.shortcuts import render
from caseworker.cases.helpers.helpers import generate_document_error_page
from caseworker.cases.services import (
    get_generated_document_preview,
)


class BaseLetter(LoginRequiredMixin, FormView):
    letter_type = None

    def letter_picklist_to_choices(self, picklist):
        picklist_choices = []
        for value in picklist:
            picklist_choices.append([value["id"], value["name"]])
        return picklist_choices

    def get_in_dict(self, values, key, id, return_key):
        for value in values:
            if value[key] == id:
                return value[return_key]
        raise KeyError(f"{key} not found in dict")

    def get_params(self):
        raise NotImplementedError("Implement `get_params` on {self.__class__.__name__}")

    def get_template_details(self, params):
        self.templates, _ = get_letter_templates(self.request, convert_dict_to_query_params(params))
        self.template_id = self.get_in_dict(self.templates["results"], "name", self.letter_type, "id")

        self.template_details, _ = get_letter_template(self.request, self.template_id)

    def get_form_kwargs(self):
        params = self.get_params()
        self.get_template_details(params)
        kwargs = super().get_form_kwargs()
        return kwargs


class SelectInformTemplate(BaseLetter):
    template_name = "core/form.html"
    form_class = SelectInformLetterTemplateForm
    letter_type = "Inform letter"

    def get_params(self):
        return {"case": self.kwargs["pk"], "page": self.request.GET.get("page", 1), "decision": "inform"}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["inform_paragraphs"] = self.letter_picklist_to_choices(self.template_details["paragraph_details"])
        return kwargs

    def form_valid(self, form):
        self.kwargs["paragraph_id"] = str(form.cleaned_data["select_template"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:select-edit-text", kwargs=self.kwargs)

    def get_back_link_url(self):
        case_id = str(self.kwargs["pk"])
        default_back_url = reverse(
            "cases:consolidate_view", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": case_id}
        )
        return self.request.GET.get("return_to", default_back_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.get_back_link_url()
        context["title"] = self.form_class.Layout.TITLE
        return context


class EditLetterText(BaseLetter):
    template_name = "case/edit-letter.html"
    form_class = LetterEditTextForm
    letter_type = "Inform letter"

    def get_params(self):
        return {"case": self.kwargs["pk"], "page": self.request.GET.get("page", 1), "decision": "inform"}

    def get_initial(self):
        initial = super().get_initial()
        paragraph_id = str(self.kwargs["paragraph_id"])
        text = self.get_in_dict(self.template_details["paragraph_details"], "id", paragraph_id, "text")
        initial["text"] = text
        return initial

    def form_valid(self, form):
        self.kwargs["tpk"] = self.template_id
        self.kwargs["decision_key"] = "inform"
        case_id = str(self.kwargs["pk"])
        addressee = self.kwargs.get("addressee", "")
        text = str(form.cleaned_data["text"])

        preview, status_code = get_generated_document_preview(
            self.request, case_id, template=self.template_id, text=quote(text), addressee=addressee
        )

        if status_code == 400:
            return generate_document_error_page()

        return render(
            self.request,
            "generated-documents/preview.html",
            {
                "preview": preview["preview"],
                "text": text,
                "addressee": addressee,
                "kwargs": self.kwargs,
                "return_url": reverse(
                    "cases:consolidate_view", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": case_id}
                ),
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.form_class.Layout.TITLE
        return context
