import logging
import requests

from http import HTTPStatus

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin

from exporter.applications.services import get_application
from exporter.core.helpers import get_rfd_certificate, has_valid_rfd_certificate
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.firearms import (
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmNameForm,
    FirearmProductControlListEntryForm,
    FirearmPvGradingForm,
    FirearmPvGradingDetailsForm,
    FirearmReplicaForm,
    FirearmRFDValidityForm,
)
from exporter.goods.services import post_firearm
from lite_forms.generators import error_page


logger = logging.getLogger(__name__)


class AddGoodFirearmSteps:
    CATEGORY = "CATEGORY"
    NAME = "NAME"
    PRODUCT_CONTROL_LIST_ENTRY = "PRODUCT_CONTROL_LIST_ENTRY"
    PV_GRADING = "PV_GRADING"
    PV_GRADING_DETAILS = "PV_GRADING_DETAILS"
    CALIBRE = "CALIBRE"
    IS_REPLICA = "IS_REPLICA"
    IS_RFD_CERTIFICATE_VALID = "IS_RFD_CERTIFICATE_VALID"
    IS_REGISTERED_FIREARMS_DEALER = "IS_REGISTERED_FIREARMS_DEALER"


def has_rfd_certificate(wizard):
    return has_valid_rfd_certificate(wizard.application)


def is_pv_graded(wizard):
    add_goods_cleaned_data = wizard.get_cleaned_data_for_step(AddGoodFirearmSteps.PV_GRADING)
    return add_goods_cleaned_data.get("is_pv_graded")


class AddGoodFirearm(LoginRequiredMixin, BaseSessionWizardView):
    form_list = [
        (AddGoodFirearmSteps.CATEGORY, FirearmCategoryForm),
        (AddGoodFirearmSteps.NAME, FirearmNameForm),
        (AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY, FirearmProductControlListEntryForm),
        (AddGoodFirearmSteps.PV_GRADING, FirearmPvGradingForm),
        (AddGoodFirearmSteps.PV_GRADING_DETAILS, FirearmPvGradingDetailsForm),
        (AddGoodFirearmSteps.CALIBRE, FirearmCalibreForm),
        (AddGoodFirearmSteps.IS_REPLICA, FirearmReplicaForm),
        (AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID, FirearmRFDValidityForm),
    ]
    condition_dict = {
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID: has_rfd_certificate,
    }

    condition_dict = {
        AddGoodFirearmSteps.PV_GRADING_DETAILS: is_pv_graded,
    }

    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_2_0:
            raise Http404

        try:
            self.application = get_application(self.request, self.kwargs["pk"])
        except requests.exceptions.HTTPError:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["hide_step_count"] = True
        ctx["back_link_url"] = reverse(
            "applications:new_good",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def get_cleaned_data_for_step(self, step):
        cleaned_data = super().get_cleaned_data_for_step(step)
        if cleaned_data is None:
            return {}
        return cleaned_data

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY:
            kwargs["request"] = self.request

        if step == AddGoodFirearmSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request

        if step == AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID:
            kwargs["rfd_certificate"] = get_rfd_certificate(self.application)

        return kwargs

    def get_payload(self, form_list):
        firearm_data_keys = [
            "calibre",
            "category",
            "is_replica",
            "replica_description",
        ]

        keys_to_remove = [
            "is_rfd_valid",
        ]

        payload = {}
        firearm_data = {}
        for form in form_list:
            for k, v in form.cleaned_data.items():
                if k in keys_to_remove:
                    continue

                if k in firearm_data_keys:
                    firearm_data[k] = v
                else:
                    payload[k] = v

        payload["firearm_details"] = firearm_data

        if payload.get("is_pv_graded"):
            payload["date_of_issue"] = payload["date_of_issue"].isoformat()

        return payload

    def get_success_url(self, api_resp_data):
        return reverse(
            "applications:add_good_summary",
            kwargs={"pk": self.kwargs["pk"], "good_pk": api_resp_data["good"]["id"]},
        )

    def done(self, form_list, **kwargs):
        payload = self.get_payload(form_list)
        api_resp_data, status_code = post_firearm(
            self.request,
            payload,
        )
        if status_code != HTTPStatus.CREATED:
            logger.error(
                "Error creating firearm - response was: %s - %s",
                status_code,
                api_resp_data,
                exc_info=True,
            )
            return error_page(self.request, "Unexpected error adding firearm")

        return redirect(self.get_success_url(api_resp_data))
