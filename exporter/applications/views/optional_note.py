from django.urls import reverse

from exporter.applications.forms.hmrc import query_explanation_form
from exporter.applications.services import get_application, put_application
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


class ApplicationOptionalNote(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_application(request, self.object_pk)
        self.form = query_explanation_form(self.object_pk)
        self.action = put_application
        self.success_url = reverse("applications:task_list", kwargs={"pk": self.object_pk})
