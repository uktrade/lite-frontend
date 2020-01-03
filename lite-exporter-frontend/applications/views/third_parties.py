from http import HTTPStatus

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.third_party import third_party_forms
from applications.helpers.check_your_answers import convert_consignee
from applications.services import (
    post_third_party,
    delete_third_party,
    post_consignee,
    get_application,
    delete_consignee,
)
from lite_forms.generators import form_page, error_page
from lite_forms.submitters import submit_paged_form
from lite_forms.views import MultiFormView
from applications.forms.end_user import new_party_form_group
from lite_content.lite_exporter_frontend.applications import ConsigneeForm


class AddThirdParty(TemplateView):
    application_id = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs["pk"])
        application = get_application(request, self.application_id)
        self.form = third_party_forms(application)

        return super(AddThirdParty, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.form, post_third_party, object_pk=self.application_id)

        if response:
            return response

        return redirect(
            reverse_lazy(
                "applications:third_party_attach_document",
                kwargs={"pk": self.application_id, "obj_pk": data["third_party"]["id"]},
            )
        )


class ThirdParties(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        context = {
            "application": application,
            "third_parties": application["third_parties"],
        }
        return render(request, "applications/parties/third-parties.html", context)


class RemoveThirdParty(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        obj_pk = str(kwargs["obj_pk"])
        delete_third_party(request, draft_id, obj_pk)
        return redirect(reverse_lazy("applications:third_parties", kwargs={"pk": draft_id}))


class Consignee(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        if application["consignee"]:
            context = {
                "application": application,
                "title": "Consignee",
                "edit_url": reverse_lazy("applications:set_consignee", kwargs={"pk": application_id}),
                "remove_url": reverse_lazy("applications:remove_consignee", kwargs={"pk": application_id}),
                "answers": convert_consignee(application["consignee"], application_id, True),
            }
            return render(request, "applications/check-your-answer.html", context)
        else:
            return redirect(reverse_lazy("applications:set_consignee", kwargs={"pk": application_id}))


class SetConsignee(MultiFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.data = application["consignee"]
        self.forms = new_party_form_group(application, ConsigneeForm)
        self.action = post_consignee
        self.success_url = reverse_lazy("applications:consignee_attach_document", kwargs={"pk": self.object_pk})


class RemoveConsignee(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        status_code = delete_consignee(request, application_id)

        if status_code != HTTPStatus.NO_CONTENT:
            return error_page(request, "Unexpected error removing consignee")

        return redirect(reverse_lazy("applications:task_list", kwargs={"pk": application_id}))
