from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.parties import new_party_form_group
from applications.helpers.check_your_answers import convert_party
from applications.services import get_application, post_party, delete_party, validate_party
from applications.views.parties.base import AddParty, CopyParties, SetParty, DeleteParty, CopyAndSetParty
from lite_content.lite_exporter_frontend.applications import ConsigneeForm, ConsigneePage


class Consignee(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        if application["consignee"]:
            kwargs = {"pk": application_id, "obj_pk": application["consignee"]["id"]}
            context = {
                "application": application,
                "title": ConsigneePage.TITLE,
                "edit_url": reverse_lazy("applications:edit_consignee", kwargs=kwargs),
                "remove_url": reverse_lazy("applications:remove_consignee", kwargs=kwargs),
                "answers": convert_party(
                    party=application["consignee"],
                    application_id=application_id,
                    editable=application["status"]["value"] == "draft",
                ),
            }
            return render(request, "applications/check-your-answer.html", context)
        else:
            return redirect(reverse_lazy("applications:add_consignee", kwargs={"pk": application_id}))


class AddConsignee(AddParty):
    def __init__(self):
        super().__init__(new_url="applications:set_consignee", copy_url="applications:consignees_copy")


class SetConsignee(SetParty):
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


class RemoveConsignee(DeleteParty):
    def __init__(self, **kwargs):
        super().__init__(
            url="applications:add_consignee", action=delete_party, error=ConsigneePage.DELETE_ERROR, **kwargs,
        )


class CopyConsignees(CopyParties):
    def __init__(self):
        super().__init__(new_party_type="consignee")


class CopyConsignee(CopyAndSetParty):
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


class EditConsignee(CopyAndSetParty):
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
