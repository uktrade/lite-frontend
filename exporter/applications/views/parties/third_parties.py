from django.shortcuts import render
from django.shortcuts import reverse
from django.views.generic import TemplateView

from exporter.applications.forms.third_party import third_party_forms
from exporter.applications.services import get_application, post_party, delete_party, validate_party
from exporter.applications.views.parties.base import AddParty, CopyParties, SetParty, DeleteParty, CopyAndSetParty
from exporter.core.constants import F680
from lite_content.lite_exporter_frontend.applications import ThirdPartyForm, ThirdPartyPage

from core.auth.views import LoginRequiredMixin


class ThirdParties(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        context = {
            "application": application,
            "third_parties": application["third_parties"],
            "has_clearance": application["case_type"]["sub_type"]["key"] == F680,
        }
        return render(request, "applications/parties/third-parties.html", context)


class AddThirdParty(LoginRequiredMixin, AddParty):
    def __init__(self):
        super().__init__(new_url="applications:set_third_party", copy_url="applications:third_parties_copy")

    @property
    def back_url(self):
        return reverse("applications:task_list", kwargs={"pk": self.kwargs["pk"]}) + "#third-parties"


class SetThirdParty(LoginRequiredMixin, SetParty):
    def __init__(self):
        super().__init__(
            url="applications:third_party_attach_document",
            party_type="third_party",
            form=third_party_forms,
            back_url="applications:add_third_party",
            strings=ThirdPartyForm,
            validate_action=validate_party,
            post_action=post_party,
        )

    def on_submission(self, request, **kwargs):
        application = get_application(request, self.object_pk)
        has_clearance = application["case_type"]["sub_type"]["key"] == F680
        if not has_clearance:
            self.forms = self.form(request, application, self.strings, self.back_url)

        if int(self.request.POST.get("form_pk")) == len(self.forms.forms) - 1:
            self.action = self.post_action
        else:
            self.action = self.validate_action


class RemoveThirdParty(LoginRequiredMixin, DeleteParty):
    def __init__(self, **kwargs):
        super().__init__(
            url="applications:third_parties",
            action=delete_party,
            error=ThirdPartyPage.DELETE_ERROR,
            **kwargs,
        )


class CopyThirdParties(LoginRequiredMixin, CopyParties):
    def __init__(self):
        super().__init__(new_party_type="third_party")


class CopyThirdParty(LoginRequiredMixin, CopyAndSetParty):
    def __init__(self):
        super().__init__(
            url="applications:third_party_attach_document",
            party_type="third_party",
            form=third_party_forms,
            back_url="applications:add_third_party",
            strings=ThirdPartyForm,
            validate_action=validate_party,
            post_action=post_party,
        )

    def on_submission(self, request, **kwargs):
        application = get_application(request, self.object_pk)
        has_clearance = application["case_type"]["sub_type"]["key"] == F680
        if not has_clearance:
            self.forms = self.form(request, application, self.strings, self.back_url)

        if int(self.request.POST.get("form_pk")) == len(self.forms.forms) - 1:
            self.action = self.post_action
        else:
            self.action = self.validate_action
