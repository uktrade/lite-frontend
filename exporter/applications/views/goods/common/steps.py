from exporter.core.wizard.steps import Step
from exporter.goods.forms.common import (
    ProductControlListEntryForm,
    ProductNameForm,
    ProductPartNumberForm,
    ProductPVGradingForm,
    ProductPVGradingDetailsForm,
)

from .initial import (
    get_control_list_entry_initial_data,
    get_name_initial_data,
    get_pv_grading_details_initial_data,
    get_pv_grading_initial_data,
)
from .payloads import get_part_number_payload


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


class ProductPartNumberStep(Step):
    form_class = ProductPartNumberForm

    def get_initial(self, view):
        no_part_number_comments = view.good.get("no_part_number_comments")
        if no_part_number_comments:
            return {
                "part_number_missing": True,
                "no_part_number_comments": no_part_number_comments,
            }
        return {
            "part_number": view.good["part_number"],
        }

    def get_step_data(self, form):
        return get_part_number_payload(form)


class ProductPVGradingStep(Step):
    form_class = ProductPVGradingForm
    name = "PV_GRADING"

    def get_initial(self, view):
        return get_pv_grading_initial_data(view.good)


class ProductPVGradingDetailsStep(Step):
    form_class = ProductPVGradingDetailsForm
    name = "PV_GRADING_DETAILS"

    def get_initial(self, view):
        return get_pv_grading_details_initial_data(view.good)

    def get_form_kwargs(self, view):
        return {"request": view.request}
