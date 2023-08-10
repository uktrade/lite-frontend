from caseworker.cases.views.finalisation.forms import SelectInformLetterTemplateForm, TemplateTextForm
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


TEXT = "text"


class SelectInformTemplate(LoginRequiredMixin, FormView):
    template_name = "core/form.html"
    form_class = SelectInformLetterTemplateForm
    success_url = ""

    def letter_picklist_to_choices(self, picklist):
        picklist_choices = []
        for value in picklist:
            picklist_choices.append([value["id"], value["name"]])
        return picklist_choices
    
    
    def get_inform_letter_template_id(self, templates):
        for t in templates:
            if t['name'] == 'Inform letter':
                return t["id"]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        params = {"case": self.kwargs["pk"], "page": self.request.GET.get("page", 1), "decision": "refuse"}
        self.templates, _ = get_letter_templates(self.request, convert_dict_to_query_params(params))
        inform_template_id = self.get_inform_letter_template_id(self.templates["results"])
        template_details, status = get_letter_template(self.request, inform_template_id)

        kwargs["inform_paragraphs"] = self.letter_picklist_to_choices(template_details['paragraph_details'])
        return kwargs

    def form_valid(self, form):
        self.kwargs["paragraph_id"] = str(form.cleaned_data["select_template"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:inform_edit_text", kwargs=self.kwargs)


class SelectEditText(LoginRequiredMixin, FormView):
    template_name = "core/form.html"
    form_class = TemplateTextForm

    def get_picklist_text(self, id, picklist):
        for x in picklist:
            if x["id"] == id:
                return x["text"]

    def get_form_kwargs(self):
        paragraph_id = str(self.kwargs.pop("paragraph_id"))
        kwargs = super().get_form_kwargs()

        params = {"case": self.kwargs["pk"], "page": self.request.GET.get("page", 1), "decision": "refuse"}
        self.templates, _ = get_letter_templates(self.request, convert_dict_to_query_params(params))
        self.template_id = self.templates["results"][0]["id"]

        template_details, status = get_letter_template(self.request, self.template_id)

        kwargs["text"] = self.get_picklist_text(paragraph_id, template_details['paragraph_details'])
        return kwargs

    def form_valid(self, form):
        self.kwargs["tpk"] = self.template_id
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
            {"preview": preview["preview"], TEXT: text, "addressee": addressee, "kwargs": self.kwargs},
        )
