from exporter.applications.views.goods.common.initial import (
    get_control_list_entry_initial_data,
    get_name_initial_data,
)
from exporter.core.wizard.steps import Step
from exporter.goods.forms.common import (
    ProductControlListEntryForm,
    ProductNameForm,
)


class ProductNameStep(Step):
    form_class = ProductNameForm

    def get_initial(self, view):
        return get_name_initial_data(view.good)


class ProductControlListEntryStep(Step):
    form_class = ProductControlListEntryForm

    def get_initial(self, view):
        return get_control_list_entry_initial_data(view.good)

    def get_form_kwargs(self, view):
        return {"request": view.request}
