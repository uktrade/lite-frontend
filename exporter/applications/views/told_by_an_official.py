from django.urls import reverse_lazy

from exporter.applications.forms.edit import told_by_an_official_form
from exporter.applications.services import get_application, put_application
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


class ApplicationEditToldByAnOfficial(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_application(request, self.object_pk)
        self.form = told_by_an_official_form(self.object_pk)
        self.action = put_application
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
