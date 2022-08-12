import logging

from http import HTTPStatus

from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import FormView

from lite_forms.generators import error_page

from core.auth.views import LoginRequiredMixin

from exporter.core.common.decorators import expect_status
from exporter.core.common.exceptions import ServiceError
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.common import (
    ProductControlListEntryForm,
    ProductNameForm,
)

from .initial import (
    get_control_list_entry_initial_data,
    get_name_initial_data,
)
from .mixins import (
    ApplicationMixin,
    GoodMixin,
)


logger = logging.getLogger(__name__)


class BaseProductEditView(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    FormView,
):
    template_name = "core/form.html"

    def get_success_url(self):
        raise NotImplementedError(f"Implement `get_success_url` for {self.__class__.__name__}")

    def get_back_link_url(self):
        return self.get_success_url()

    def get_edit_payload(self, form):
        raise NotImplementedError(f"Implement `get_edit_payload` for {self.__class__.__name__}")

    def edit_object(self, request, good_id, payload):
        raise NotImplementedError(f"Implement `edit_object` for {self.__class__.__name__}")

    def form_valid(self, form):
        self.edit_object(self.request, self.good["id"], self.get_edit_payload(form))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["back_link_url"] = self.get_back_link_url()

        return ctx


class BaseEditName:
    form_class = ProductNameForm

    def get_initial(self):
        return get_name_initial_data(self.good)


class BaseEditControlListEntry:
    form_class = ProductControlListEntryForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_initial(self):
        return get_control_list_entry_initial_data(self.good)


class BaseProductEditWizardView(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    def handle_service_error(self, service_error):
        logger.error(
            service_error.log_message,
            service_error.status_code,
            service_error.response,
            exc_info=True,
        )
        if settings.DEBUG:
            raise service_error
        return error_page(self.request, service_error.user_message)

    def get_success_url(self):
        raise NotImplementedError(f"Implement `get_success_url` for {self.__class__.__name__}")

    def get_back_link_url(self):
        return self.get_success_url()

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = self.get_success_url()
        ctx["title"] = form.Layout.TITLE
        return ctx

    def get_payload(self, form_dict):
        raise NotImplementedError(f"Implement `get_payload` on f{self.__class__.__name__}")

    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_object(self, request, good_pk, payload):
        raise NotImplementedError(f"Implement `edit_object` on f{self.__class__.__name__}")

    def process_forms(self, form_list, form_dict, **kwargs):
        self.edit_object(self.request, self.good["id"], self.get_payload(form_dict))

    def done(self, form_list, form_dict, **kwargs):
        try:
            self.process_forms(form_list, form_dict, **kwargs)
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())
