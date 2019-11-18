from django.urls import reverse_lazy

from applications.forms.reference_name import reference_name_form
from applications.services import get_application, put_application
from lite_forms.views import SingleFormView


class ApplicationEditReferenceName(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_application(request, self.object_pk)
        self.form = reference_name_form(self.object_pk)
        self.action = put_application
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
