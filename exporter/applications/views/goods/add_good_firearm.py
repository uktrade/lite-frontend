import logging

from http import HTTPStatus

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin

from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.firearms import (
    FirearmCategoryForm,
    FirearmNameForm,
    FirearmProductControlListEntryForm,
)
from exporter.goods.services import post_firearm
from lite_forms.generators import error_page


logger = logging.getLogger(__name__)


class AddGoodFirearmSteps:
    CATEGORY = "CATEGORY"
    NAME = "NAME"
    PRODUCT_CONTROL_LIST_ENTRY = "PRODUCT_CONTROL_LIST_ENTRY"


class AddGoodFirearm(LoginRequiredMixin, BaseSessionWizardView):
    form_list = [
        (AddGoodFirearmSteps.CATEGORY, FirearmCategoryForm),
        (AddGoodFirearmSteps.NAME, FirearmNameForm),
        (AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY, FirearmProductControlListEntryForm),
    ]

    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_2_0:
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

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY:
            kwargs["request"] = self.request

        return kwargs

    def done(self, form_list, **kwargs):
        firearm_data_keys = ["category"]
        all_data = {}
        firearm_data = {}
        for form in form_list:
            for k, v in form.cleaned_data.items():
                if k in firearm_data_keys:
                    firearm_data[k] = v
                else:
                    all_data[k] = v

        all_data["is_pv_graded"] = "no"
        all_data["firearm_details"] = firearm_data

        api_resp_data, status_code = post_firearm(
            self.request,
            all_data,
        )

        if status_code != HTTPStatus.CREATED:
            logger.error(
                "Error creating firearm - response was: %s - %s",
                status_code,
                api_resp_data,
                exc_info=True,
            )
            return error_page(self.request, "Unexpected error adding firearm")

        return redirect(
            reverse(
                "applications:add_good_summary",
                kwargs={"pk": self.kwargs["pk"], "good_pk": api_resp_data["good"]["id"]},
            )
        )
