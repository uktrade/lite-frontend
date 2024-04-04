from django.urls import reverse_lazy

from exporter.applications.forms.f680_details import f680_details_form
from exporter.applications.services import put_application_with_clearance_types, get_application
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


class F680Details(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        application = get_application(request, self.object_pk)
        self.form = f680_details_form(request, self.object_pk)
        self.action = put_application_with_clearance_types
        clearances = application["clearances"] or []
        self.data = {"clearances": [f680_clearance_type["key"] for f680_clearance_type in clearances]}
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
