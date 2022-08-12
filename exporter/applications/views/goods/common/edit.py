from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin

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
