from django.urls import reverse_lazy, reverse
from django.views.generic import (
    FormView,
    TemplateView,
)

from lite_forms.views import MultiFormView

from exporter.applications.services import post_applications
from exporter.applications.licence_type_processors import ExportLicenceLicenceTypeProcessor
from exporter.apply_for_a_licence.forms.open_general_licences import (
    open_general_licence_forms,
    open_general_licence_submit_success_page,
)
from exporter.apply_for_a_licence.enums import LicenceType
from exporter.apply_for_a_licence.forms.triage_questions import (
    LicenceTypeForm,
    transhipment_questions,
)
from exporter.apply_for_a_licence.validators import validate_open_general_licences
from exporter.core.constants import PERMANENT, CaseTypes
from exporter.core.services import post_open_general_licence_cases
from exporter.f680.licence_type_processors import F680LicenceLicenceTypeProcessor

from core.auth.views import LoginRequiredMixin


class LicenceTypeView(LoginRequiredMixin, FormView):
    form_class = LicenceTypeForm
    template_name = "core/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        licence_type = form.cleaned_data["licence_type"]

        LicenceTypeProcessor = {
            LicenceType.EXPORT_LICENCE: ExportLicenceLicenceTypeProcessor,
            LicenceType.F680: F680LicenceLicenceTypeProcessor,
        }[licence_type]

        licence_type_processor = LicenceTypeProcessor(self.request)

        return licence_type_processor.process()

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx["back_link_url"] = reverse("core:home")

        return ctx


class TranshipmentQuestions(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.forms = transhipment_questions(request)
        self.action = post_applications
        self.data = {"export_type": PERMANENT}

    def get_success_url(self):
        if self.request.POST.get("application_type") == CaseTypes.OGTL:
            return reverse_lazy("apply_for_a_licence:ogl_questions", kwargs={"ogl": CaseTypes.OGTL})
        else:
            pk = self.get_validated_data()["id"]
            return reverse_lazy("applications:task_list", kwargs={"pk": pk})


class OpenGeneralLicenceQuestions(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.forms = open_general_licence_forms(request, **kwargs)
        self.action = validate_open_general_licences

    def get_success_url(self):
        post_open_general_licence_cases(self.request, self.get_validated_data())
        return (
            reverse(
                "apply_for_a_licence:ogl_submit",
                kwargs={"ogl": self.kwargs["ogl"], "pk": self.get_validated_data()["open_general_licence"]},
            )
            + "?animate=True"
        )


class OpenGeneralLicenceSubmit(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return open_general_licence_submit_success_page(request, **kwargs)
