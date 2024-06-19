from http import HTTPStatus

from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from exporter.applications.forms.declaration import ApplicationDeclarationForm
from exporter.applications.services import submit_application


class ApplicationDeclarationView(LoginRequiredMixin, FormView):
    form_class = ApplicationDeclarationForm
    template_name = "core/form.html"

    def dispatch(self, request, **kwargs):
        self.application_pk = kwargs["pk"]
        return super().dispatch(request, **kwargs)

    def get_summary_url(self):
        return reverse("applications:summary", kwargs={"pk": self.application_pk})

    def get_success_url(self):
        return reverse_lazy("applications:success_page", kwargs={"pk": self.application_pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "back_link_url": self.get_summary_url(),
                "back_link_text": self.form_class.Layout.BACK_LINK_TEXT,
                "form_title": self.form_class.Layout.TITLE,
            }
        )
        return context

    @expect_status(HTTPStatus.OK, "Error submitting application", "Unexpected error submitting application")
    def submit_application(self, request, application_pk, data):
        return submit_application(request, application_pk, json=data)

    def form_valid(self, form):
        data = form.cleaned_data
        # TODO: we should update lite-api so we can remove these extra fields
        data.update({"submit_declaration": True, "agreed_to_declaration_text": "I AGREE"})
        self.submit_application(self.request, self.application_pk, data)
        return super().form_valid(form)
