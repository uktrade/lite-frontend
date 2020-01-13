from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.parties import new_party_form_group
from applications.helpers.check_your_answers import convert_end_user
from applications.services import get_application, post_end_user, delete_end_user
from applications.views.parties.base import AddParty, SetParty, DeleteParty, ExistingPartiesList
from lite_content.lite_exporter_frontend.applications import EndUserForm, EndUserPage


class EndUser(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        if application["end_user"]:
            context = {
                "application": application,
                "title": EndUserPage.TITLE,
                "edit_url": reverse_lazy("applications:set_end_user", kwargs={"pk": application_id}),
                "remove_url": reverse_lazy("applications:remove_end_user", kwargs={"pk": application_id}),
                "answers": convert_end_user(application["end_user"], application_id, True),
                "highlight": ["Document"] if not application["end_user"]["document"] else {},
            }
            return render(request, "applications/check-your-answer.html", context)
        else:
            return redirect(reverse_lazy("applications:add_end_user", kwargs={"pk": application_id}))


class AddEndUser(AddParty):
    def __init__(self):
        super().__init__(
            new_url="applications:set_end_user", copy_url="applications:copy_end_user",
        )


class SetEndUser(SetParty):
    def __init__(self):
        super().__init__(
            url="applications:end_user_attach_document",
            name="end_user",
            form=new_party_form_group,
            back_url="applications:add_end_user",
            action=post_end_user,
            strings=EndUserForm,
            multiple_allowed=False,
        )


class RemoveEndUser(DeleteParty):
    def __init__(self):
        super().__init__(
            url="applications:add_end_user",
            action=delete_end_user,
            error=EndUserPage.DELETE_ERROR,
            multiple_allowed=False,
        )


class ExistingEndUser(ExistingPartiesList):
    def __init__(self):
        super().__init__(destination_url="applications:set_end_user", back_url="applications:add_end_user")
