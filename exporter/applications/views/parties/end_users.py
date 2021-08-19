from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from exporter.applications.forms.parties import new_party_form_group
from exporter.applications.helpers.check_your_answers import convert_party, is_application_export_type_permanent
from exporter.applications.services import get_application, post_party, validate_party, delete_party
from exporter.applications.views.parties.base import AddParty, SetParty, DeleteParty, CopyParties, CopyAndSetParty
from exporter.core.constants import OPEN
from lite_content.lite_exporter_frontend.applications import EndUserForm, EndUserPage

from core.auth.views import LoginRequiredMixin


class EndUser(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        is_permanent_app = is_application_export_type_permanent(application)
        if application["end_user"]:
            kwargs = {"pk": application_id, "obj_pk": application["end_user"]["id"]}
            context = {
                "application": application,
                "title": EndUserPage.TITLE,
                "edit_url": reverse("applications:edit_end_user", kwargs=kwargs),
                "remove_url": reverse("applications:remove_end_user", kwargs=kwargs),
                "answers": convert_party(
                    party=application["end_user"],
                    application=application,
                    editable=application["status"]["value"] == "draft",
                ),
                "highlight": ["Document"]
                if (is_permanent_app and application.sub_type != OPEN and not application["end_user"]["document"])
                else {},
            }

            return render(request, "applications/end-user.html", context)
        else:
            return redirect(reverse("applications:add_end_user", kwargs={"pk": application_id}))


class AddEndUser(LoginRequiredMixin, AddParty):
    def __init__(self):
        super().__init__(new_url="applications:set_end_user", copy_url="applications:end_users_copy")

    @property
    def back_url(self):
        return reverse("applications:task_list", kwargs={"pk": self.kwargs["pk"]}) + "#end_user"


class SetEndUser(LoginRequiredMixin, SetParty):
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

    def get_success_url(self):
        if self.application.sub_type == OPEN:
            return reverse("applications:end_user", kwargs={"pk": self.object_pk})
        else:
            return reverse(
                self.url, kwargs={"pk": self.object_pk, "obj_pk": self.get_validated_data()[self.party_type]["id"]}
            )


class RemoveEndUser(LoginRequiredMixin, DeleteParty):
    def __init__(self):
        super().__init__(
            url="applications:add_end_user", action=delete_party, error=EndUserPage.DELETE_ERROR,
        )


class CopyEndUsers(LoginRequiredMixin, CopyParties):
    def __init__(self):
        super().__init__(new_party_type="end_user")


class CopyEndUser(LoginRequiredMixin, CopyAndSetParty):
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

    def get_success_url(self):
        if self.application.sub_type == OPEN:
            return reverse("applications:end_user", kwargs={"pk": self.object_pk})
        else:
            return reverse(
                self.url, kwargs={"pk": self.object_pk, "obj_pk": self.get_validated_data()[self.party_type]["id"]}
            )


class EditEndUser(LoginRequiredMixin, CopyAndSetParty):
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
