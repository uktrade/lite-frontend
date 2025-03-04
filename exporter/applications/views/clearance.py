from django.urls import reverse_lazy

from exporter.applications.components import back_to_task_list
from exporter.applications.services import put_application, get_application
from exporter.core.services import get_pv_gradings
from lite_content.lite_exporter_frontend.applications import ClearanceLevel
from lite_forms.components import Form, RadioButtons
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


def clearance_level_form(application_id, options):
    return Form(
        title=ClearanceLevel.TITLE,
        description="",
        questions=[RadioButtons(name="clearance_level", options=options)],
        back_link=back_to_task_list(application_id),
    )


class SetClearanceLevel(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        pv_grading_options = get_pv_gradings(request, convert_to_options=True)
        self.form = clearance_level_form(application_id=kwargs["pk"], options=pv_grading_options)
        self.action = put_application
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
        application = get_application(request, self.object_pk)
        self.data = {"clearance_level": application["clearance_level"]}
