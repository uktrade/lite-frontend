from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.parties import new_party_form_group
from applications.helpers.check_your_answers import convert_party
from applications.services import get_application, post_party, validate_party, delete_party
from applications.views.parties.base import AddParty, SetParty, DeleteParty, CopyParties, CopyAndSetParty
from lite_content.lite_exporter_frontend.applications import EndUserForm, EndUserPage


class EndUser(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        if application["end_user"]:
            kwargs = {"pk": application_id, "obj_pk": application["end_user"]["id"]}
            context = {
                "application": application,
                "title": EndUserPage.TITLE,
                "edit_url": reverse_lazy("applications:edit_end_user", kwargs=kwargs),
                "remove_url": reverse_lazy("applications:remove_end_user", kwargs=kwargs),
                "answers": convert_party(
                    party=application["end_user"],
                    application=application,
                    editable=application["status"]["value"] == "draft",
                ),
                "highlight": ["Document"] if not application["end_user"]["document"] else {},
            }

            return render(request, "applications/check-your-answer.html", context)
        else:
            return redirect(reverse_lazy("applications:add_end_user", kwargs={"pk": application_id}))


class AddEndUser(AddParty):
    def __init__(self):
        super().__init__(new_url="applications:set_end_user", copy_url="applications:end_users_copy")


class SetEndUser(SetParty):
    def __init__(self, copy_existing=False):
        super().__init__(
            url="applications:end_user_attach_document",
            party_type="end_user",
            form=new_party_form_group,
            back_url="applications:end_user",
            strings=EndUserForm,
            copy_existing=copy_existing,
            post_action=post_party,
            validate_action=validate_party,
        )


class RemoveEndUser(DeleteParty):
    def __init__(self):
        super().__init__(
            url="applications:add_end_user", action=delete_party, error=EndUserPage.DELETE_ERROR,
        )


class CopyEndUsers(CopyParties):
    def __init__(self):
        super().__init__(new_party_type="end_user")


class CopyEndUser(CopyAndSetParty):
    def __init__(self):
        super().__init__(
            url="applications:end_user_attach_document",
            party_type="end_user",
            form=new_party_form_group,
            back_url="applications:end_users_copy",
            strings=EndUserForm,
            validate_action=validate_party,
            post_action=post_party,
        )


class EditEndUser(CopyAndSetParty):
    def __init__(self):
        super().__init__(
            url="applications:end_user_attach_document",
            party_type="end_user",
            form=new_party_form_group,
            back_url="applications:end_user",
            strings=EndUserForm,
            validate_action=validate_party,
            post_action=post_party,
        )
