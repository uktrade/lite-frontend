from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from exporter.applications.forms.parties import new_party_form_group
from exporter.applications.helpers.check_your_answers import convert_party
from exporter.applications.services import get_application, post_party, delete_party, validate_party
from exporter.applications.views.parties.base import AddParty, CopyParties, SetParty, DeleteParty, CopyAndSetParty
from lite_content.lite_exporter_frontend.applications import ConsigneeForm, ConsigneePage

from core.auth.views import LoginRequiredMixin


class Consignee(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        if application["consignee"]:
            kwargs = {"pk": application_id, "obj_pk": application["consignee"]["id"]}
            context = {
                "application": application,
                "title": ConsigneePage.TITLE,
                "edit_url": reverse("applications:edit_consignee", kwargs=kwargs),
                "remove_url": reverse("applications:remove_consignee", kwargs=kwargs),
                "answers": convert_party(
                    party=application["consignee"],
                    application=application,
                    editable=application["status"]["value"] == "draft",
                ),
            }
            return render(request, "applications/end-user.html", context)
        else:
            return redirect(reverse("applications:add_consignee", kwargs={"pk": application_id}))


class AddConsignee(LoginRequiredMixin, AddParty):
    def __init__(self):
        super().__init__(new_url="applications:set_consignee", copy_url="applications:consignees_copy")

    @property
    def back_url(self):
        return reverse("applications:task_list", kwargs={"pk": self.kwargs["pk"]}) + "#consignee"


class SetConsignee(LoginRequiredMixin, SetParty):
    def __init__(self):
        super().__init__(
            url="applications:consignee_attach_document",
            party_type="consignee",
            form=new_party_form_group,
            back_url="applications:consignee",
            strings=ConsigneeForm,
            post_action=post_party,
            validate_action=validate_party,
        )


class RemoveConsignee(LoginRequiredMixin, DeleteParty):
    def __init__(self, **kwargs):
        super().__init__(
            url="applications:add_consignee",
            action=delete_party,
            error=ConsigneePage.DELETE_ERROR,
            **kwargs,
        )


class CopyConsignees(LoginRequiredMixin, CopyParties):
    def __init__(self):
        super().__init__(new_party_type="consignee")


class CopyConsignee(LoginRequiredMixin, CopyAndSetParty):
    def __init__(self):
        super().__init__(
            url="applications:consignee_attach_document",
            party_type="consignee",
            form=new_party_form_group,
            back_url="applications:consignees_copy",
            strings=ConsigneeForm,
            validate_action=validate_party,
            post_action=post_party,
        )


class EditConsignee(LoginRequiredMixin, CopyAndSetParty):
    def __init__(self):
        super().__init__(
            url="applications:consignee_attach_document",
            party_type="consignee",
            form=new_party_form_group,
            back_url="applications:consignee",
            strings=ConsigneeForm,
            validate_action=validate_party,
            post_action=post_party,
        )
