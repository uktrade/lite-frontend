from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.end_user import new_party_form_group
from applications.helpers.check_your_answers import convert_end_user
from applications.helpers.validate_status import check_all_parties_have_a_document
from applications.services import (
    get_application,
    post_end_user,
    get_ultimate_end_users,
    post_ultimate_end_user,
    delete_ultimate_end_user,
    delete_end_user,
)
from lite_forms.generators import form_page, error_page
from lite_forms.submitters import submit_paged_form
from lite_forms.views import MultiFormView
from lite_content.lite_exporter_frontend.applications import UltimateEndUserForm, EndUserForm


class EndUser(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        if application["end_user"]:
            context = {
                "application": application,
                "title": "End user",
                "edit_url": reverse_lazy("applications:set_end_user", kwargs={"pk": application_id}),
                "remove_url": reverse_lazy("applications:remove_end_user", kwargs={"pk": application_id}),
                "answers": convert_end_user(application["end_user"], application_id, True),
                "highlight": ["Document"] if not application["end_user"]["document"] else {},
            }
            return render(request, "applications/check-your-answer.html", context)
        else:
            return redirect(reverse_lazy("applications:set_end_user", kwargs={"pk": application_id}))


class SetEndUser(MultiFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.data = application["end_user"]
        self.forms = new_party_form_group(application, EndUserForm)
        self.action = post_end_user
        self.success_url = reverse_lazy("applications:end_user_attach_document", kwargs={"pk": self.object_pk})


class RemoveEndUser(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        status_code = delete_end_user(request, application_id)

        if status_code != 204:
            return error_page(request, "Unexpected error removing end user")

        return redirect(reverse_lazy("applications:task_list", kwargs={"pk": application_id}))


class UltimateEndUsers(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        ultimate_end_users = get_ultimate_end_users(request, application_id)

        context = {
            "application": application,
            "ultimate_end_users": ultimate_end_users,
            "show_warning": check_all_parties_have_a_document(ultimate_end_users) == "in_progress",
        }
        return render(request, "applications/parties/ultimate-end-users.html", context)


class AddUltimateEndUser(TemplateView):
    draft_id = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.draft_id = str(kwargs["pk"])
        application = get_application(request, self.draft_id)
        self.form = new_party_form_group(application, UltimateEndUserForm)

        return super(AddUltimateEndUser, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.form, post_ultimate_end_user, object_pk=self.draft_id)

        if response:
            return response

        return redirect(
            reverse_lazy(
                "applications:ultimate_end_user_attach_document",
                kwargs={"pk": self.draft_id, "obj_pk": data["ultimate_end_user"]["id"]},
            )
        )


class RemoveUltimateEndUser(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        obj_pk = str(kwargs["obj_pk"])
        delete_ultimate_end_user(request, draft_id, obj_pk)
        return redirect(reverse_lazy("applications:ultimate_end_users", kwargs={"pk": draft_id}))
