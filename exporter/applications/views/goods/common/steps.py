from exporter.applications.views.goods.common.initial import get_name_initial_data
from exporter.core.wizard.steps import Step
from exporter.goods.forms.common import ProductNameForm


class ProductNameStep(Step):
    form_class = ProductNameForm

    def get_initial(self, view):
        return get_name_initial_data(view.good)
