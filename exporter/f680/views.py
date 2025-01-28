from http import HTTPStatus

from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.wizard.views import BaseSessionWizardView

from .constants import (
    ApplicationFormSteps,
)
from .forms import (
    ApplicationNameForm,
    ApplicationPreviousApplicationForm,
)
from .payloads import (
    F680CreatePayloadBuilder,  # PS-IGNORE
)
from .services import (
    post_f680_application,
)


class F680ApplicationCreateView(LoginRequiredMixin, BaseSessionWizardView):  # PS-IGNORE
    form_list = [
        (ApplicationFormSteps.APPLICATION_NAME, ApplicationNameForm),
        (ApplicationFormSteps.PREVIOUS_APPLICATION, ApplicationPreviousApplicationForm),
    ]

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating F680 application",  # PS-IGNORE
        "Unexpected error creating F680 application",
    )
    def post_f680_application(self, data):
        return post_f680_application(self.request, data)  # PS-IGNORE

    def get_success_url(self, application_id):
        return reverse(
            "f680:summary",  # PS-IGNORE
            kwargs={
                "pk": application_id,
            },
        )

    def get_payload(self, form_dict):
        return F680CreatePayloadBuilder(self).build(form_dict)  # PS-IGNORE

    def done(self, form_list, form_dict, **kwargs):
        data = self.get_payload(form_dict)
        response_data, _ = self.post_f680_application(data)  # PS-IGNORE
        return redirect(self.get_success_url(response_data["id"]))
