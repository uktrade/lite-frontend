from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.parties import new_party_form_group
from applications.helpers.check_your_answers import convert_consignee
from applications.services import get_application, post_consignee, delete_consignee
from applications.views.parties.base import AddParty, ExistingPartiesList, SetParty, DeleteParty
from lite_content.lite_exporter_frontend.applications import ConsigneeForm, ConsigneePage


class Consignee(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        if application["consignee"]:
            context = {
                "application": application,
                "title": ConsigneePage.TITLE,
                "edit_url": reverse_lazy("applications:edit_consignee", kwargs={"pk": application_id}),
                "remove_url": reverse_lazy("applications:remove_consignee", kwargs={"pk": application_id}),
                "answers": convert_consignee(application["consignee"], application_id, True),
            }
            return render(request, "applications/check-your-answer.html", context)
        else:
            return redirect(reverse_lazy("applications:add_consignee", kwargs={"pk": application_id}))


class AddConsignee(AddParty):
    def __init__(self):
        super().__init__(
            new_url="applications:set_consignee", copy_url="applications:copy_consignee",
        )


class SetConsignee(SetParty):
    def __init__(self, copy_existing=False):
        super().__init__(
            url="applications:consignee_attach_document",
            name="consignee",
            form=new_party_form_group,
            back_url="applications:add_consignee",
            action=post_consignee,
            strings=ConsigneeForm,
            multiple_allowed=False,
            copy_existing=copy_existing,
        )


class EditConsignee(SetConsignee):
    def __init__(self):
        super().__init__(copy_existing=True)


class RemoveConsignee(DeleteParty):
    def __init__(self, **kwargs):
        super().__init__(
            url="applications:add_consignee",
            action=delete_consignee,
            error=ConsigneePage.DELETE_ERROR,
            multiple_allowed=False,
            **kwargs,
        )


class ExistingConsignee(ExistingPartiesList):
    def __init__(self):
        super().__init__(destination_url="applications:set_consignee", back_url="applications:add_consignee")
