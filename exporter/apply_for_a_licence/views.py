from django.urls import reverse_lazy, reverse
from django.views.generic import (
    FormView,
    TemplateView,
)

from exporter.applications.services import post_applications, post_open_general_licences_applications
from exporter.apply_for_a_licence.forms.open_general_licences import (
    open_general_licence_forms,
    open_general_licence_submit_success_page,
)

from exporter.apply_for_a_licence.forms.triage_questions import (
    LicenceTypeForm,
    export_licence_questions,
    transhipment_questions,
)
from exporter.apply_for_a_licence.validators import validate_open_general_licences
from exporter.core.constants import PERMANENT, CaseTypes
from exporter.core.services import post_open_general_licence_cases
from lite_forms.views import MultiFormView

from core.auth.views import LoginRequiredMixin, RedirectView
from exporter.f680.views import F680FeatureRequiredMixin


class LicenceType(LoginRequiredMixin, FormView):
    form_class = LicenceTypeForm
    template_name = "core/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        self.licence_type = form.cleaned_data["licence_type"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(f"apply_for_a_licence:{self.licence_type}_questions")


class ExportLicenceQuestions(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.forms = export_licence_questions(request, None)

    def get_action(self):
        if self.request.POST.get("application_type") == CaseTypes.OGEL:
            return post_open_general_licences_applications
        else:
            return post_applications

    def on_submission(self, request, **kwargs):
        copied_req = request.POST.copy()
        self.forms = export_licence_questions(
            request, copied_req.get("application_type"), copied_req.get("goodstype_category")
        )

    def get_success_url(self):
        if self.request.POST.get("application_type") == CaseTypes.OGEL:
            return reverse_lazy("apply_for_a_licence:ogl_questions", kwargs={"ogl": CaseTypes.OGEL})
        else:
            pk = self.get_validated_data()["id"]
            return reverse_lazy("applications:task_list", kwargs={"pk": pk})


class F680Questions(LoginRequiredMixin, RedirectView, F680FeatureRequiredMixin):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("f680:apply")


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
