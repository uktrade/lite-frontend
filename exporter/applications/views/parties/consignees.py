import logging

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect

from core.auth.views import LoginRequiredMixin
from core.wizard.views import BaseSessionWizardView

from exporter.applications.forms.parties import new_party_form_group
from exporter.applications.helpers.check_your_answers import convert_party
from exporter.applications.services import validate_party
from exporter.applications.views.parties.base import CopyParties, DeleteParty, CopyAndSetParty
from exporter.applications.forms.parties import (
    PartyReuseForm,
    PartySubTypeSelectForm,
    PartyNameForm,
    PartyWebsiteForm,
    PartyAddressForm,
)
from exporter.applications.services import (
    get_application,
    post_party,
    delete_party,
)
from exporter.core.helpers import (
    str_to_bool,
)
from exporter.core.constants import (
    SetPartyFormSteps,
)

from http import HTTPStatus
from lite_content.lite_exporter_frontend.applications import ConsigneeForm, ConsigneePage

from .payloads import SetConsigneePayloadBuilder

log = logging.getLogger(__name__)

from core.decorators import expect_status


class Consignee(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        if application["consignee"]:
            kwargs = {"pk": application_id, "obj_pk": application["consignee"]["id"]}
            context = {
                "application": application,
                "edit_url": reverse("applications:edit_consignee", kwargs=kwargs),
                "remove_url": reverse("applications:remove_consignee", kwargs=kwargs),
                "answers": convert_party(
                    party=application["consignee"],
                    application=application,
                    editable=application["status"]["value"] == "draft",
                ),
            }
            return render(request, "applications/consignee.html", context)
        else:
            return redirect(reverse("applications:add_consignee", kwargs={"pk": application_id}))


class AddConsignee(LoginRequiredMixin, FormView):
    form_class = PartyReuseForm
    template_name = "core/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.title
        return context

    def form_valid(self, form):
        reuse_party = str_to_bool(form.cleaned_data.get("reuse_party"))
        if reuse_party:
            success_url = reverse("applications:consignees_copy", kwargs=self.kwargs)
        else:
            success_url = reverse("applications:set_consignee", kwargs=self.kwargs)

        return HttpResponseRedirect(success_url)


class SetConsignee(LoginRequiredMixin, BaseSessionWizardView):
    party_type = "consignee"
    form_list = [
        (SetPartyFormSteps.PARTY_SUB_TYPE, PartySubTypeSelectForm),
        (SetPartyFormSteps.PARTY_NAME, PartyNameForm),
        (SetPartyFormSteps.PARTY_WEBSITE, PartyWebsiteForm),
        (SetPartyFormSteps.PARTY_ADDRESS, PartyAddressForm),
    ]

    def get_form_kwargs(self, step=None):
        PartySubTypeSelectForm.Layout.TITLE = "Select the type of consignee"
        PartyNameForm.Layout.TITLE = "Consignee name"
        PartyWebsiteForm.Layout.TITLE = "Consignee website address (optional)"
        PartyAddressForm.Layout.TITLE = "Consignee address"
        kwargs = super().get_form_kwargs(step)

        if step == SetPartyFormSteps.PARTY_ADDRESS:
            kwargs["request"] = self.request

        return kwargs

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        return context

    def get_payload(self, form_dict):
        return SetConsigneePayloadBuilder().build(form_dict)

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding consignee to application",
        "Unexpected error adding consignee to application",
    )
    def post_party_with_payload(self, pk, form_dict):
        payload = self.get_payload(form_dict)
        payload.update({"type": self.party_type})

        return post_party(self.request, pk, payload)

    def get_success_url(self, party_id):
        return reverse("applications:consignee_attach_document", kwargs={"pk": self.kwargs["pk"], "obj_pk": party_id})

    def done(self, form_list, form_dict, **kwargs):
        response, _ = self.post_party_with_payload(self.kwargs["pk"], form_dict)

        return redirect(self.get_success_url(response[self.party_type]["id"]))


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
