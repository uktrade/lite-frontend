from django.urls import reverse_lazy

from applications.forms.f680_details import f680_details_form
from applications.services import put_application_with_clearance_types, get_application
from lite_forms.views import SingleFormView


class F680Details(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        application = get_application(request, self.object_pk)
        self.form = f680_details_form(request, self.object_pk)
        self.action = put_application_with_clearance_types
        self.data = {"types": [f680_clearance_type["name"]["key"] for f680_clearance_type in application["types"]]}
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
