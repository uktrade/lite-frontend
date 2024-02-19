from http import HTTPStatus

from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import TemplateView

from lite_content.lite_internal_frontend.cases import CasesListPage
from core.views import error_page

from core.auth.views import LoginRequiredMixin

from caseworker.queues import forms
from caseworker.queues.services import (
    get_enforcement_xml,
    post_enforcement_xml,
)


class EnforcementXMLExport(LoginRequiredMixin, TemplateView):
    def get(self, request, pk):
        data, status_code = get_enforcement_xml(request, pk)

        if status_code == HTTPStatus.NO_CONTENT:
            return error_page(request, CasesListPage.EnforcementXML.Export.NO_CASES)
        elif status_code != HTTPStatus.OK:
            return error_page(request, CasesListPage.EnforcementXML.Export.GENERIC_ERROR)
        else:
            return data


class EnforcementXMLImport(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "queues/enforcement-xml-import.html"
    form_class = forms.EnforcementXMLImportForm
    success_message = "Enforcement XML imported successfully"

    def form_valid(self, form):
        response = post_enforcement_xml(request=self.request, queue_pk=self.kwargs["pk"], json=form.cleaned_data)
        if not response.ok:
            for key, errors in response.json()["errors"].items():
                for error in errors:
                    form.add_error(key, error)
            return self.form_invalid(form)
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return self.request.get_full_path()
